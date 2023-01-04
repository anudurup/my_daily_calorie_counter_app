import streamlit as st
import pandas as pd
import functions

def remove_meal_function():    
    if st.session_state["remove_meal_index"] != "":
        remove_index = int(st.session_state["remove_meal_index"])
        calorie_dict_dataframe = pd.read_excel("item_calorie_dict.xlsx", engine="openpyxl")    
        calorie_dict_dataframe.drop(calorie_dict_dataframe.index[remove_index], inplace=True)
        functions.update_excel_file(calorie_dict_dataframe, "item_calorie_dict.xlsx")
        
        recipes_excel_dataframe = pd.read_excel("recipes.xlsx", engine="openpyxl")
        recipes_excel_dataframe.drop(recipes_excel_dataframe.index[remove_index], inplace=True)
        functions.update_excel_file(recipes_excel_dataframe, "recipes.xlsx")
        st.session_state["remove_meal_index"] = ""

st.title("List of all existing meals")
st.subheader("Make sure the meals you add match once of these.")
st.write("Click the checkbox to remove a recipe from this list.")
df = pd.read_excel("recipes.xlsx", engine="openpyxl")
df2 = df.filter(['food_item','no_of_servings','ingredients'], axis=1)
st.dataframe(df2)

st.text_input("Enter index of item to remove",key="remove_meal_index")
st.button("Remove meal", key="remove_meal",on_click=remove_meal_function)