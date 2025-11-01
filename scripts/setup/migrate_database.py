#!/usr/bin/env python3
"""
Database migration script to add Cameroonian education system columns
Adds document_type, subject, and class_level columns to the documents table
"""

from app import create_app, db
from sqlalchemy import text

def migrate_database():
    """Add new columns to the documents table"""
    
    app = create_app()
    with app.app_context():
        
        print("🔄 Starting database migration for Cameroonian education system...")
        
        try:
            # Check if columns already exist
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'documents' 
                AND column_name IN ('document_type', 'subject', 'class_level')
            """))
            
            existing_columns = [row[0] for row in result.fetchall()]
            print(f"📊 Existing columns: {existing_columns}")
            
            # Add document_type column if it doesn't exist
            if 'document_type' not in existing_columns:
                print("➕ Adding document_type column...")
                db.session.execute(text("""
                    ALTER TABLE documents 
                    ADD COLUMN document_type VARCHAR(50)
                """))
                print("✅ Added document_type column")
            else:
                print("ℹ️  document_type column already exists")
            
            # Add subject column if it doesn't exist
            if 'subject' not in existing_columns:
                print("➕ Adding subject column...")
                db.session.execute(text("""
                    ALTER TABLE documents 
                    ADD COLUMN subject VARCHAR(100)
                """))
                print("✅ Added subject column")
            else:
                print("ℹ️  subject column already exists")
            
            # Add class_level column if it doesn't exist  
            if 'class_level' not in existing_columns:
                print("➕ Adding class_level column...")
                db.session.execute(text("""
                    ALTER TABLE documents 
                    ADD COLUMN class_level VARCHAR(50)
                """))
                print("✅ Added class_level column")
            else:
                print("ℹ️  class_level column already exists")
            
            # Commit the changes
            db.session.commit()
            
            # Verify the columns were added
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'documents' 
                AND column_name IN ('document_type', 'subject', 'class_level')
                ORDER BY column_name
            """))
            
            print("\n📋 Migration Results:")
            print("=" * 50)
            for row in result.fetchall():
                column_name, data_type, is_nullable = row
                print(f"✅ {column_name}: {data_type} (nullable: {is_nullable})")
            
            # Create tables for new models if they don't exist
            print("\n🔄 Creating new tables for education system...")
            db.create_all()
            
            # Check if subjects and class_levels tables exist and have data
            subjects_count = db.session.execute(text("SELECT COUNT(*) FROM subjects")).scalar()
            levels_count = db.session.execute(text("SELECT COUNT(*) FROM class_levels")).scalar()
            
            print(f"\n📊 Database Status:")
            print(f"   Subjects: {subjects_count}")
            print(f"   Class Levels: {levels_count}")
            
            if subjects_count == 0 or levels_count == 0:
                print("\n⚠️  Warning: Education system data is missing!")
                print("   Run 'python setup_cameroon_education.py' to populate the data")
            
            print("\n✅ Database migration completed successfully!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = migrate_database()
    if not success:
        exit(1)