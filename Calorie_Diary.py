import streamlit as st
import os
import pandas as pd

st.set_page_config(layout="wide", page_title="Calorie_Diary.py")
st.title("Calorie Counter")
st.subheader("This is my calorie counter app")
st.write("This app is to help diet and exercise tracking.")

st.image("food_dairy.jpg",width=200)

def create_tracker():
    date = st.session_state["date_added"]
    if not os.path.exists("daily_trackers" + os.sep + date + "_tracker.csv"):
        if not os.path.exists("daily_trackers" + os.sep + date + "_tracker.csv"):
            df = pd.DataFrame([], columns=['mealtype','recipe_name','measure','calories','protein','fats','carbs'])
            df.to_csv("daily_trackers" + os.sep + date + "_tracker.csv", sep=',',index=False)
        st.info("Created the tracker for date- " + date)        
    else:
        st.info("Tracker already exists for this date")
    st.session_state["date_added"] = ""

with st.form("Create new tracker"):
    st.write("Existing daily trackers:")
    dates = os.listdir("daily_trackers")
    dates = dates[::-1]
    date_selectbox = st.selectbox("Select Date you want to add meal:", options=dates)
    st.write("Do you want to add a older date to the trackers?")
    st.text_input("Enter date in the format Jan-01-2023", key="date_added")
    st.form_submit_button("Add tracker for this date", on_click=create_tracker)