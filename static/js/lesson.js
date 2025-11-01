// JS for Lesson Generator Panel

async function loadLessons() {
    const subject = document.getElementById('subject-select').value;
    const classLevel = document.getElementById('class-select').value;

    if (!subject || !classLevel) {
        alert('Please select subject and class');
        return;
    }

    document.getElementById('lessons-loading').classList.remove('d-none');
    const resp = await fetch('/api/lessons/load', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject: subject, class_level: classLevel})
    });

    const data = await resp.json();
    document.getElementById('lessons-loading').classList.add('d-none');

    if (data.success) {
        const container = document.getElementById('lessons-container');
        container.innerHTML = '';
        data.lessons.forEach((lesson, idx) => {
            const div = document.createElement('div');
            div.className = 'mb-2';
            div.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>${lesson.lesson}</div>
                    <div>
                        <button class="btn btn-sm btn-outline-primary" onclick="generateLesson(${idx})">Generate</button>
                    </div>
                </div>
            `;
            container.appendChild(div);
        });
    } else {
        alert('Failed to load lessons: ' + data.error);
    }
}

async function generateLesson(index) {
    const subject = document.getElementById('subject-select').value;
    const classLevel = document.getElementById('class-select').value;
    const lessons = Array.from(document.querySelectorAll('#lessons-container div')).map(d => d.innerText.trim());
    const lesson = {lesson: lessons[index]};

    const resp = await fetch('/api/lessons/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject: subject, class_level: classLevel, lesson: lesson})
    });

    const data = await resp.json();

    if (data.success) {
        // Open OnlyOffice editor
        if (data.edit_url) {
            window.open(data.edit_url, '_blank');
        } else {
            alert('Lesson generated, but no edit URL returned.');
        }
    } else {
        alert('Lesson generation failed: ' + data.error);
    }
}

async function generateAllLessons() {
    const subject = document.getElementById('subject-select').value;
    const classLevel = document.getElementById('class-select').value;

    if (!subject || !classLevel) {
        alert('Please select subject and class');
        return;
    }

    // Load lessons first
    const loadResp = await fetch('/api/lessons/load', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject: subject, class_level: classLevel})
    });

    const loadData = await loadResp.json();
    if (!loadData.success) {
        alert('Failed to load lessons: ' + loadData.error);
        return;
    }

    const lessons = loadData.lessons;
    for (const l of lessons) {
        const genResp = await fetch('/api/lessons/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({subject: subject, class_level: classLevel, lesson: l})
        });
        const genData = await genResp.json();
        console.log('Generated', genData);
    }

    alert('All lessons generation triggered. Check Generated Lessons table.');
}

async function refreshGeneratedLessons() {
    const subject = document.getElementById('subject-select').value;
    const classLevel = document.getElementById('class-select').value;

    const resp = await fetch('/api/lessons/generated', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({subject: subject, class_level: classLevel})
    });

    const data = await resp.json();

    if (data.success) {
        const tableBody = document.getElementById('generated-lessons-body');
        if (!tableBody) return;
        tableBody.innerHTML = '';
        data.lessons.forEach((lesson) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${lesson.lesson_title}</td>
                <td><a href="${lesson.view_url}" target="_blank" class="btn btn-sm btn-primary">Edit</a></td>
                <td><a href="${lesson.download_url}" target="_blank" class="btn btn-sm btn-secondary">Download</a></td>
                <td>${lesson.generated_at || ''}</td>
            `;
            tableBody.appendChild(tr);
        });
    } else {
        alert('Failed to refresh generated lessons: ' + data.error);
    }
}

// Initialize subject/class selects on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const subjectSelect = document.getElementById('subject-select');
    const classSelect = document.getElementById('class-select');

    if (subjectSelect) {
        subjectSelect.innerHTML = document.getElementById('dashboard-subject') ? document.getElementById('dashboard-subject').innerHTML : subjectSelect.innerHTML;
    }
    if (classSelect) {
        classSelect.innerHTML = document.getElementById('dashboard-class') ? document.getElementById('dashboard-class').innerHTML : classSelect.innerHTML;
    }
});
