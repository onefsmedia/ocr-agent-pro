// OCR Agent JavaScript Functions

// Global variables
let currentSessionId = null;
let uploadInProgress = false;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check authentication status
    checkGoogleAuth();
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize file upload drag and drop
    initializeFileUpload();
    
    // Initialize auto-refresh for database status
    setInterval(refreshDashboardStats, 30000); // Every 30 seconds
}

function initializeFileUpload() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('file-input');
    
    if (uploadArea && fileInput) {
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileUpload(files[0]);
            }
        });
        
        // Click to upload
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                handleFileUpload(this.files[0]);
            }
        });
    }
}

function handleFileUpload(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg', 'image/tiff', 'image/bmp'];
    if (!allowedTypes.includes(file.type)) {
        showNotification('Please select a valid file type (PDF, PNG, JPG, JPEG, TIFF, BMP)', 'error');
        return;
    }
    
    // Validate file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
        showNotification('File size must be less than 16MB', 'error');
        return;
    }
    
    // Auto-fill document name if empty
    const nameInput = document.getElementById('document-name');
    if (nameInput && !nameInput.value.trim()) {
        nameInput.value = file.name.replace(/\.[^/.]+$/, ''); // Remove extension
    }
    
    showNotification(`Selected: ${file.name}`, 'info');
}

async function uploadDocument() {
    if (uploadInProgress) return;
    
    const form = document.getElementById('upload-form');
    const formData = new FormData(form);
    
    uploadInProgress = true;
    showUploadProgress(true);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Document uploaded successfully! Processing started in background. ${data.estimated_time}`, 'success');
            form.reset();
            
            // Start polling for status updates
            pollDocumentStatus(data.document_id, data.filename);
            
            refreshDashboardStats();
        } else {
            showNotification(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showNotification('Upload failed: ' + error.message, 'error');
    } finally {
        uploadInProgress = false;
        showUploadProgress(false);
    }
}

async function pollDocumentStatus(documentId, filename) {
    const maxPolls = 60; // Poll for up to 60 times (30 minutes at 30-second intervals)
    let pollCount = 0;
    
    const statusTooltip = showPersistentNotification(
        `Processing "${filename}"... This may take several minutes.`, 
        'info',
        true // persistent
    );
    
    const pollInterval = setInterval(async () => {
        pollCount++;
        
        try {
            const response = await fetch(`/api/document-status/${documentId}`);
            const data = await response.json();
            
            if (response.ok) {
                const status = data.processing_status;
                
                if (status === 'completed') {
                    clearInterval(pollInterval);
                    hidePersistentNotification(statusTooltip);
                    showNotification(
                        `"${filename}" processed successfully! Created ${data.chunk_count} text chunks.`, 
                        'success'
                    );
                    refreshDashboardStats();
                } else if (status === 'failed') {
                    clearInterval(pollInterval);
                    hidePersistentNotification(statusTooltip);
                    showNotification(
                        `Processing failed for "${filename}": ${data.error_message || 'Unknown error'}`, 
                        'error'
                    );
                } else {
                    // Still processing - update the notification
                    updatePersistentNotification(
                        statusTooltip,
                        `Processing "${filename}"... Status: ${status} (${data.extracted_text_length} characters extracted)`
                    );
                }
            } else {
                console.error('Error checking status:', data.error);
            }
        } catch (error) {
            console.error('Error polling document status:', error);
        }
        
        // Stop polling after max attempts
        if (pollCount >= maxPolls) {
            clearInterval(pollInterval);
            hidePersistentNotification(statusTooltip);
            showNotification(
                `Processing status check timed out for "${filename}". Check the documents list for updates.`, 
                'warning'
            );
        }
    }, 30000); // Poll every 30 seconds
}

function showUploadProgress(show) {
    const progressDiv = document.getElementById('upload-progress');
    if (progressDiv) {
        progressDiv.style.display = show ? 'block' : 'none';
    }
}

// Google Authentication Functions
async function checkGoogleAuth() {
    try {
        const response = await fetch('/auth/google/status');
        const data = await response.json();
        
        updateGoogleStatus(data.authorized);
        return data.authorized;
    } catch (error) {
        console.error('Failed to check Google auth status:', error);
        updateGoogleStatus(false);
        return false;
    }
}

function updateGoogleStatus(isAuthorized) {
    const statusElements = document.querySelectorAll('#google-status, .google-status');
    statusElements.forEach(element => {
        if (isAuthorized) {
            element.innerHTML = '<i class="fas fa-check-circle text-success"></i>';
            element.title = 'Google services connected';
        } else {
            element.innerHTML = '<i class="fas fa-times-circle text-danger"></i>';
            element.title = 'Google services not connected';
        }
    });
}

function authorizeGoogle() {
    window.location.href = '/auth/google/authorize';
}

async function revokeGoogleAuth() {
    try {
        const response = await fetch('/auth/google/revoke', { method: 'POST' });
        const data = await response.json();
        
        showNotification(data.message, 'info');
        updateGoogleStatus(false);
    } catch (error) {
        showNotification('Failed to revoke authorization', 'error');
    }
}

// Chat Functions
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const chatContainer = document.getElementById('chat-messages');
    
    if (!input || !input.value.trim()) return;
    
    const message = input.value.trim();
    input.value = '';
    
    // Add user message to chat
    addMessageToChat('user', message);
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            // Update session ID
            currentSessionId = data.session_id;
            
            // Add assistant response
            addMessageToChat('assistant', data.response);
        } else {
            addMessageToChat('assistant', 'Sorry, I encountered an error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessageToChat('assistant', 'Sorry, I couldn\'t process your message. Please try again.');
    }
}

function addMessageToChat(role, content) {
    const chatContainer = document.getElementById('chat-messages');
    if (!chatContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = `message-avatar ${role}`;
    avatarDiv.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = `message-bubble ${role}`;
    bubbleDiv.textContent = content;
    
    if (role === 'user') {
        messageDiv.appendChild(bubbleDiv);
        messageDiv.appendChild(avatarDiv);
    } else {
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);
    }
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addTypingIndicator() {
    const chatContainer = document.getElementById('chat-messages');
    if (!chatContainer) return null;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message assistant typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar assistant"><i class="fas fa-robot"></i></div>
        <div class="message-bubble assistant">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    
    const typingId = 'typing-' + Date.now();
    typingDiv.id = typingId;
    
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return typingId;
}

function removeTypingIndicator(typingId) {
    if (typingId) {
        const typingElement = document.getElementById(typingId);
        if (typingElement) {
            typingElement.remove();
        }
    }
}

// Search Functions
async function performSearch() {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');
    
    if (!searchInput || !resultsContainer) return;
    
    const query = searchInput.value.trim();
    if (!query) return;
    
    resultsContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                limit: 10
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.results) {
            displaySearchResults(data.results);
        } else {
            resultsContainer.innerHTML = '<div class="text-muted">No results found.</div>';
        }
    } catch (error) {
        resultsContainer.innerHTML = '<div class="text-danger">Search failed: ' + error.message + '</div>';
    }
}

function displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="text-muted">No results found.</div>';
        return;
    }
    
    const resultsHTML = results.map(result => `
        <div class="search-result card mb-2">
            <div class="card-body">
                <h6 class="card-title">${result.document_name}</h6>
                <p class="card-text text-truncate-2">${result.content}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">Similarity: ${(result.similarity_score * 100).toFixed(1)}%</small>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewDocument('${result.document_id}')">
                        View Document
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = resultsHTML;
}

