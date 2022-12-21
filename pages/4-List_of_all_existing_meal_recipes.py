import streamlit as st
import pandas as pd

st.title("List of all existing meals")
st.subheader("Make sure the meals you add match once of these.")
df = pd.read_excel("recipes.xlsx",engine="openpyxl")
recipes = df['food_item'].to_list()
ingredients = df['ingredients'].to_list()
for i,recip in enumerate(recipes):
    st.write(recip)
    st.button("View ingredients", key=recip)
    if st.session_state[recip]:
        st.info(ingredients[i])