import streamlit as st
import functions
import pandas as pd
import os
import glob
from datetime import datetime

now = datetime.now()
date = now.strftime("%b-%d-%Y")
day_file = 'daily_trackers' + os.sep + f'{date}_tracker.csv'

if not os.path.exists(day_file):
    df = pd.DataFrame([], columns=['mealtype','recipe_name','measure','calories','protein','fats','carbs'])
    df.to_csv(day_file, sep=',',index=False)

st.title("Add meals per day to track")
dates = glob.glob("daily_trackers\*.csv")
dates = dates[::-1]
dates = [os.path.basename(date).replace('.csv','') for date in dates]
date_selectbox = st.selectbox("Select Date you want to add meal:", options=dates)
fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'
if not os.path.exists(fname):
    df = pd.DataFrame([], columns=['mealtype','recipe_name','measure','calories','protein','fats','carbs'])
    df.to_csv(fname, sep=',',index=False)

#Calorie Chart
calorie_chart_file = 'calorie_chart_trackers' + os.sep + os.path.basename(fname) [:-4] + '_calorie_chart.csv'
def get_calorie_deficit():
    date_df = pd.read_csv(fname,sep=',')
    bmr = (10 * float(current_weight)) + (6.25 * 155) - (5 * 30) - 161
    total_cals_to_consume_per_day = 1.55 *  bmr
    calorie_deficit = total_cals_to_consume_per_day - date_df['calories'].sum() + float(st.session_state['exercise'])
    rows = list()
    rows.append(['Weight',55, current_weight])
    rows.append(['Calories burned with exercise','600', st.session_state['exercise']])
    rows.append(['BMR',1207.75,bmr])
    rows.append(['Calories Consumed',total_cals_to_consume_per_day,date_df['calories'].sum()])
    rows.append(['Calorie Deficit',500,round(calorie_deficit,2)])
    rows.append(['Protein Consumed',f"{round(total_cals_to_consume_per_day*0.35*0.129598,2)}g",f"{round(date_df['protein'].sum(),2)}g"])
    rows.append(['Fats Consumed',f"{round(total_cals_to_consume_per_day*0.35*0.129598,2)}g",f"{round(date_df['protein'].sum(),2)}g"])
    rows.append(['Carbs Consumed',f"{round(total_cals_to_consume_per_day*0.65*0.129598,2)}g",f"{round(date_df['protein'].sum(),2)}g"])
    df = pd.DataFrame(rows,columns=['Title','Expected/Max','Current/Consumed Today'])
    df.to_csv(calorie_chart_file,sep=",",index=False)

st.subheader("Calculate calorie deficit chart for the day")    
current_weight = st.text_input("Enter current weight", key="weight")
calories_burnt_with_exercise  = st.text_input("calories_burnt_with_exercise", key="exercise")
st.button("Get calorie deficit for the day", key="calorie_deficit_button",on_click=get_calorie_deficit)
if os.path.exists(calorie_chart_file):
    df = pd.read_csv(calorie_chart_file, sep=",")
    st.dataframe(df.style.set_properties(**{'background-color': 'rgb(173, 216, 230)'}),width=600)

for mealtype in ['breakfast', 'smoothie', 'lunch', 'salad', 'snack', 'dinner']:
    st.subheader(f"{mealtype.title()}:")
    if os.path.exists(fname):    
        df = pd.read_csv(fname,sep=',')
        for i,recipe_name in enumerate(df.loc[df['mealtype'] == mealtype]['recipe_name'].to_list()):
            checkbox = st.checkbox(recipe_name,key = f'{mealtype}_{recipe_name}')
            st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
            if checkbox:  
                df = df.drop(df.index[df["recipe_name"] == recipe_name])
                df.to_csv(fname,sep=',',index=False)
                del st.session_state[f'{mealtype}_{recipe_name}']
                st.experimental_rerun()   
        df2 = df.loc[df['mealtype'] == mealtype]
        st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
        
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(label=f"Add {mealtype} items:", placeholder=f"Enter {mealtype} item...", key=f'{mealtype}_item')
        if st.session_state[f'{mealtype}_item'] != "":  
            meal_item = st.session_state[f"{mealtype}_item"].lower()
            measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
            match_items = list()
            for i,key in enumerate(food_items):
                if meal_item in key:
                    match_items.append(f"{key}:{measures[i]}")
            meal_selectbox = st.selectbox(label=f"Pick item which matches \"{meal_item}\":",key=f'{mealtype}_select_index_{meal_item}',options=match_items)
    with col2:
        st.text_input(label=f"Enter {mealtype} quantity:", placeholder=f"Enter {mealtype} quantity...", key=f'{mealtype}_quantity')
    meal_button = st.button(f"Add {mealtype} item", key=f"add_{mealtype}_item")
    if not functions.check_if_item_exists(st.session_state[f'{mealtype}_item'].lower()):
        st.info("Add single item/meal to the database.")
    if meal_button:
        measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
        key = meal_selectbox.split(':')[0]
        quantity = float(st.session_state[f"{mealtype}_quantity"])
        index = food_items.index(key)      
        calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
        
        if not os.path.exists(fname):
            with open(fname, 'w') as f:
                f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

        df = pd.read_csv(fname,sep=',')           
        if (len(measure.split()) > 1):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)
        if (key in df.loc[df["mealtype"]==mealtype]['recipe_name'].to_list()):
            df.loc[df['recipe_name']==key] = [mealtype,key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
        else:
            df.loc[len(df.index)] = [mealtype,key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
        df.to_csv(fname,sep=',',index=False)
        st.experimental_rerun()

df = pd.read_csv(fname, sep=',')
st.subheader("Total consumed today:")
st.write(f"Total Calories:{round(df['calories'].sum(),2)}, Total Protein:{round(df['protein'].sum(),2)}g, Total Fats:{round(df['fats'].sum(),2)}g, Total Carbs:{round(df['carbs'].sum(),2)}g")  