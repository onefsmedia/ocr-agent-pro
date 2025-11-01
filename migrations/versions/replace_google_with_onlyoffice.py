"""Replace Google integrations with OnlyOffice integrations

Revision ID: replace_google_with_onlyoffice
Revises: 
Create Date: 2025-10-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'replace_google_with_onlyoffice'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Remove Google integration columns
    try:
        op.drop_column('document', 'google_drive_id')
    except Exception:
        pass
    
    try:
        op.drop_column('document', 'google_sheet_id')
    except Exception:
        pass
    
    try:
        op.drop_column('document', 'google_doc_id')
    except Exception:
        pass
    
    # Add OnlyOffice integration columns
    try:
        op.add_column('document', sa.Column('onlyoffice_file_id', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('document', sa.Column('onlyoffice_sheet_id', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('document', sa.Column('onlyoffice_doc_id', sa.String(100), nullable=True))
    except Exception:
        pass


def downgrade():
    # Remove OnlyOffice integration columns
    try:
        op.drop_column('document', 'onlyoffice_file_id')
    except Exception:
        pass
    
    try:
        op.drop_column('document', 'onlyoffice_sheet_id')
    except Exception:
        pass
    
    try:
        op.drop_column('document', 'onlyoffice_doc_id')
    except Exception:
        pass
    
    # Add back Google integration columns
    try:
        op.add_column('document', sa.Column('google_drive_id', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('document', sa.Column('google_sheet_id', sa.String(100), nullable=True))
    except Exception:
        pass
    
    try:
        op.add_column('document', sa.Column('google_doc_id', sa.String(100), nullable=True))
    except Exception:
        pass