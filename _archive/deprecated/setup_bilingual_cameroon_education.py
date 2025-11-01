#!/usr/bin/env python3
"""
Enhanced setup script for Cameroonian Education System with English and French sections
Adds complete bilingual education structure from primary to high school
"""

from app import create_app, db
from app.models import Subject, ClassLevel

def setup_bilingual_cameroon_education():
    """Setup complete Cameroonian bilingual education system"""
    
    app = create_app()
    with app.app_context():
        
        # Create tables if they don't exist
        db.create_all()
        
        # Add education_section column if it doesn't exist
        try:
            from sqlalchemy import text
            db.session.execute(text("""
                ALTER TABLE class_levels 
                ADD COLUMN IF NOT EXISTS education_section VARCHAR(20)
            """))
            db.session.commit()
            print("✅ Added education_section column")
        except Exception as e:
            print(f"ℹ️  education_section column handling: {e}")
        
        # Clear existing class levels for clean update
        ClassLevel.query.delete()
        db.session.commit()
        
        # Comprehensive Cameroonian Education System Class Levels
        class_levels_data = [
            # PRIMARY EDUCATION (6 years) - Both sections use same French system
            {'name': 'SIL (English)', 'name_french': 'Section d\'Initiation au Langage', 'education_level': 'primary', 'education_section': 'english', 'grade_number': 1},
            {'name': 'SIL (French)', 'name_french': 'Section d\'Initiation au Langage', 'education_level': 'primary', 'education_section': 'french', 'grade_number': 1},
            
            {'name': 'CP (English)', 'name_french': 'Cours Préparatoire', 'education_level': 'primary', 'education_section': 'english', 'grade_number': 2},
            {'name': 'CP (French)', 'name_french': 'Cours Préparatoire', 'education_level': 'primary', 'education_section': 'french', 'grade_number': 2},
            
            {'name': 'CE1 (English)', 'name_french': 'Cours Élémentaire 1ère année', 'education_level': 'primary', 'education_section': 'english', 'grade_number': 3},
            {'name': 'CE1 (French)', 'name_french': 'Cours Élémentaire 1ère année', 'education_level': 'primary', 'education_section': 'french', 'grade_number': 3},
            
            {'name': 'CE2 (English)', 'name_french': 'Cours Élémentaire 2ème année', 'education_level': 'primary', 'education_section': 'english', 'grade_number': 4},
            {'name': 'CE2 (French)', 'name_french': 'Cours Élémentaire 2ème année', 'education_level': 'primary', 'education_section': 'french', 'grade_number': 4},
            
            {'name': 'CM1 (English)', 'name_french': 'Cours Moyen 1ère année', 'education_level': 'primary', 'education_section': 'english', 'grade_number': 5},
            {'name': 'CM1 (French)', 'name_french': 'Cours Moyen 1ère année', 'education_level': 'primary', 'education_section': 'french', 'grade_number': 5},
            
            {'name': 'CM2 (English)', 'name_french': 'Cours Moyen 2ème année', 'education_level': 'primary', 'education_section': 'english', 'grade_number': 6},
            {'name': 'CM2 (French)', 'name_french': 'Cours Moyen 2ème année', 'education_level': 'primary', 'education_section': 'french', 'grade_number': 6},
            
            # SECONDARY EDUCATION FIRST CYCLE (4 years)
            # English Section
            {'name': 'Form 1 (English)', 'name_french': 'Sixième Anglophone', 'education_level': 'secondary_first_cycle', 'education_section': 'english', 'grade_number': 7},
            {'name': 'Form 2 (English)', 'name_french': 'Cinquième Anglophone', 'education_level': 'secondary_first_cycle', 'education_section': 'english', 'grade_number': 8},
            {'name': 'Form 3 (English)', 'name_french': 'Quatrième Anglophone', 'education_level': 'secondary_first_cycle', 'education_section': 'english', 'grade_number': 9},
            {'name': 'Form 4 (English)', 'name_french': 'Troisième Anglophone', 'education_level': 'secondary_first_cycle', 'education_section': 'english', 'grade_number': 10},
            
            # French Section
            {'name': '6ème (French)', 'name_french': 'Sixième', 'education_level': 'secondary_first_cycle', 'education_section': 'french', 'grade_number': 7},
            {'name': '5ème (French)', 'name_french': 'Cinquième', 'education_level': 'secondary_first_cycle', 'education_section': 'french', 'grade_number': 8},
            {'name': '4ème (French)', 'name_french': 'Quatrième', 'education_level': 'secondary_first_cycle', 'education_section': 'french', 'grade_number': 9},
            {'name': '3ème (French)', 'name_french': 'Troisième', 'education_level': 'secondary_first_cycle', 'education_section': 'french', 'grade_number': 10},
            
            # SECONDARY EDUCATION SECOND CYCLE (3 years)
            # English Section (GCE A-Level system)
            {'name': 'Form 5 (English)', 'name_french': 'Seconde Anglophone', 'education_level': 'secondary_second_cycle', 'education_section': 'english', 'grade_number': 11},
            {'name': 'Lower Sixth (English)', 'name_french': 'Première Anglophone', 'education_level': 'secondary_second_cycle', 'education_section': 'english', 'grade_number': 12},
            {'name': 'Upper Sixth (English)', 'name_french': 'Terminale Anglophone', 'education_level': 'secondary_second_cycle', 'education_section': 'english', 'grade_number': 13},
            
            # French Section (Baccalauréat system)
            {'name': '2nde (French)', 'name_french': 'Seconde', 'education_level': 'secondary_second_cycle', 'education_section': 'french', 'grade_number': 11},
            {'name': '1ère (French)', 'name_french': 'Première', 'education_level': 'secondary_second_cycle', 'education_section': 'french', 'grade_number': 12},
            {'name': 'Terminale (French)', 'name_french': 'Terminale', 'education_level': 'secondary_second_cycle', 'education_section': 'french', 'grade_number': 13},
        ]
        
        # Enhanced subjects for both sections
        subjects_data = [
            # CORE SUBJECTS - Both Sections
            {'name': 'English Language', 'name_french': 'Langue Anglaise', 'category': 'languages'},
            {'name': 'French Language', 'name_french': 'Langue Française', 'category': 'languages'},
            {'name': 'Mathematics', 'name_french': 'Mathématiques', 'category': 'science'},
            {'name': 'General Science', 'name_french': 'Sciences Générales', 'category': 'science'},
            {'name': 'History', 'name_french': 'Histoire', 'category': 'humanities'},
            {'name': 'Geography', 'name_french': 'Géographie', 'category': 'humanities'},
            
            # PRIMARY SUBJECTS
            {'name': 'Social Studies', 'name_french': 'Études Sociales', 'category': 'humanities'},
            {'name': 'Physical Education', 'name_french': 'Éducation Physique', 'category': 'arts'},
            {'name': 'Religious Education', 'name_french': 'Instruction Religieuse', 'category': 'humanities'},
            {'name': 'Arts and Crafts', 'name_french': 'Arts et Artisanat', 'category': 'arts'},
            {'name': 'Music Education', 'name_french': 'Éducation Musicale', 'category': 'arts'},
            {'name': 'Moral Education', 'name_french': 'Instruction Civique', 'category': 'humanities'},
            
            # SECONDARY SCIENCES
            {'name': 'Physics', 'name_french': 'Physique', 'category': 'science'},
            {'name': 'Chemistry', 'name_french': 'Chimie', 'category': 'science'},
            {'name': 'Biology', 'name_french': 'Biologie', 'category': 'science'},
            {'name': 'Additional Mathematics', 'name_french': 'Mathématiques Additionnelles', 'category': 'science'},
            {'name': 'Further Mathematics', 'name_french': 'Mathématiques Approfondies', 'category': 'science'},
            {'name': 'Computer Science', 'name_french': 'Informatique', 'category': 'technical'},
            
            # LANGUAGES AND LITERATURE
            {'name': 'Literature in English', 'name_french': 'Littérature Anglaise', 'category': 'languages'},
            {'name': 'French Literature', 'name_french': 'Littérature Française', 'category': 'languages'},
            {'name': 'German Language', 'name_french': 'Langue Allemande', 'category': 'languages'},
            {'name': 'Spanish Language', 'name_french': 'Langue Espagnole', 'category': 'languages'},
            {'name': 'Arabic Language', 'name_french': 'Langue Arabe', 'category': 'languages'},
            {'name': 'Latin', 'name_french': 'Latin', 'category': 'languages'},
            {'name': 'Indigenous Languages', 'name_french': 'Langues Locales', 'category': 'languages'},
            
            # HUMANITIES AND SOCIAL SCIENCES
            {'name': 'Economics', 'name_french': 'Sciences Économiques', 'category': 'humanities'},
            {'name': 'Philosophy', 'name_french': 'Philosophie', 'category': 'humanities'},
            {'name': 'Sociology', 'name_french': 'Sociologie', 'category': 'humanities'},
            {'name': 'Psychology', 'name_french': 'Psychologie', 'category': 'humanities'},
            {'name': 'Political Science', 'name_french': 'Sciences Politiques', 'category': 'humanities'},
            {'name': 'Citizenship Education', 'name_french': 'Éducation à la Citoyenneté', 'category': 'humanities'},
            {'name': 'Law', 'name_french': 'Droit', 'category': 'humanities'},
            
            # TECHNICAL AND VOCATIONAL
            {'name': 'Technical Drawing', 'name_french': 'Dessin Technique', 'category': 'technical'},
            {'name': 'Agriculture', 'name_french': 'Agriculture', 'category': 'technical'},
            {'name': 'Home Economics', 'name_french': 'Économie Domestique', 'category': 'technical'},
            {'name': 'Accounting', 'name_french': 'Comptabilité', 'category': 'technical'},
            {'name': 'Business Studies', 'name_french': 'Études Commerciales', 'category': 'technical'},
            {'name': 'Office Practice', 'name_french': 'Pratique de Bureau', 'category': 'technical'},
            {'name': 'Entrepreneurship', 'name_french': 'Entrepreneuriat', 'category': 'technical'},
            {'name': 'Industrial Arts', 'name_french': 'Arts Industriels', 'category': 'technical'},
            
            # ARTS AND CREATIVE STUDIES
            {'name': 'Fine Arts', 'name_french': 'Beaux-Arts', 'category': 'arts'},
            {'name': 'Performing Arts', 'name_french': 'Arts du Spectacle', 'category': 'arts'},
            {'name': 'Music', 'name_french': 'Musique', 'category': 'arts'},
            {'name': 'Drama/Theatre', 'name_french': 'Art Dramatique', 'category': 'arts'},
            {'name': 'Visual Arts', 'name_french': 'Arts Visuels', 'category': 'arts'},
            
            # SPECIALIZED STREAMS (Upper Secondary)
            # English Section A-Level Subjects
            {'name': 'Advanced Level English', 'name_french': 'Anglais Niveau Avancé', 'category': 'languages'},
            {'name': 'Advanced Level Mathematics', 'name_french': 'Mathématiques Niveau Avancé', 'category': 'science'},
            {'name': 'Advanced Level Physics', 'name_french': 'Physique Niveau Avancé', 'category': 'science'},
            {'name': 'Advanced Level Chemistry', 'name_french': 'Chimie Niveau Avancé', 'category': 'science'},
            {'name': 'Advanced Level Biology', 'name_french': 'Biologie Niveau Avancé', 'category': 'science'},
            
            # French Section Baccalauréat Subjects
            {'name': 'Sciences Naturelles', 'name_french': 'Sciences Naturelles', 'category': 'science'},
            {'name': 'Sciences Physiques', 'name_french': 'Sciences Physiques', 'category': 'science'},
            {'name': 'Sciences Économiques et Sociales', 'name_french': 'Sciences Économiques et Sociales', 'category': 'humanities'},
            {'name': 'Littéraires', 'name_french': 'Filière Littéraire', 'category': 'languages'},
        ]
        
        # Add Class Levels
        print("🏫 Adding bilingual Cameroonian class levels...")
        for level_data in class_levels_data:
            existing_level = ClassLevel.query.filter_by(name=level_data['name']).first()
            if not existing_level:
                level = ClassLevel(**level_data)
                db.session.add(level)
                print(f"Added class level: {level_data['name']} ({level_data['education_section']})")
            else:
                print(f"Class level already exists: {level_data['name']}")
        
        # Add Subjects
        print("\\n📚 Adding enhanced Cameroonian subjects...")
        Subject.query.delete()  # Clear existing for clean update
        db.session.commit()
        
        for subject_data in subjects_data:
            subject = Subject(**subject_data)
            db.session.add(subject)
            print(f"Added subject: {subject_data['name']}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("\\n✅ Successfully added bilingual Cameroonian education system!")
            
            # Print comprehensive summary
            total_subjects = Subject.query.count()
            total_levels = ClassLevel.query.count()
            
            print(f"\\n📊 BILINGUAL EDUCATION SYSTEM SUMMARY:")
            print("=" * 60)
            print(f"Total Subjects: {total_subjects}")
            print(f"Total Class Levels: {total_levels}")
            
            # Class levels by section and level
            english_primary = ClassLevel.query.filter_by(education_section='english', education_level='primary').count()
            french_primary = ClassLevel.query.filter_by(education_section='french', education_level='primary').count()
            english_sec1 = ClassLevel.query.filter_by(education_section='english', education_level='secondary_first_cycle').count()
            french_sec1 = ClassLevel.query.filter_by(education_section='french', education_level='secondary_first_cycle').count()
            english_sec2 = ClassLevel.query.filter_by(education_section='english', education_level='secondary_second_cycle').count()
            french_sec2 = ClassLevel.query.filter_by(education_section='french', education_level='secondary_second_cycle').count()
            
            print(f"\\n🏫 CLASS LEVELS BY SECTION:")
            print(f"  📚 PRIMARY EDUCATION:")
            print(f"    English Section: {english_primary} levels (SIL-CM2)")
            print(f"    French Section: {french_primary} levels (SIL-CM2)")
            print(f"  🎓 SECONDARY FIRST CYCLE:")
            print(f"    English Section: {english_sec1} levels (Form 1-4)")
            print(f"    French Section: {french_sec1} levels (6ème-3ème)")
            print(f"  🎯 SECONDARY SECOND CYCLE:")
            print(f"    English Section: {english_sec2} levels (Form 5-Upper Sixth)")
            print(f"    French Section: {french_sec2} levels (2nde-Terminale)")
            
            print(f"\\n📖 SUBJECTS BY CATEGORY:")
            for category in ['science', 'languages', 'humanities', 'technical', 'arts']:
                count = Subject.query.filter_by(category=category).count()
                print(f"  {category.title()}: {count} subjects")
            
            print(f"\\n🇨🇲 EDUCATION FEATURES:")
            print("✅ Complete bilingual system (English/French)")
            print("✅ Primary education (6 years, both sections)")
            print("✅ Secondary first cycle (4 years, both sections)")
            print("✅ Secondary second cycle (3 years, both sections)")
            print("✅ GCE A-Level system (English section)")
            print("✅ Baccalauréat system (French section)")
            print("✅ Comprehensive subject coverage")
            print("✅ Technical and vocational options")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding data: {e}")
            raise e

if __name__ == '__main__':
    setup_bilingual_cameroon_education()