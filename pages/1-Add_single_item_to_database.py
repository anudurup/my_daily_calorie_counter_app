import streamlit as st
import functions
import pandas as pd

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
        clear_items()

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