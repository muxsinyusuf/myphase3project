from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

recipe_ingredient_association = Table(
    'recipe_ingredient_association',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredient.id')),
    Column('quantity', Integer)
)

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructions = Column(String)
    ingredients = relationship(
        "Ingredient",
        secondary=recipe_ingredient_association,
        backref="recipes",
        overlaps="recipes"
    )

    def __repr__(self):
        return self.name

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String)

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

    def add_recipe(self, recipe_name, instructions, ingredient_names):
        ingredients = [Ingredient(name=name) for name in ingredient_names]
        recipe = Recipe(name=recipe_name, instructions=instructions, ingredients=ingredients)
        self.session.add(recipe)
        self.session.commit()

    def add_ingredients(self, ingredient_names):
        for ingredient_name in ingredient_names:
            ingredient = Ingredient(name=ingredient_name)
            self.session.add(ingredient)
            self.session.commit()

    def search_recipe(self, query):
        return self.session.query(Recipe).filter(Recipe.name.ilike('%' + query + '%')).first()

if __name__ == "__main__":
    engine = create_engine('sqlite:///recipe_book.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    recipe_book = RecipeBook(session)
    
    while True:
        print("Menu:")
        print("1. Add Recipe")
        print("2. Add Ingredients")
        print("3. Search Recipe")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            recipe_name = input("Enter recipe name: ")
            instructions = input("Enter instructions: ")
            ingredient_names = input("Enter ingredients (comma-separated): ").split(',')
            recipe_book.add_recipe(recipe_name, instructions, ingredient_names)
            print("Recipe added successfully.")

        elif choice == "2":
            ingredient_names = input("Enter ingredient names (comma-separated): ").split(',')
            recipe_book.add_ingredients(ingredient_names)
            print("Ingredients added successfully.")

        elif choice == "3":
            query = input("Enter recipe name to search: ")
            search_result = recipe_book.search_recipe(query)
            if search_result:
                print("Search result for '{}':".format(query))
                print('yes we have {search_result}')
            else:
                print("No recipes found for '{}'".format(query))

        elif choice == "4":
            break

    session.close()
