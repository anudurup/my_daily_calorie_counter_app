import streamlit as st
import pandas as pd
import json
import functions

st.set_page_config(layout="wide", page_title='3- View all ingredients and meals.py')
st.subheader("List of all existing ingredients")
st.write("Make sure the ingredients you add match once of these.")
df = pd.read_csv("item_calorie_dict.csv")
ingredients = df['food_item'].to_list()
measures = df["measure"].to_list()
calories = df["calories"].to_list()
df = pd.read_csv("item_calorie_dict.csv")
st.dataframe(df.style.set_properties(**{'background-color': 'rgb(144, 238, 144)'}),width=600,height=600)  

st.subheader("List of all existing meals")
st.write("Make sure the meals you add match once of these.")
st.write("Click the checkbox to remove a recipe from this list.")
df = pd.read_csv("recipes.csv")
st.dataframe(df.style.set_properties(**{'background-color': 'rgb(173, 216, 230)'}),width=1500,height=500)

col1,col2 = st.columns (2)
def remove_meal_function():    
    if st.session_state["remove_meal_index"] != "":
        remove_index = int(st.session_state["remove_meal_index"])
        calorie_dict_dataframe = pd.read_csv("item_calorie_dict.csv")    
        calorie_dict_dataframe.drop(calorie_dict_dataframe.index[remove_index], inplace=True)
        calorie_dict_dataframe.to_csv("item_calorie_dict.csv")
        
        recipes_excel_dataframe = pd.read_csv("recipes.csv")
        recipes_excel_dataframe.drop(recipes_excel_dataframe.index[remove_index], inplace=True)
        recipes_excel_dataframe.to_csv("recipes.csv")
        st.session_state["remove_meal_index"] = ""
with col2:
    st.subheader("Remove meal from database")
    st.text_input("Enter index of item to remove",key="remove_meal_index")
    st.button("Remove meal",key="remove_meal",on_click=remove_meal_function)

def update_recipe_name():
    current_name = st.session_state["current_meal"]
    new_name = st.session_state["changed_meal"]
    df = pd.read_csv("recipes.csv")
    index = df.index[df['food_item']==current_name]
    df.at[index,'food_item'] = new_name
    df.to_csv("recipes.csv",index=False)
    df = pd.read_csv("item_calorie_dict.csv")
    index = df.index[df['food_item']==current_name]
    df.at[index,'food_item'] = new_name
    df.to_csv("item_calorie_dict.csv",index=False)
    f = open("recipes.json")
    recipes = json.load(f)
    recipes[new_name] = recipes[current_name]
    del recipes[current_name]
    f.close()
    import os
    file = 'recipes.json'
    if (os.path.exists(file)):
        os.remove(file)
    json_object = json.dumps(recipes, indent=4)
    with open("recipes.json", "w") as outfile:
        outfile.write(json_object)
    functions.update_trackers_for_recipe_name_change(current_name,new_name)
    st.session_state["current_meal"] = ""
    st.session_state["changed_meal"] = ""

with col1:
    st.subheader("Change name of a meal")
    current_recipe_name = st.text_input(label="current meal name", placeholder="meal_name...",
                key='current_meal')
    changed_recipe_name = st.text_input(label="changed meal name", placeholder="meal_name...",
                key='changed_meal')
    change_recipe = st.button(label="change recipe name",key="change_recipe_name",on_click=update_recipe_name)