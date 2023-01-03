import pandas as pd
import os

def change_names_to_lower_case(f = "item_calorie_dict.xlsx"):
    df = pd.read_excel(f, engine="openpyxl")
    for i,value in enumerate(df['food_item'].to_list()):
        df['food_item'][i] = value.lower()
    df.to_excel(f, engine="openpyxl",index=False)

change_names_to_lower_case('recipes.xlsx')