// Dashboard Functions
async function refreshDashboardStats() {
    try {
        const response = await fetch('/api/documents?per_page=1');
        const data = await response.json();
        
        // Update document count
        const docCountElements = document.querySelectorAll('.doc-count');
        docCountElements.forEach(el => el.textContent = data.pagination?.total || 0);
        
        // Update other stats as needed
        
    } catch (error) {
        console.error('Failed to refresh dashboard stats:', error);
    }
}

async function testLLMConnection() {
    try {
        showNotification('Testing LLM connection...', 'info');
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: 'Hello, are you working?'
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('LLM connection successful!', 'success');
        } else {
            showNotification('LLM connection failed: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        showNotification('LLM connection failed: ' + error.message, 'error');
    }
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function showPersistentNotification(message, type = 'info', persistent = false) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-spinner fa-spin me-2"></i>${message}
        ${!persistent ? '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' : ''}
    `;
    
    document.body.appendChild(notification);
    
    return notification; // Return reference for updates
}

function updatePersistentNotification(notification, newMessage) {
    if (notification && notification.parentNode) {
        notification.innerHTML = `
            <i class="fas fa-spinner fa-spin me-2"></i>${newMessage}
        `;
    }
}

function hidePersistentNotification(notification) {
    if (notification && notification.parentNode) {
        notification.remove();
    }
}

function viewDocument(documentId) {
    window.open(`/api/documents/${documentId}`, '_blank');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

// Settings Functions
async function saveSettings() {
    const form = document.getElementById('settings-form');
    if (!form) return;
    
    const formData = new FormData(form);
    const settings = {};
    
    for (let [key, value] of formData.entries()) {
        settings[key] = value;
    }
    
    try {
        const response = await fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Settings saved successfully!', 'success');
        } else {
            showNotification('Failed to save settings: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        showNotification('Failed to save settings: ' + error.message, 'error');
    }
}

// Event Listeners
document.addEventListener('keydown', function(e) {
    // Enter key in chat input
    if (e.key === 'Enter' && e.target.id === 'chat-input') {
        e.preventDefault();
        sendMessage();
    }
    
    // Enter key in search input
    if (e.key === 'Enter' && e.target.id === 'search-input') {
        e.preventDefault();
        performSearch();
    }
});

// Quick chat function for dashboard
async function quickChat() {
    const input = document.getElementById('quick-chat-input');
    const responseDiv = document.getElementById('quick-chat-response');
    
    if (!input || !input.value.trim()) return;
    
    responseDiv.style.display = 'block';
    responseDiv.innerHTML = '<div class="text-center text-muted"><i class="fas fa-spinner fa-spin"></i> Thinking...</div>';
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: input.value
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            responseDiv.innerHTML = data.response || 'No response received.';
            input.value = '';
        } else {
            responseDiv.innerHTML = 'Error: ' + (data.error || 'Unknown error');
        }
    } catch (error) {
        responseDiv.innerHTML = 'Error: ' + error.message;
    }
}