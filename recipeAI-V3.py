import json
import math

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

with open("recipeV3.json", "r") as json_file:
    recipes = json.load(json_file)

N = int(input("Enter the number of ingredients: "))
ingredients = []
for i in range(N):
    print(f"Enter the ingredient {i+1}: ", end="")
    ingredient = input()
    ingredients.append(ingredient)

def normalize(ingredient, synonyms):
    if ingredient in synonyms:
        return synonyms[ingredient]
    else:
        return ingredient

vocab = sorted({val for k in recipes for val in k['ingredients']})
idx = {w:i for i, w in enumerate(vocab)}

df = [0]*len(idx)
for i in range(len(recipes)):
    ing = set(recipes[i]['ingredients'])
    for v in ing:
        if v in recipes[i]:
            df[idx[v]] += 1

N=len(recipes)
idf = [math.log((N+1)/(dfi+1))+1 for dfi in df]

def weight_vector(ing_list):
    v = [0.0]*len(idx)
    for ing in idx:
        if ing in ing_list:
            v[idx[ing]] = 1.0 * idf[idx[ing]]
    return v

def cosine(u, i):
    dot = sum(x*y for x, y in zip(u, i))
    mu = math.sqrt(sum(x*x for x in u))
    mi = math.sqrt(sum(x*x for x in i))
    return 0.0 if 0 in [mu, mi] else (dot / (mu * mi))

user_vec = weight_vector(ingredients)

def score_recipe(recipe):
    r_vec = weight_vector(recipe["ingredients"])
    sim = cosine(user_vec, r_vec)
    missing = [m for m in recipe["ingredients"] if m not in ingredients]
    extra = [e for e in ingredients if e not in recipe["ingredients"]]
    recipe_len = len(recipe["ingredients"])
    return {
        "name": recipe["name"],
        "similiarity": sim,
        "missing": missing,
        "output": recipe["output"],
        "extra": extra,
        "recipe_len": recipe_len
    }
scored = [score_recipe(r) for r in recipes]
scored.sort(
    key=lambda x: (-x["similiarity"], len(x["missing"]), x["recipe_len"])
)

THRESHOLD = 0.1
top = [t for t in scored if t["similiarity"]>=THRESHOLD][:5]

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





















