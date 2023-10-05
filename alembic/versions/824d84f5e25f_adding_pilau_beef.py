"""adding pilau beef

Revision ID: 824d84f5e25f
Revises: 4e6a6a00164e
Create Date: 2023-10-05 16:53:47.915551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '824d84f5e25f'
down_revision = '4e6a6a00164e'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO recipe (name, instructions) VALUES ('Pilau Beef', '1. Peel the onions and garlic cloves, Wash the beef and add into a pan. Slice in one onion and 2 garlic cloves with the ginger. Add bay leaves, with a cup of water and some salt to taste., 2. Chop the remaining onion and garlic.Wash the rice and repeat until the water runs clear.In another pan, heat the oil under low heat. Add the onions into the pot and cook until the onions start to caramelize and become brown. You should stir the onions with a wooden spoon continuously to prevent burning. 3. Pour in the garlic and the ground spices. The brownish colour comes from the brown spices. Stir for 30 secs. 4.Add the rice into the pot. Pour in the stock and meat chunks. Add more water so there is enough to cook the rice (read the rice pack instructions). Taste for salt and add more if needed. 5. Add the rice into the pot. Pour in the stock and meat chunks. Add more water so there is enough to cook the rice (read the rice pack instructions). Taste for salt and add more if needed.')")


def downgrade():
    op.execute("DELETE FROM recipe WHERE name='Pilau Beef'")
