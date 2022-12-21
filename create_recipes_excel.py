import pandas as pd
import json

fname = open('recipes.json')
recipes = json.load(fname)
rows = list()
for recipe_name, ingredients in recipes.items():
    row = list()
    row.append(recipe_name)
    ingredient_string = ""
    for k,v in ingredients.items():
        if not ('total' in k) and not ('no_of_servings' == k):
            ingredient_string += f"{k.rstrip()}: {v.rstrip()},"
    ingredient_string = ingredient_string.rstrip(',')
    row += [ingredient_string, ingredients['no_of_servings'],ingredients['total_cals'],ingredients['total_protein'],ingredients['total_fats'],ingredients['total_carbs']]
    rows.append(row)

df = pd.DataFrame(rows,columns=["food_item","ingredients","no_of_servings","calories","protein","fats","carbohydrates"])
df.to_excel("recipes.xlsx", engine="openpyxl", index=False)