from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from flask import session, current_app
import json
import io

class GoogleService:
    """Service for Google APIs integration"""
    
    def __init__(self):
        self.credentials = self._get_credentials()
    
    def _get_credentials(self):
        """Get Google API credentials from session or database"""
        
        # Try to get from session first
        if 'google_credentials' in session:
            return Credentials(**session['google_credentials'])
        
        # Try to get from database
        try:
            from app.models import SystemSettings
            setting = SystemSettings.query.filter_by(key='google_credentials').first()
            if setting:
                creds_dict = json.loads(setting.value)
                return Credentials(**creds_dict)
        except Exception:
            pass
        
        return None
    
    def _refresh_credentials_if_needed(self):
        """Refresh credentials if they're expired"""
        
        if not self.credentials:
            return False
        
        if self.credentials.expired and self.credentials.refresh_token:
            try:
                self.credentials.refresh(Request())
                
                # Update session and database
                credentials_dict = {
                    'token': self.credentials.token,
                    'refresh_token': self.credentials.refresh_token,
                    'token_uri': self.credentials.token_uri,
                    'client_id': self.credentials.client_id,
                    'client_secret': self.credentials.client_secret,
                    'scopes': self.credentials.scopes
                }
                
                session['google_credentials'] = credentials_dict
                
                # Update database
                from app.models import SystemSettings
                from app import db
                
                setting = SystemSettings.query.filter_by(key='google_credentials').first()
                if setting:
                    setting.value = json.dumps(credentials_dict)
                    db.session.commit()
                
                return True
                
            except Exception as e:
                print(f"Failed to refresh credentials: {e}")
                return False
        
        return True
    
    def is_authenticated(self):
        """Check if user is authenticated with Google"""
        
        if not self.credentials:
            return False
        
        if self.credentials.valid:
            return True
        
        return self._refresh_credentials_if_needed()
    
    def upload_to_drive(self, file_path, file_name, folder_id=None):
        """Upload file to Google Drive"""
        
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google")
        
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            
            # File metadata
            file_metadata = {'name': file_name}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Upload file
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return file.get('id')
            
        except Exception as e:
            raise Exception(f"Google Drive upload failed: {str(e)}")
    
    def create_google_doc(self, title, content):
        """Create a new Google Doc with content"""
        
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google")
        
        try:
            # Create document
            docs_service = build('docs', 'v1', credentials=self.credentials)
            
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            
            # Add content to document
            if content:
                requests = [
                    {
                        'insertText': {
                            'location': {'index': 1},
                            'text': content
                        }
                    }
                ]
                
                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests}
                ).execute()
            
            return doc_id
            
        except Exception as e:
            raise Exception(f"Google Docs creation failed: {str(e)}")
    
    def create_google_sheet(self, document):
        """Create a Google Sheet with document chunks"""
        
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google")
        
        try:
            sheets_service = build('sheets', 'v4', credentials=self.credentials)
            
            # Create spreadsheet
            spreadsheet = {
                'properties': {
                    'title': f"{document.name} - Chunks"
                }
            }
            
            result = sheets_service.spreadsheets().create(
                body=spreadsheet
            ).execute()
            
            spreadsheet_id = result.get('spreadsheetId')
            
            # Prepare data for the sheet
            values = [
                ['Chunk Index', 'Content', 'Character Start', 'Character End', 'Created At']
            ]
            
            for chunk in document.chunks:
                values.append([
                    chunk.chunk_index,
                    chunk.content[:1000] + "..." if len(chunk.content) > 1000 else chunk.content,
                    chunk.start_char or '',
                    chunk.end_char or '',
                    chunk.created_at.strftime('%Y-%m-%d %H:%M:%S') if chunk.created_at else ''
                ])
            
            # Update the sheet with data
            body = {
                'values': values
            }
            
            sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return spreadsheet_id
            
        except Exception as e:
            raise Exception(f"Google Sheets creation failed: {str(e)}")
    
    def sync_document_to_drive(self, document):
        """Sync document to Google Drive and create associated Docs/Sheets"""
        
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google")
        
        results = {}
        
        try:
            # Upload original file to Drive
            drive_id = self.upload_to_drive(document.file_path, document.name)
            results['drive_id'] = drive_id
            
            # Create Google Doc with extracted text
            if document.extracted_text:
                doc_id = self.create_google_doc(
                    f"{document.name} - Extracted Text",
                    document.extracted_text
                )
                results['doc_id'] = doc_id
            
            # Create Google Sheet with chunks
            if document.chunks:
                sheet_id = self.create_google_sheet(document)
                results['sheet_id'] = sheet_id
            
            return results
            
        except Exception as e:
            raise Exception(f"Document sync failed: {str(e)}")
    
    def get_drive_files(self, query=None, page_size=10):
        """Get list of files from Google Drive"""
        
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google")
        
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            
            # Build query parameters
            params = {
                'pageSize': page_size,
                'fields': 'nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime)'
            }
            
            if query:
                params['q'] = query
            
            results = service.files().list(**params).execute()
            return results.get('files', [])
            
        except Exception as e:
            raise Exception(f"Failed to get Drive files: {str(e)}")
    
    def download_from_drive(self, file_id, destination_path):
        """Download file from Google Drive"""
        
        if not self.is_authenticated():
            raise Exception("Not authenticated with Google")
        
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            
            # Get file
            request = service.files().get_media(fileId=file_id)
            
            # Download file
            with open(destination_path, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
            
            return destination_path
            
        except Exception as e:
            raise Exception(f"Download from Drive failed: {str(e)}")
    
    def test_connection(self):
        """Test connection to Google APIs"""
        
        try:
            if not self.is_authenticated():
                return {"status": "error", "message": "Not authenticated"}
            
            # Test Drive API
            service = build('drive', 'v3', credentials=self.credentials)
            about = service.about().get(fields='user').execute()
            
            return {
                "status": "connected",
                "user": about.get('user', {}).get('displayName', 'Unknown'),
                "email": about.get('user', {}).get('emailAddress', 'Unknown')
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}