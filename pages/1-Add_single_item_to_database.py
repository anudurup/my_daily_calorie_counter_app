import streamlit as st
import functions
import pandas as pd

def add_item_to_dictionary():        
        item = st.session_state['food_item']
        fname = 'item_calorie_dict.xlsx'
        df = pd.read_excel(fname,engine = 'openpyxl')   
        st.write("Enter all the values")
        measure = st.session_state["measure"]    
        calories = st.session_state["calories"]    
        protein = st.session_state["protein"]   
        fats = st.session_state["fats"]        
        carbs = st.session_state["carbs"]
        if item in df['food_item'].values:
            print(f"{item} exists, so updating")
            df = pd.read_excel(fname,engine = 'openpyxl')
            index = df.index[df['food_item']==item]
            df.iloc[index] = [item,measure,calories,protein,fats,carbs]
        else:
            df2 = {'food_item':item,'measure':measure,'calories':calories,"protein":protein,"fats":fats,"carbohydrates":carbs}
            df = pd.read_excel(fname,engine = 'openpyxl')
            df = df.append(df2, ignore_index = True)
        functions.update_excel_file(df,fname)
        st.info("Added item to database")

def clear_items():
    st.session_state["food_item"] = ""
    st.session_state["measure"] = ""
    st.session_state["calories"] = ""
    st.session_state["protein"] = ""
    st.session_state["fats"] = ""
    st.session_state["carbs"] = ""

st.title("Add single item to database")
st.text_input(label="Enter food item", key='food_item')
st.text_input(label="Enter measure", key='measure')
st.text_input(label="Enter calories", key='calories')
st.text_input(label="Enter protein", key='protein') 
st.text_input(label="Enter fats", key='fats')
st.text_input(label="Enter carbs", key='carbs')
col1,col2 = st.columns([0.5,3])
with col1: 
    st.button(label="Add item", on_click=add_item_to_dictionary, key="add_item")
with col2:
    st.button(label="Clear items", on_click=clear_items, key="clear_items")