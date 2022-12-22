import streamlit as st
import pandas as pd
import functions

st.title("List of all existing meals")
st.subheader("Make sure the meals you add match once of these.")
df = pd.read_excel("recipes.xlsx",engine="openpyxl")
recipes = df['food_item'].to_list()
ingredients = df['ingredients'].to_list()

for i,recip in enumerate(recipes):    
    st.write(recip)
    st.button("View ingredients", key=recip)
    st.button("Remove item from database",key="remove_meal_"+recip)
    if st.session_state[recip]:
        st.info(ingredients[i])
    if st.session_state["remove_meal_"+recip]:
        calorie_dict_dataframe = pd.read_excel("item_calorie_dict.xlsx", engine="openpyxl")    
        calorie_dict_dataframe = calorie_dict_dataframe[calorie_dict_dataframe['food_item'] != recip]
        functions.update_excel_file(calorie_dict_dataframe, "item_calorie_dict.xlsx")
        
        recipes_excel_dataframe = pd.read_excel("recipes.xlsx", engine="openpyxl")
        recipes_excel_dataframe = recipes_excel_dataframe[recipes_excel_dataframe['food_item'] != recip]
        functions.update_excel_file(recipes_excel_dataframe, "recipes.xlsx")
        st.experimental_rerun()