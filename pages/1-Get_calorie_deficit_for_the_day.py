import streamlit as st
import functions
import pandas as pd
import os
from datetime import datetime
import functions

now = datetime.now()
date = now.strftime("%b-%d-%Y")
day = functions.get_dayname()
day_folder = 'daily_trackers' + os.sep + f'{date}_tracker'

if not os.path.exists(day_folder):
    os.mkdir(day_folder)

st.title("View meals per day")

dates = os.listdir("daily_trackers")
dates = dates[::-1]
date_selectbox = st.selectbox("Select Date you want to add meal:", options=dates)
functions.create_total_nutrition_details(date_selectbox) 

fpath = "daily_trackers" + os.sep + date_selectbox

def get_calorie_deficit():
    bmr = (10 * float(current_weight)) + (6.25 * 155) - (5 * 30) - 161
    total_cals_to_consume_per_day = 1.55 *  bmr
    calorie_deficit = total_cals_to_consume_per_day - total_calories_consumed_today + float(calories_burnt_with_exercise)
    with open(fpath + os.sep + 'calorie_deficit.txt', 'w') as f: 
        f.write("Title:Expected/Max:Current/Consumed Today\n")
        f.write(f"Weight:65:{current_weight}\n")
        f.write(f"Calories burned with exercise:300:{calories_burnt_with_exercise}\n")
        f.write(f"BMR:1307.75:{bmr}\n")
        f.write(f"Calories Consumed:{total_cals_to_consume_per_day}:{total_calories_consumed_today}\n")
        f.write(f"Calorie Deficit:500:{round(calorie_deficit,2)}\n")
        f.write(f"Protein Consumed:{round(total_cals_to_consume_per_day*0.35*0.129598,2)}g:{total_protein_consumed_today}g\n")
        f.write(f"Fats Consumed:{round(total_cals_to_consume_per_day*0.35*0.129598,2)}g:{total_fats_consumed_today}g\n")
        f.write(f"Carbs Consumed:{round(total_cals_to_consume_per_day*0.65*0.129598,2)}g:{total_carbs_consumed_today}g")
        
current_weight = st.text_input("Enter current weight", key="weight")
calories_burnt_with_exercise  = st.text_input("calories_burnt_with_exercise", key="exercise")
st.button("Get calorie deficit for the day", key="calorie_deficit_button",on_click=get_calorie_deficit)

total_calories_consumed_today = 0
if os.path.exists(fpath + os.sep + 'total_nutrition_today.txt'):
    fname = open(fpath + os.sep + 'total_nutrition_today.txt')
    lines = fname.readlines()
    fname.close()
    prev_line = ""
    for i,line in enumerate(lines):
        if "Total consumed today" in prev_line:
            total_calories_consumed_today = float(line.split(',')[0].split(':')[1]) 
            total_protein_consumed_today = float(line.split(',')[1].split(':')[1]) 
            total_fats_consumed_today = float(line.split(',')[2].split(':')[1]) 
            total_carbs_consumed_today = float(line.split(',')[3].split(':')[1])        
        prev_line = line   

if os.path.exists(fpath + os.sep + 'calorie_deficit.txt'):
    df = pd.read_csv(fpath + os.sep + 'calorie_deficit.txt', sep=":")
    st.dataframe(df.style.set_properties(**{'background-color': 'rgb(173, 216, 230)'}),width=600)