"""adding chapo

Revision ID: 4e6a6a00164e
Revises: 64934708f362
Create Date: 2023-10-04 18:11:36.031269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e6a6a00164e'
down_revision = '64934708f362'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO recipe (name, instructions) VALUES ('Chapo', '1. Add 3 cups of flour in a bowl , 2. Add salt, sugar, 2 tbsp of oil and 1 ½ cups of water in a separate jar/ bowl. Stir until the salt and sugar dissolves.. Keep kneading for 10 minutes and add flour if needed until the dough becomes non-sticky. Add 2-3 tbsp of oil and continue kneading until the oil mixes well and the dough is soft. Cover the dough and leave it for 40 minutes, 3Next, start rolling each of the coil-like shape doughs with the rolling pin to form a circular shape again.')")
   
   


def downgrade():
    op.execute("DELETE FROM recipe WHERE name='Chapo'")

    
