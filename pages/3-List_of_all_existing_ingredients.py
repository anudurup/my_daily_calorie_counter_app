import streamlit as st
import pandas as pd

st.title("List of all existing ingredients")
st.subheader("Make sure the ingredients you add match once of these.")
df = pd.read_excel("item_calorie_dict.xlsx",engine="openpyxl")
ingredients = df['food_item'].to_list()
measures = df["measure"].to_list()
calories = df["calories"].to_list()
df = pd.read_excel("item_calorie_dict.xlsx", engine="openpyxl")
df2 = df.filter(['food_item','measure','calories'], axis=1)
st.dataframe(df2,width=400,height=600)