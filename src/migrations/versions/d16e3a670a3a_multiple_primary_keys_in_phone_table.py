"""multiple primary keys in Phone table

Revision ID: d16e3a670a3a
Revises: e84b66a82b3f
Create Date: 2023-05-10 20:12:28.635527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd16e3a670a3a'
down_revision = 'e84b66a82b3f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('phone', 'phone_id')
    op.add_column('phone_advert', sa.Column('code', sa.Integer(), nullable=False))
    op.add_column('phone_advert', sa.Column('number', sa.Integer(), nullable=False))
    op.drop_constraint('phone_advert_phone_id_fkey', 'phone_advert', type_='foreignkey')
    op.create_foreign_key(None, 'phone_advert', 'phone', ['number'], ['number'])
    op.create_foreign_key(None, 'phone_advert', 'phone', ['code'], ['code'])
    op.drop_column('phone_advert', 'phone_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phone_advert', sa.Column('phone_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'phone_advert', type_='foreignkey')
    op.drop_constraint(None, 'phone_advert', type_='foreignkey')
    op.create_foreign_key('phone_advert_phone_id_fkey', 'phone_advert', 'phone', ['phone_id'], ['phone_id'])
    op.drop_column('phone_advert', 'number')
    op.drop_column('phone_advert', 'code')
    op.add_column('phone', sa.Column('phone_id', sa.INTEGER(), server_default=sa.text("nextval('phone_phone_id_seq'::regclass)"), autoincrement=True, nullable=False))
    # ### end Alembic commands ###
