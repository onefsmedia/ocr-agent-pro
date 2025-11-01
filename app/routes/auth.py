from flask import Blueprint, request, jsonify, redirect, url_for, session
import json
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/onlyoffice/status')
def onlyoffice_status():
    """Check OnlyOffice integration status"""
    
    try:
        from app.services.onlyoffice_service import OnlyOfficeService
        onlyoffice_service = OnlyOfficeService()
        connected = onlyoffice_service.check_connection()
        
        return jsonify({
            'authenticated': connected,
            'status': 'connected' if connected else 'disconnected',
            'service': 'onlyoffice'
        })
        
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'status': 'error',
            'error': str(e)
        }), 500

@auth_bp.route('/status')
def auth_status():
    """Get overall authentication status"""
    
    return jsonify({
        'authenticated': True,  # For now, assume always authenticated
        'service': 'local',
        'user': 'system'
    })

@auth_bp.route('/logout')
def logout():
    """Logout (clear session)"""
    
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# Placeholder routes for backward compatibility
@auth_bp.route('/google/status')
def google_status():
    """Legacy Google status route - redirects to OnlyOffice"""
    return redirect(url_for('auth.onlyoffice_status'))

@auth_bp.route('/google/authorize')
def google_authorize():
    """Legacy Google authorize route - returns not implemented"""
    return jsonify({
        'error': 'Google authentication has been replaced with OnlyOffice integration',
        'redirect': url_for('auth.onlyoffice_status')
    }), 501

@auth_bp.route('/google/callback')
def google_callback():
    """Legacy Google callback route - returns not implemented"""
    return jsonify({
        'error': 'Google authentication has been replaced with OnlyOffice integration',
        'redirect': url_for('auth.onlyoffice_status')
    }), 501