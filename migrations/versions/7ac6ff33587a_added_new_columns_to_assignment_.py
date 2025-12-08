"""added new columns to assignment submission and class assignment models

Revision ID: 7ac6ff33587a
Revises: 910e28658fa0
Create Date: 2025-12-08 16:51:26.743671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ac6ff33587a'
down_revision = '910e28658fa0'
branch_labels = None
depends_on = None


def upgrade():
    # CLASS ASSIGNMENT TABLE
    with op.batch_alter_table('class_assignment', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'created_by_first_name',
            sa.String(length=50),
            nullable=False,
            server_default="Unknown"
        ))
        batch_op.add_column(sa.Column(
            'created_by_last_name',
            sa.String(length=50),
            nullable=False,
            server_default="Unknown"
        ))
        batch_op.add_column(sa.Column('due_date', sa.DateTime(), nullable=True))

    # STUDENT ASSIGNMENT SUBMISSION TABLE
    with op.batch_alter_table('student_assignment_submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'submitted_by_first_name',
            sa.String(length=50),
            nullable=False,
            server_default="Unknown"
        ))
        batch_op.add_column(sa.Column(
            'submitted_by_last_name',
            sa.String(length=50),
            nullable=False,
            server_default="Unknown"
        ))
        batch_op.add_column(sa.Column(
            'student_score',
            sa.Integer(),
            nullable=False,
            server_default="0"
        ))
        batch_op.add_column(sa.Column(
            'student_grade',
            sa.String(length=5),
            nullable=False,
            server_default="N/A"
        ))
        batch_op.drop_column('due_date')
        batch_op.drop_column('issued_date')


def downgrade():
    with op.batch_alter_table('student_assignment_submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('issued_date', sa.DATE(), nullable=False))
        batch_op.add_column(sa.Column('due_date', sa.DATE(), nullable=False))
        batch_op.drop_column('student_grade')
        batch_op.drop_column('student_score')
        batch_op.drop_column('submitted_by_last_name')
        batch_op.drop_column('submitted_by_first_name')

    with op.batch_alter_table('class_assignment', schema=None) as batch_op:
        batch_op.drop_column('due_date')
        batch_op.drop_column('created_by_last_name')
        batch_op.drop_column('created_by_first_name')
