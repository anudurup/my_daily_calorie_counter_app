import streamlit as st
import functions
import pandas as pd
import os
from datetime import datetime

now = datetime.now()
date = now.strftime("%b-%d-%Y")
day = functions.get_dayname()
day_folder = 'daily_trackers' + os.sep + f'{date}_tracker'

if not os.path.exists(day_folder):
    os.mkdir(day_folder)

st.title("Calorie Counter")
st.subheader("This is my calorie counter app")
st.write("This app is to help diet and exercise tracking.")

st.subheader("View meals per day")
dates = os.listdir("daily_trackers")
date_selectbox = st.selectbox("Select Date you want to add meal:", options=dates)
fpath = "daily_trackers" + os.sep + date_selectbox

def get_calorie_deficit():
    bmr = (10 * float(current_weight)) + (6.25 * 155) - (5 * 29) - 161
    total_cals_to_consume_per_day = 1.55 *  bmr
    calorie_deficit = total_cals_to_consume_per_day - total_calories + float(calories_burnt_with_exercise)
    with open(fpath + os.sep + 'calorie_deficit.txt', 'w') as f: 
        f.write(f"Current Weight: {current_weight}\n")
        f.write(f"Calories burned with exercise: {calories_burnt_with_exercise}\n")
        f.write(f"BMR:  {bmr}\n")
        f.write(f"Total cals to consume per day:  {total_cals_to_consume_per_day}\n")
        f.write(f"Calorie Deficit: {calorie_deficit}")

current_weight = st.text_input("Enter current weight", key="weight")
calories_burnt_with_exercise  = st.text_input("calories_burnt_with_exercise", key="exercise")
st.button("Get calorie deficit for the day", key="calorie_deficit_button",on_click=get_calorie_deficit)

total_calories = 0
prev_line = ""
if os.path.exists(fpath + os.sep + 'total_nutrition_today.txt'):
    fname = open(fpath + os.sep + 'total_nutrition_today.txt')
    lines = fname.readlines()
    for line in lines:
        if not ':' in line:
            st.subheader(line)
        else:
            st.write(line) 
        if "Total consumed today" in prev_line:
            total_calories = float(line.split(',')[0].split(':')[1])
        prev_line = line  

if os.path.exists(fpath + os.sep + 'calorie_deficit.txt'):
    for line in open(fpath + os.sep + 'calorie_deficit.txt').readlines():
        st.write(line) 