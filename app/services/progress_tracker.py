"""
Progress tracking for large file uploads and processing
"""

from flask import jsonify
from app.models import ProcessingJob
from app import db
from datetime import datetime

class ProgressTracker:
    """Track progress of file uploads and processing"""
    
    @staticmethod
    def create_job(job_type, document_id, estimated_duration=None):
        """Create a new processing job"""
        job = ProcessingJob(
            job_type=job_type,
            document_id=document_id,
            status='pending',
            progress_percentage=0,
            estimated_duration=estimated_duration
        )
        db.session.add(job)
        db.session.commit()
        return job.id
    
    @staticmethod
    def update_progress(job_id, progress_percentage, status=None, message=None):
        """Update job progress"""
        job = ProcessingJob.query.get(job_id)
        if job:
            job.progress_percentage = progress_percentage
            if status:
                job.status = status
            if message:
                job.status_message = message
            job.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_progress(job_id):
        """Get current job progress"""
        job = ProcessingJob.query.get(job_id)
        if job:
            return {
                'id': job.id,
                'status': job.status,
                'progress': job.progress_percentage,
                'message': getattr(job, 'status_message', ''),
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat()
            }
        return None
