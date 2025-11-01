#!/usr/bin/env python3
"""
PostgreSQL Password Discovery Script
"""

import subprocess
import sys
import os

def test_password(password):
    """Test a password for postgres user"""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    cmd = [
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        "-U", "postgres",
        "-h", "localhost", 
        "-p", "5432",
        "-d", "postgres",
        "-c", "SELECT current_user;"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=5)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔍 PostgreSQL Password Discovery")
    print("=" * 40)
    
    # Common PostgreSQL passwords to try
    passwords = [
        "",              # No password
        "postgres",      # Default username as password
        "password",      # Common default
        "admin",         # Common admin password
        "root",          # Another common one
        "123456",        # Weak password
        "12345",         # Weak password
        "1234",          # Weak password
        "Master@2025",   # Your preferred password (maybe already set?)
        "Password123",   # Common pattern
        "postgres123",   # Username + numbers
        "pgadmin",       # pgAdmin default
        "qwerty",        # Common keyboard password
        "welcome",       # Common welcome password
        "test",          # Test password
        "demo",          # Demo password
        "guest",         # Guest password
        "user",          # User password
        "pass",          # Short for password
        "letmein",       # Common phrase
        "changeme",      # Default change-me password
    ]
    
    print(f"Testing {len(passwords)} common passwords...")
    print()
    
    for i, password in enumerate(passwords, 1):
        password_display = "(empty)" if not password else "*" * len(password)
        print(f"[{i:2d}/{len(passwords)}] Testing: {password_display}")
        
        success, stdout, stderr = test_password(password)
        
        if success:
            print(f"✅ SUCCESS! Password found: '{password}'")
            print(f"   Connection output: {stdout.strip()}")
            
            # Now create our user and database
            print("\n🛠️  Creating renderman user and ocr_agent database...")
            
            # Create user
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            create_user_cmd = [
                r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
                "-U", "postgres", "-h", "localhost", "-p", "5432", "-d", "postgres",
                "-c", "CREATE USER renderman WITH PASSWORD 'Master@2025' CREATEDB CREATEROLE;"
            ]
            
            result = subprocess.run(create_user_cmd, capture_output=True, text=True, env=env)
            if result.returncode == 0 or "already exists" in result.stderr:
                print("✅ User 'renderman' created/exists")
            else:
                print(f"❌ Failed to create user: {result.stderr}")
            
            # Create database
            create_db_cmd = [
                r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
                "-U", "postgres", "-h", "localhost", "-p", "5432", "-d", "postgres",
                "-c", "CREATE DATABASE ocr_agent OWNER renderman;"
            ]
            
            result = subprocess.run(create_db_cmd, capture_output=True, text=True, env=env)
            if result.returncode == 0 or "already exists" in result.stderr:
                print("✅ Database 'ocr_agent' created/exists")
            else:
                print(f"❌ Failed to create database: {result.stderr}")
            
            print("\n🎉 Setup completed!")
            print("\n📋 Discovered credentials:")
            print(f"   • PostgreSQL admin user: postgres")
            print(f"   • PostgreSQL admin password: {password}")
            print(f"   • OCR Agent user: renderman")
            print(f"   • OCR Agent password: Master@2025")
            print(f"   • OCR Agent database: ocr_agent")
            
            return True
        else:
            print(f"   ❌ Failed: {stderr.strip()}")
    
    print("\n💡 None of the common passwords worked.")
    print("   PostgreSQL may be configured with a custom password.")
    print("   You may need to reset it manually or check installation docs.")
    
    return False

if __name__ == "__main__":
    main()