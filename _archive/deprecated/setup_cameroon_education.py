#!/usr/bin/env python3
"""
Setup script for Cameroonian Education System data
Adds subjects and class levels to the database
"""

from app import create_app, db
from app.models import Subject, ClassLevel

def setup_cameroon_education_data():
    """Setup Cameroonian education system subjects and class levels"""
    
    app = create_app()
    with app.app_context():
        
        # Create tables if they don't exist
        db.create_all()
        
        # Cameroonian Education System Class Levels
        class_levels_data = [
            # Primary Education (6 years)
            {'name': 'SIL', 'name_french': 'Section d\'Initiation au Langage', 'education_level': 'primary', 'grade_number': 1},
            {'name': 'CP', 'name_french': 'Cours Préparatoire', 'education_level': 'primary', 'grade_number': 2},
            {'name': 'CE1', 'name_french': 'Cours Élémentaire 1ère année', 'education_level': 'primary', 'grade_number': 3},
            {'name': 'CE2', 'name_french': 'Cours Élémentaire 2ème année', 'education_level': 'primary', 'grade_number': 4},
            {'name': 'CM1', 'name_french': 'Cours Moyen 1ère année', 'education_level': 'primary', 'grade_number': 5},
            {'name': 'CM2', 'name_french': 'Cours Moyen 2ème année', 'education_level': 'primary', 'grade_number': 6},
            
            # Secondary Education First Cycle (4 years)
            {'name': 'Form 1 (6ème)', 'name_french': 'Sixième', 'education_level': 'secondary_first_cycle', 'grade_number': 7},
            {'name': 'Form 2 (5ème)', 'name_french': 'Cinquième', 'education_level': 'secondary_first_cycle', 'grade_number': 8},
            {'name': 'Form 3 (4ème)', 'name_french': 'Quatrième', 'education_level': 'secondary_first_cycle', 'grade_number': 9},
            {'name': 'Form 4 (3ème)', 'name_french': 'Troisième', 'education_level': 'secondary_first_cycle', 'grade_number': 10},
            
            # Secondary Education Second Cycle (3 years)
            {'name': 'Form 5 (2nde)', 'name_french': 'Seconde', 'education_level': 'secondary_second_cycle', 'grade_number': 11},
            {'name': 'Lower Sixth (1ère)', 'name_french': 'Première', 'education_level': 'secondary_second_cycle', 'grade_number': 12},
            {'name': 'Upper Sixth (Tle)', 'name_french': 'Terminale', 'education_level': 'secondary_second_cycle', 'grade_number': 13},
        ]
        
        # Cameroonian Education System Subjects
        subjects_data = [
            # Core Subjects (Primary and Secondary)
            {'name': 'English Language', 'name_french': 'Langue Anglaise', 'category': 'languages'},
            {'name': 'French Language', 'name_french': 'Langue Française', 'category': 'languages'},
            {'name': 'Mathematics', 'name_french': 'Mathématiques', 'category': 'science'},
            {'name': 'Science', 'name_french': 'Sciences', 'category': 'science'},
            
            # Primary Subjects
            {'name': 'Social Studies', 'name_french': 'Études Sociales', 'category': 'humanities'},
            {'name': 'Physical Education', 'name_french': 'Éducation Physique', 'category': 'arts'},
            {'name': 'Religious Knowledge', 'name_french': 'Instruction Religieuse', 'category': 'humanities'},
            {'name': 'Arts and Crafts', 'name_french': 'Arts et Artisanat', 'category': 'arts'},
            {'name': 'Music', 'name_french': 'Musique', 'category': 'arts'},
            
            # Secondary Subjects - Sciences
            {'name': 'Physics', 'name_french': 'Physique', 'category': 'science'},
            {'name': 'Chemistry', 'name_french': 'Chimie', 'category': 'science'},
            {'name': 'Biology', 'name_french': 'Biologie', 'category': 'science'},
            {'name': 'Additional Mathematics', 'name_french': 'Mathématiques Additionnelles', 'category': 'science'},
            {'name': 'Further Mathematics', 'name_french': 'Mathématiques Avancées', 'category': 'science'},
            {'name': 'Computer Science', 'name_french': 'Informatique', 'category': 'technical'},
            
            # Secondary Subjects - Languages
            {'name': 'Literature in English', 'name_french': 'Littérature Anglaise', 'category': 'languages'},
            {'name': 'French Literature', 'name_french': 'Littérature Française', 'category': 'languages'},
            {'name': 'German Language', 'name_french': 'Langue Allemande', 'category': 'languages'},
            {'name': 'Spanish Language', 'name_french': 'Langue Espagnole', 'category': 'languages'},
            {'name': 'Arabic Language', 'name_french': 'Langue Arabe', 'category': 'languages'},
            {'name': 'Latin', 'name_french': 'Latin', 'category': 'languages'},
            
            # Secondary Subjects - Humanities
            {'name': 'History', 'name_french': 'Histoire', 'category': 'humanities'},
            {'name': 'Geography', 'name_french': 'Géographie', 'category': 'humanities'},
            {'name': 'Economics', 'name_french': 'Économie', 'category': 'humanities'},
            {'name': 'Philosophy', 'name_french': 'Philosophie', 'category': 'humanities'},
            {'name': 'Citizenship Education', 'name_french': 'Éducation à la Citoyenneté', 'category': 'humanities'},
            
            # Technical and Vocational Subjects
            {'name': 'Technical Drawing', 'name_french': 'Dessin Technique', 'category': 'technical'},
            {'name': 'Agriculture', 'name_french': 'Agriculture', 'category': 'technical'},
            {'name': 'Food and Nutrition', 'name_french': 'Alimentation et Nutrition', 'category': 'technical'},
            {'name': 'Accounting', 'name_french': 'Comptabilité', 'category': 'technical'},
            {'name': 'Commercial Studies', 'name_french': 'Études Commerciales', 'category': 'technical'},
            {'name': 'Office Practice', 'name_french': 'Pratique de Bureau', 'category': 'technical'},
            {'name': 'Home Economics', 'name_french': 'Économie Domestique', 'category': 'technical'},
            
            # Arts Subjects
            {'name': 'Fine Arts', 'name_french': 'Beaux-Arts', 'category': 'arts'},
            {'name': 'Music Education', 'name_french': 'Éducation Musicale', 'category': 'arts'},
            {'name': 'Drama', 'name_french': 'Art Dramatique', 'category': 'arts'},
            
            # Local Languages (some examples)
            {'name': 'Cameroon Local Languages', 'name_french': 'Langues Locales du Cameroun', 'category': 'languages'},
        ]
        
        # Add Class Levels
        print("Adding Cameroonian class levels...")
        for level_data in class_levels_data:
            existing_level = ClassLevel.query.filter_by(name=level_data['name']).first()
            if not existing_level:
                level = ClassLevel(**level_data)
                db.session.add(level)
                print(f"Added class level: {level_data['name']}")
            else:
                print(f"Class level already exists: {level_data['name']}")
        
        # Add Subjects
        print("\\nAdding Cameroonian subjects...")
        for subject_data in subjects_data:
            existing_subject = Subject.query.filter_by(name=subject_data['name']).first()
            if not existing_subject:
                subject = Subject(**subject_data)
                db.session.add(subject)
                print(f"Added subject: {subject_data['name']}")
            else:
                print(f"Subject already exists: {subject_data['name']}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("\\n✅ Successfully added Cameroonian education system data!")
            
            # Print summary
            total_subjects = Subject.query.count()
            total_levels = ClassLevel.query.count()
            
            print(f"\\n📊 Summary:")
            print(f"Total Subjects: {total_subjects}")
            print(f"Total Class Levels: {total_levels}")
            
            print(f"\\n📚 Subjects by Category:")
            for category in ['science', 'languages', 'humanities', 'technical', 'arts']:
                count = Subject.query.filter_by(category=category).count()
                print(f"  {category.title()}: {count}")
                
            print(f"\\n🎓 Education Levels:")
            primary_count = ClassLevel.query.filter_by(education_level='primary').count()
            secondary_first_count = ClassLevel.query.filter_by(education_level='secondary_first_cycle').count()
            secondary_second_count = ClassLevel.query.filter_by(education_level='secondary_second_cycle').count()
            print(f"  Primary: {primary_count}")
            print(f"  Secondary First Cycle: {secondary_first_count}")
            print(f"  Secondary Second Cycle: {secondary_second_count}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding data: {e}")
            raise e

if __name__ == '__main__':
    setup_cameroon_education_data()