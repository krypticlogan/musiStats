"""Init migrate

Revision ID: 3d6808641107
Revises: 
Create Date: 2024-02-14 00:09:01.181275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d6808641107'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.alter_column('genre',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=45),
               existing_nullable=True)

    with op.batch_alter_table('track', schema=None) as batch_op:
        batch_op.alter_column('genre1',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=45),
               existing_nullable=False)
        batch_op.alter_column('genre2',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=45),
               existing_nullable=True)
        batch_op.alter_column('genre3',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=45),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('track', schema=None) as batch_op:
        batch_op.alter_column('genre3',
               existing_type=sa.String(length=45),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
        batch_op.alter_column('genre2',
               existing_type=sa.String(length=45),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
        batch_op.alter_column('genre1',
               existing_type=sa.String(length=45),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.alter_column('genre',
               existing_type=sa.String(length=45),
               type_=sa.VARCHAR(length=25),
               existing_nullable=True)

    # ### end Alembic commands ###
