import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

synonyms = {
    # Eggs
    "eggs": "egg",
    "hen egg": "egg",
    "chicken egg": "egg",
    "boiled egg": "egg",
    "fried egg": "egg",

    # Bread
    "breads": "bread",
    "loaf": "bread",
    "loaves": "bread",
    "toast": "bread",
    "sandwich bread": "bread",
    "bun": "bread",
    "roll": "bread",

    # Butter
    "butters": "butter",
    "margarine": "butter",
    "ghee": "butter",
    "clarified butter": "butter",
    "spread": "butter",

    # Oil
    "oils": "oil",
    "vegetable oil": "oil",
    "sunflower oil": "oil",
    "olive oil": "oil",
    "canola oil": "oil",
    "mustard oil": "oil",

    # Milk
    "milks": "milk",
    "whole milk": "milk",
    "skimmed milk": "milk",
    "cream": "milk",

    # Cheese
    "cheeses": "cheese",
    "mozzarella": "cheese",
    "cheddar": "cheese",
    "parmesan": "cheese",

    # Tomato
    "tomatoes": "tomato",
    "cherry tomato": "tomato",
    "roma tomato": "tomato",

    # Onion
    "onions": "onion",
    "red onion": "onion",
    "white onion": "onion",
    "shallot": "onion",

    # Potato
    "potatoes": "potato",
    "sweet potato": "potato",
    "yam": "potato",

    # Chicken
    "chickens": "chicken",
    "chicken breast": "chicken",
    "chicken thigh": "chicken",
    "hen": "chicken",

    # Rice
    "rices": "rice",
    "basmati": "rice",
    "jasmine rice": "rice",
    "brown rice": "rice"
}

def normalize(ing):
    ing = ing.lower().strip()
    return synonyms.get(ing, ing)

with open("recipeV3.json", "r") as json_file:
    recipes = json.load(json_file)

for i in range(len(recipes)):
    recipes[i]["ingredients"] = [normalize(ing) for ing in recipes[i]["ingredients"]]

recipe_text = [" ".join(recipes[i]["ingredients"]) for i in range(len(recipes))]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(recipe_text)

N = int(input("Enter the number of ingredients: "))
ingredients = []
for i in range(N):
    print(f"Enter the ingredient {i+1}: ", end="")
    ingredient = input()
    ingredients.append(ingredient)

for i in range(len(ingredients)):
    ingredients = [normalize(ing) for ing in ingredients]

user_text = [" ".join(ingredients)]
user_vec = vectorizer.transform(user_text)

sims = cosine_similarity(user_vec, X)[0]

sorted = []

for i in range(len(recipes)):
    missing = [m for m in recipes[i]["ingredients"] if m not in ingredients]
    sorted.append(
        {
            "name": recipes[i]['name'],
            "sim": sims[i],
            "output": recipes[i]['output'],
            "missing": missing
        }
    )

sorted.sort(
    key = lambda x: [-x['sim']]
)

top = sorted[:3]

if not top:
    print("No recipe for this, try something new")
else:
    for i in range(len(top)):
        if top[i]['missing'] is not None:
            print(f"{i+1}You can make {top[i]['name']}. But you are missing {top[i]['missing']}")
            print(f"To make it just {top[i]['output']}\n")
        else:
            print(f"{i+1}.You can make {top[i]['name']}.")
            print(f"To make it just {top[i]['output']}\n")