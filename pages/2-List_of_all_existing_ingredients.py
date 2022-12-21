import streamlit as st
import pandas as pd

st.title("List of all existing ingredients")
st.subheader("Make sure the ingredients you add match once of these.")
df = pd.read_excel("item_calorie_dict.xlsx",engine="openpyxl")
ingredients = df['food_item'].to_list()
measures = df["measure"].to_list()
calories = df["calories"].to_list()
for i,ingr in enumerate(ingredients):
    st.write(f'{ingr} : quantity - {measures[i]} calories - {calories[i]}')