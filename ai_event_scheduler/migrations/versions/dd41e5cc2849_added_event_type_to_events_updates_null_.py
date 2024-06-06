"""Added event_type to events updates null check

Revision ID: dd41e5cc2849
Revises: 
Create Date: 2024-06-02 23:26:27.844028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd41e5cc2849'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_feedback_event_id'), ['event_id'], unique=False)

    op.create_table('resource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('resource', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_resource_event_id'), ['event_id'], unique=False)

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('ticket_price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('total_revenue', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('attendee_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('average_rating', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('event_type', sa.String(length=64), nullable=True))
        batch_op.create_index(batch_op.f('ix_event_user_id'), ['user_id'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('last_login', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('login_count', sa.Integer(), nullable=True))
        batch_op.alter_column('username',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.drop_constraint('user_username_key', type_='unique')
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.create_unique_constraint('user_username_key', ['username'])
        batch_op.alter_column('username',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.drop_column('login_count')
        batch_op.drop_column('last_login')
        batch_op.drop_column('email')

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_user_id'))
        batch_op.drop_column('event_type')
        batch_op.drop_column('average_rating')
        batch_op.drop_column('attendee_count')
        batch_op.drop_column('total_revenue')
        batch_op.drop_column('ticket_price')
        batch_op.drop_column('date')

    with op.batch_alter_table('resource', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_resource_event_id'))

    op.drop_table('resource')
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_feedback_event_id'))

    op.drop_table('feedback')
    # ### end Alembic commands ###
