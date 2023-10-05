from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Recipe, Ingredient, RecipeBook

fake = Faker()

recipe = [
    "Spaghetti Carbonara",
    "Chicken Parmesan",
    "Pilau Beef",
    "Chapo"
]

structions = [
    "1.  Cook spaghetti until al dente, 2. Cook bacon in a large skillet until crispy. 3. In a bowl, whisk together eggs and parmesan cheese. 4. Add garlic to the bacon and cook for 1 minute. 5. Add spaghetti to the skillet and toss with bacon and garlic. 6. Pour the egg mixture over the spaghetti and toss until the eggs are cooked. Serve hot.",
    "1. Preheat oven to 400°F. 2. Coat chicken breast in beaten eggs, then coat in breadcrumbs mixed with parmesan cheese. 3. Place chicken in a baking dish and bake for 20-25 minutes. 4. Spoon marinara sauce over chicken and top with mozzarella cheese. 5. Bake for an additional 10-15 minutes. Serve hot.",
    "1.Peel the onions and garlic cloves, Wash the beef and add into a pan. Slice in one onion and 2 garlic cloves with the ginger. Add bay leaves, with a cup of water and some salt to taste., 2. Chop the remaining onion and garlic.Wash the rice and repeat until the water runs clear.In another pan, heat the oil under low heat. Add the onions into the pot and cook until the onions start to caramelize and become brown. You should stir the onions with a wooden spoon continuously to prevent burning. 3. Pour in the garlic and the ground spices. The brownish colour comes from the brown spices. Stir for 30 secs. 4.Add the rice into the pot. Pour in the stock and meat chunks. Add more water so there is enough to cook the rice (read the rice pack instructions). Taste for salt and add more if needed. 5. Add the rice into the pot. Pour in the stock and meat chunks. Add more water so there is enough to cook the rice (read the rice pack instructions). Taste for salt and add more if needed.",
    "1.Add 3 cups of flour in a bowl , 2. Add salt, sugar, 2 tbsp of oil and 1 ½ cups of water in a separate jar/ bowl. Stir until the salt and sugar dissolves.. Keep kneading for 10 minutes and add flour if needed until the dough becomes non-sticky. Add 2-3 tbsp of oil and continue kneading until the oil mixes well and the dough is soft. Cover the dough and leave it for 40 minutes, 3Next, start rolling each of the coil-like shape doughs with the rolling pin to form a circular shape again."
]

ingredients = [
    "spaghetti", "eggs", "bacon", "parmesan cheese", "garlic",
    "chicken breast", "breadcrumbs", "marinara sauce", "mozzarella cheese",
    "beef", "onion", "ginger", "bay leaves", "salt",
    "flour", "warm water", "sugar", "olive oil", "salt"
]

def generate_random_recipe_with_ingredients():
    recipe_name = fake.random.choice(recipe)
    instructions = fake.random.choice(instructions)

    num_ingredients = random.randint(5)
    ingredients = []
    for _ in range(num_ingredients):
        ingredient_name = fake.random.choice(ingredients)
        ingredient = Ingredient(name=ingredient_name)
        ingredients.append(ingredient)

    return Recipe(name=recipe_name, instructions=instructions, ingredients=ingredients)

if __name__ == "__main__":
    engine = create_engine('sqlite:///recipe_book.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    recipe_book = RecipeBook()
    
    for _ in range(2): 
        recipe = generate_random_recipe_with_ingredients()
        recipe_book.add_recipe(recipe)

    print("Recipes in the database:")
    for recipe in session.query(Recipe).all():
        print(f"Recipe: {recipe.name}, Ingredients: {[ingredient.name for ingredient in recipe.ingredients]}")

    session.commit()
