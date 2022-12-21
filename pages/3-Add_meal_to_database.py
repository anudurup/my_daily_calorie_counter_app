import streamlit as st
import functions
import pandas as pd
import json

def add_meal_to_dictionary():        
        f = open('new_recipe.txt')
        lines = f.readlines()
        recipe = st.session_state['meal']
        ingredients = dict()
        for line in lines:
            if line.strip() != '':
                ingredient = line.split(':')[0]
                ingredients[ingredient] = line.split('-')[1]
        recipe_json_file = open('recipes.json')
        available_recipes = json.load(recipe_json_file)
        recipe_json_file.close()
        if recipe in available_recipes.keys():
            update_meal = 1
            create_meal = 0
        else:
            update_meal = 0
            create_meal = 1
        no_of_servings = float(st.session_state["no_of_servings"])
        print(st.session_state["no_of_servings"])
        for k, v in ingredients.items():
            ingredients[k] = v.rstrip()

        recipe_dict = dict()
        recipe_dict[recipe] = ingredients
        recipe_name,ingre_dict,total_cals,total_protein,total_fats,total_carbs = functions.get_nutrition_facts(recipe_dict,no_of_servings)

        f = open('recipes.json')
        recipes_json = json.load(f)
        f.close()
        ingre_dict['total_cals'] = total_cals
        ingre_dict['total_protein'] = total_protein
        ingre_dict['total_fats'] = total_fats
        ingre_dict['total_carbs'] = total_carbs
        ingre_dict['no_of_servings'] = no_of_servings
        recipes_json[recipe_name] = ingre_dict
        functions.write_to_recipes_json_file(recipes_json)
        
        calorie_dict_file = 'item_calorie_dict.xlsx'
        calorie_dict_dataframe = pd.read_excel(calorie_dict_file,engine = 'openpyxl')
        recipes_excel = 'recipes.xlsx'
        recipes_excel_dataframe = pd.read_excel(recipes_excel,engine = 'openpyxl')
        ingredient_string = ""
        for k,v in ingre_dict.items():
            if not ('total' in k) and not ('no_of_servings' == k):
                ingredient_string += f"{k.rstrip()}: {v.rstrip()},"
        ingredient_string = ingredient_string.rstrip(',')

        if create_meal == 1 and update_meal == 0:
            calorie_dict_dataframe_intermediate = {'food_item':recipe_name,'measure':'1 serving','calories':total_cals,"protein":total_protein,"fats":total_fats,"carbohydrates":total_carbs}
            calorie_dict_dataframe = calorie_dict_dataframe.append(calorie_dict_dataframe_intermediate, ignore_index = True)

            recipes_excel_dataframe_intermediate = {'food_item':recipe_name,'ingredients':ingredient_string,'no_of_servings':no_of_servings,"calories":total_cals,"protein":total_protein,"fats":total_fats,"carbohydrates":total_carbs}
            recipes_excel_dataframe = recipes_excel_dataframe.append(recipes_excel_dataframe_intermediate, ignore_index = True)
        elif create_meal == 0 and update_meal == 1:
            calorie_dict_index = calorie_dict_dataframe.index[calorie_dict_dataframe['food_item']==recipe]
            calorie_dict_dataframe.iloc[calorie_dict_index] = [recipe,'1 serving',total_cals,total_protein,total_fats,total_carbs]
            
            recipes_excel_index = recipes_excel_dataframe.index[recipes_excel_dataframe['food_item']==recipe]
            recipes_excel_dataframe.iloc[recipes_excel_index] = [recipe,ingredient_string,no_of_servings,total_cals,total_protein,total_fats,total_carbs]
            
        functions.update_excel_file(calorie_dict_dataframe,calorie_dict_file)
        functions.update_excel_file(recipes_excel_dataframe,recipes_excel)
        st.info("Added meal to database")
        st.session_state["meal"] = ""
        st.session_state["no_of_servings"] = ""
        st.session_state["new_ingredient"] = ""
        st.session_state["new_quantity"] = ""

def clear_ingredients():
    ingredients = list()
    functions.write_todos(ingredients, 'new_recipe.txt') 

def add_ingr():
    ingredients = functions.get_todos('new_recipe.txt')
    new_ingredient = selectbox
    new_quantity = st.session_state["new_quantity"]
    ingredients.append(f"{new_ingredient}: quantity-{new_quantity}\n")
    functions.write_todos(ingredients, 'new_recipe.txt') 
    del st.session_state["selected_ingredient"]

def update_ingredients():
    recipe_name = st.session_state['meal']
    if not (recipe_name == '') and functions.check_if_item_exists(recipe_name):
        df = pd.read_excel('recipes.xlsx', engine="openpyxl")
        for row, value in df.iterrows():
            if value["food_item"] == recipe_name:
                ingredient_string = value["ingredients"]
                break
        ingredients = ingredient_string.split(",")
        with open('new_recipe.txt','w') as f:
            for ingr in ingredients:
                f.write(f"{ingr.split(':')[0]}: quantity-{ingr.split(':')[1]}\n")
    else:
        ingredients = list()
        with open('new_recipe.txt','w') as f:
            f.writelines(ingredients)

recipe_name = st.text_input(label="meal_name", placeholder="meal_name...",
            key='meal',on_change=update_ingredients)

st.text_input(label="no_of_servings", placeholder="no_of_servings...",
            key='no_of_servings')
col1, col2 = st.columns([2,2])
with col1:
    st.text_input(label="add ingredient", placeholder="Add ingredient...",
            key='new_ingredient')
with col2:
    st.text_input(label="add quantity", placeholder="Add quantity for the given ingredient...",
            key='new_quantity')
ingredient = st.session_state["new_ingredient"]
if not functions.check_if_item_exists(ingredient):
    st.info(f"Add single item: {ingredient} to the database")

if st.session_state["new_ingredient"] != "":   
    measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
    match_items = list()
    for key in food_items:
        if ingredient in key:
            match_items.append(key)
    selectbox = st.selectbox(label=f"Pick item which matches \"{ingredient}\":",key=f'select_index_{ingredient}',options=match_items)
    st.button("Add ingredient", key="selected_ingredient", on_click=add_ingr)

ingredients = functions.get_todos('new_recipe.txt')
for index, ingr in enumerate(ingredients):
    checkbox = st.checkbox(ingr, key=ingr)
    if checkbox:  # If we check the checkbox it will be True
        ingredients.pop(index)
        functions.write_todos(ingredients, 'new_recipe.txt')
        del st.session_state[ingr]
        st.experimental_rerun() # This clears the task once it is checked.

col3, col4 = st.columns([0.5,2])
with col3:
    st.button(label="Add meal", on_click=add_meal_to_dictionary, key="add_meal")
with col4: 
    st.button("Clear all ingredients", key="clear_ingredients", on_click=clear_ingredients)