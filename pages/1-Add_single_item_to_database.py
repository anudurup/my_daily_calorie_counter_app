import streamlit as st
import functions
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="1-Add_single_item_to_database.py")
def add_item_to_dictionary():        
        item = st.session_state['food_item'].lower()
        fname = 'item_calorie_dict.csv'
        df = pd.read_csv(fname)   
        st.write("Enter all the values")
        measure = st.session_state["measure"]    
        calories = st.session_state["calories"]    
        protein = st.session_state["protein"]   
        fats = st.session_state["fats"]        
        carbs = st.session_state["carbs"]
        update_flag = 0
        if item in df['food_item'].values:
            update_flag = 1
            df.loc[df['food_item']==item]  = [item,measure,calories,protein,fats,carbs]
        else:
            df.loc[len(df.index)] = [item,measure,calories,protein,fats,carbs]
        df.to_csv('item_calorie_dict.csv',index=False)
        if update_flag:
            st.info(f"{item} exists, so updating")
        else:
            st.info(f"Added {item} to database")
        update_recipes_based_on_item(item)
        clear_items()

def add_meal_to_dictionary(recipe,no_of_servings):        
    f = open('new_recipe.txt')
    lines = f.readlines()
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
    
    calorie_dict_file = 'item_calorie_dict.csv'
    calorie_dict_dataframe = pd.read_csv(calorie_dict_file)
    recipes_excel = 'recipes.csv'
    recipes_excel_dataframe = pd.read_csv(recipes_excel)
    ingredient_string = ""
    for k,v in ingre_dict.items():
        if not ('total' in k) and not ('no_of_servings' == k):
            ingredient_string += f"{k.rstrip()}: {v.rstrip()},"
    ingredient_string = ingredient_string.rstrip(',')

    if create_meal == 1 and update_meal == 0:
        calorie_dict_dataframe.loc[len(calorie_dict_dataframe.index)] = [recipe_name, '1 serving', total_cals, total_protein, total_fats, total_carbs]
        calorie_dict_dataframe.to_csv('item_calorie_dict.csv',index=False)

        recipes_excel_dataframe.loc[len(recipes_excel_dataframe.index)] = [recipe_name, ingredient_string, no_of_servings, total_cals, total_protein, total_fats, total_carbs]
        recipes_excel_dataframe.to_csv('recipes.csv',index=False)
    elif create_meal == 0 and update_meal == 1:
        calorie_dict_dataframe.loc[calorie_dict_dataframe['food_item'] == recipe] = [recipe_name, '1 serving', total_cals, total_protein, total_fats, total_carbs]
        calorie_dict_dataframe.to_csv('item_calorie_dict.csv',index=False)

        recipes_excel_dataframe.loc[recipes_excel_dataframe['food_item'] == recipe] = [recipe_name, ingredient_string, no_of_servings, total_cals, total_protein, total_fats, total_carbs]
        recipes_excel_dataframe.to_csv('recipes.csv',index=False)

def update_recipes_based_on_item(item):
    df = pd.read_csv("recipes.csv")
    item_dict = pd.read_csv("item_calorie_dict.csv")
    for recipe in df['food_item'].to_list():
        ingredient_string = df.loc[df['food_item'] == recipe]["ingredients"].squeeze()
        if item in ingredient_string:
            print(recipe)
            ingredients = ingredient_string.split(',')           
            with open('new_recipe.txt','w') as f:
                for ingr in ingredients:
                    f.write(f"{ingr.split(':')[0]}: quantity-{ingr.split(':')[1]}\n")
            add_meal_to_dictionary(recipe,df.loc[df['food_item'] == recipe]["no_of_servings"].squeeze())

def clear_items():
    st.session_state["food_item"] = ""
    st.session_state["measure"] = ""
    st.session_state["calories"] = ""
    st.session_state["protein"] = ""
    st.session_state["fats"] = ""
    st.session_state["carbs"] = ""

col1, empty_col,col2 = st.columns([5,1,5])
with col1:
    st.subheader("List of all existing ingredients")
    st.write("Make sure the ingredients you add match once of these.")
    df = pd.read_csv("item_calorie_dict.csv")
    st.dataframe(df.style.set_properties(**{'background-color': 'rgb(144, 238, 144)'}),width=600,height=600)  

with col2:
    st.title("Add single item to database")
    st.text_input(label="Enter food item", key='food_item')
    st.text_input(label="Enter measure", key='measure')
    st.text_input(label="Enter calories", key='calories')
    st.text_input(label="Enter protein", key='protein') 
    st.text_input(label="Enter fats", key='fats')
    st.text_input(label="Enter carbs", key='carbs')
    st.button(label="Add item", on_click=add_item_to_dictionary, key="add_item")