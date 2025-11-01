#!/usr/bin/env python3
"""
Database setup script for OCR Agent
Creates the PostgreSQL database and user if they don't exist
"""

import subprocess
import sys
import os

def run_psql_command(command, user="postgres", password=None, database="postgres", port=5432):
    """Run a PostgreSQL command"""
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    
    cmd = [
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        "-U", user,
        "-h", "localhost", 
        "-p", str(port),
        "-d", database,
        "-c", command
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def try_common_passwords():
    """Try common PostgreSQL passwords"""
    common_passwords = [
        "Master@2025",  # Your preferred password
        "postgres",     # Common default
        "password",     # Another common default
        "admin",        # Yet another common one
        "",             # No password
    ]
    
    for password in common_passwords:
        print(f"Trying postgres user with password: {'(empty)' if not password else '***'}")
        success, stdout, stderr = run_psql_command("SELECT version();", password=password)
        if success:
            print(f"✅ Connected to PostgreSQL as postgres!")
            return password
        else:
            print(f"❌ Failed: {stderr.strip()}")
    
    return None

def create_user_and_database(postgres_password):
    """Create the renderman user and ocr_agent database"""
    
    # Create user
    print("\n📝 Creating renderman user...")
    create_user_cmd = "CREATE USER renderman WITH PASSWORD 'Master@2025' CREATEDB CREATEROLE;"
    success, stdout, stderr = run_psql_command(create_user_cmd, password=postgres_password)
    
    if success:
        print("✅ User 'renderman' created successfully!")
    elif "already exists" in stderr:
        print("ℹ️  User 'renderman' already exists")
    else:
        print(f"❌ Failed to create user: {stderr}")
        return False
    
    # Create database
    print("\n📝 Creating ocr_agent database...")
    create_db_cmd = "CREATE DATABASE ocr_agent OWNER renderman;"
    success, stdout, stderr = run_psql_command(create_db_cmd, password=postgres_password)
    
    if success:
        print("✅ Database 'ocr_agent' created successfully!")
    elif "already exists" in stderr:
        print("ℹ️  Database 'ocr_agent' already exists")
    else:
        print(f"❌ Failed to create database: {stderr}")
        return False
    
    # Grant privileges
    print("\n📝 Granting privileges...")
    grant_cmd = "GRANT ALL PRIVILEGES ON DATABASE ocr_agent TO renderman;"
    success, stdout, stderr = run_psql_command(grant_cmd, password=postgres_password)
    
    if success:
        print("✅ Privileges granted successfully!")
    else:
        print(f"⚠️  Warning: Failed to grant privileges: {stderr}")
    
    return True

def test_connection():
    """Test connection with renderman user"""
    print("\n🔍 Testing connection as renderman...")
    success, stdout, stderr = run_psql_command(
        "SELECT current_database(), current_user;", 
        user="renderman", 
        password="Master@2025",
        database="ocr_agent"
    )
    
    if success:
        print("✅ Successfully connected as renderman to ocr_agent database!")
        print(f"Output: {stdout.strip()}")
        return True
    else:
        print(f"❌ Failed to connect as renderman: {stderr}")
        return False

def main():
    print("🐘 PostgreSQL Database Setup for OCR Agent")
    print("=" * 50)
    
    # Step 1: Find working postgres credentials
    print("\n🔑 Step 1: Finding PostgreSQL admin credentials...")
    postgres_password = try_common_passwords()
    
    if not postgres_password:
        print("\n❌ Could not connect to PostgreSQL with any common passwords.")
        print("\n💡 Please provide the postgres user password:")
        postgres_password = input("Password: ")
        
        success, stdout, stderr = run_psql_command("SELECT version();", password=postgres_password)
        if not success:
            print(f"❌ Still failed to connect: {stderr}")
            sys.exit(1)
    
    # Step 2: Create user and database
    print(f"\n🏗️  Step 2: Setting up renderman user and ocr_agent database...")
    if not create_user_and_database(postgres_password):
        print("❌ Failed to setup database")
        sys.exit(1)
    
    # Step 3: Test connection
    print(f"\n🧪 Step 3: Testing final configuration...")
    if test_connection():
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Configuration Summary:")
        print("   • Database: ocr_agent")
        print("   • User: renderman")
        print("   • Password: Master@2025")
        print("   • Connection: postgresql://renderman:Master%402025@localhost:5432/ocr_agent")
    else:
        print("❌ Database setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()