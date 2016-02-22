"""empty message

Revision ID: 2b646de9cc1d
Revises: dd8bb9b55960
Create Date: 2016-02-22 19:12:38.128567

"""

# revision identifiers, used by Alembic.
revision = '2b646de9cc1d'
down_revision = 'dd8bb9b55960'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association',
    sa.Column('puppy_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.id'], ),
    sa.ForeignKeyConstraint(['puppy_id'], ['puppy.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    ### end Alembic commands ###