from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker,declarative_base
import random

Base = declarative_base()

recipe_ingredient_association = Table('recipe_ingredient_association', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredient.id')),
    Column('quantity', String)
)

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructions = Column(String)
    ingredients = relationship("Ingredient", secondary=recipe_ingredient_association)


    def __repr__(self):
        return self.name

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipes = relationship("Recipe", secondary=recipe_ingredient_association)


class RecipeBook:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.engine = create_engine('sqlite:///recipe_book.db')
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

        self.added_ingredients = set()

    

    def add_recipe(self, recipe):
        self.session.add(recipe)
        self.session.commit()

    def remove_recipe(self, recipe):
        self.session.delete(recipe)
        self.session.commit()

    def search_recipe(self, query):
        return self.session.query(Recipe).filter(Recipe.name.ilike('%' + query + '%')).first()

    def add_to_grocery_list(self, ingredients):
        for ingredient in ingredients:
            if ingredient not in self.added_ingredients:
                if not self.session.query(Ingredient).filter(Ingredient.name.ilike(ingredient)).first():
                    self.session.add(Ingredient(name=ingredient))
                self.added_ingredients.add(ingredient)
        self.session.commit()

    def remove_from_grocery_list(self, ingredient):
        ingredient_obj = self.session.query(Ingredient).filter(Ingredient.name.ilike(ingredient)).first()
        if ingredient_obj:
            self.session.delete(ingredient_obj)
            self.session.commit()
            self.added_ingredients.remove(ingredient)

    def get_random_recipe(self):
        return random.choice(self.session.query(Recipe).all())
    
    def remove_recipe_by_name(self, recipe_name):
        recipe = self.session.query(Recipe).filter(Recipe.name == recipe_name).first()
        if recipe:
            self.session.delete(recipe)
            self.session.commit()
            print(f"Recipe '{recipe_name}' has been removed.")
        else:
            print(f"Recipe '{recipe_name}' not found.")

    def check_if_ingredients_added(self, recipe_id):
        return recipe_id in self.added_ingredients

    def mark_ingredients_as_added(self, recipe_id):
        self.added_ingredients.add(recipe_id)


recipe_book = RecipeBook()

recipe1 = Recipe(name="Spaghetti Carbonara", 
                 instructions="1. Cook spaghetti until al dente, 2. Cook bacon in a large skillet until crispy. 3. In a bowl, whisk together eggs and parmesan cheese. 4. Add garlic to the bacon and cook for 1 minute. 5. Add spaghetti to the skillet and toss with bacon and garlic. 6. Pour the egg mixture over the spaghetti and toss until the eggs are cooked. Serve hot.")

recipe2 = Recipe(name="Chicken Parmesan", 
                 instructions="1. Preheat oven to 400°F. 2. Coat chicken breast in beaten eggs, then coat in breadcrumbs mixed with parmesan cheese. 3. Place chicken in a baking dish and bake for 20-25 minutes. 4. Spoon marinara sauce over chicken and top with mozzarella cheese. 5. Bake for an additional 10-15 minutes. Serve hot.")
 
recipe3 = Recipe(name="Pilau Beef",
                 instructions="1. Peel the onions and garlic cloves, Wash the beef and add into a pan. Slice in one onion and 2 garlic cloves with the ginger. Add bay leaves, with a cup of water and some salt to taste., 2. Chop the remaining onion and garlic.Wash the rice and repeat until the water runs clear.In another pan, heat the oil under low heat. Add the onions into the pot and cook until the onions start to caramelize and become brown. You should stir the onions with a wooden spoon continuously to prevent burning. 3. Pour in the garlic and the ground spices. The brownish colour comes from the brown spices. Stir for 30 secs. 4.Add the rice into the pot. Pour in the stock and meat chunks. Add more water so there is enough to cook the rice (read the rice pack instructions). Taste for salt and add more if needed. 5. Add the rice into the pot. Pour in the stock and meat chunks. Add more water so there is enough to cook the rice (read the rice pack instructions). Taste for salt and add more if needed. ")

recipe4 = Recipe(name="Chapo", 
                 instructions="1. Add 3 cups of flour in a bowl , 2. Add salt, sugar, 2 tbsp of oil and 1 ½ cups of water in a separate jar/ bowl. Stir until the salt and sugar dissolves.. Keep kneading for 10 minutes and add flour if needed until the dough becomes non-sticky. Add 2-3 tbsp of oil and continue kneading until the oil mixes well and the dough is soft. Cover the dough and leave it for 40 minutes, 3Next, start rolling each of the coil-like shape doughs with the rolling pin to form a circular shape again.")
 

recipe1.ingredients.append(Ingredient(name="spaghetti"))
recipe1.ingredients.append(Ingredient(name="eggs"))
recipe1.ingredients.append(Ingredient(name="bacon"))
recipe1.ingredients.append(Ingredient(name="parmesan cheese"))
recipe1.ingredients.append(Ingredient(name="garlic"))
recipe1.ingredients.append(Ingredient(name="olive oil"))

recipe2.ingredients.append(Ingredient(name="chicken breast"))
recipe2.ingredients.append(Ingredient(name="breadcrumbs"))
recipe2.ingredients.append(Ingredient(name="parmesan cheese"))
recipe2.ingredients.append(Ingredient(name="eggs"))
recipe2.ingredients.append(Ingredient(name="marinara sauce"))
recipe2.ingredients.append(Ingredient(name="mozzarella cheese"))

recipe3.ingredients.append(Ingredient(name="Beef"))
recipe3.ingredients.append(Ingredient(name="Onion"))
recipe3.ingredients.append(Ingredient(name="Garlic"))
recipe3.ingredients.append(Ingredient(name="Ginger"))
recipe3.ingredients.append(Ingredient(name="Bay leaves"))
recipe3.ingredients.append(Ingredient(name="Salt"))


recipe4.ingredients.append(Ingredient(name="flour"))
recipe4.ingredients.append(Ingredient(name="warm water"))
recipe4.ingredients.append(Ingredient(name=" sugar"))
recipe4.ingredients.append(Ingredient(name="olive oil"))
recipe4.ingredients.append(Ingredient(name="Salt"))

# recipe_book.add_recipe(recipe1)
# recipe_book.add_recipe(recipe2)
# recipe_book.add_recipe(recipe3)
# recipe_book.add_recipe(recipe4)


# Searching for a recipe
query = "Spaghetti Carbonara"
search_result = recipe_book.search_recipe(query)
print("Search result for '{}':".format(query))
print(search_result)

# Adding ingredients
if search_result:
    print("Adding ingredients for '{0}' to grocery list...".format(search_result.name))
    if not recipe_book.check_if_ingredients_added(search_result.id):
        recipe_book.add_to_grocery_list([ingredient.name for ingredient in search_result.ingredients])
        recipe_book.mark_ingredients_as_added(search_result.id)

# Removing ingredient 
if search_result and len(search_result.ingredients) > 2:
    ingredient = search_result.ingredients[2].name
    print("Removing '{}' from grocery list...".format(ingredient))
    recipe_book.remove_from_grocery_list(ingredient)
