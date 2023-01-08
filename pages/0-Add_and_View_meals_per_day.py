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

#Create Breakfast
def add_breakfast_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = breakfast_selectbox.split(':')[0]
    quantity = float(st.session_state["breakfast_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
    fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'      
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = ['breakfast',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = ['breakfast',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["breakfast_item"] = ""
    st.session_state['breakfast_quantity'] = ""

st.subheader("Breakfast:")
if os.path.exists(fname):    
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df.loc[df['mealtype'] == 'breakfast']['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    df2 = df.loc[df['mealtype'] == 'breakfast']
    st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
    
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Add breakfast items:", placeholder="Enter breakfast item...", key='breakfast_item')
    if st.session_state['breakfast_item'] != "":  
        breakfast_item = st.session_state["breakfast_item"].lower()
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for i,key in enumerate(food_items):
            if breakfast_item in key:
                match_items.append(f"{key}:{measures[i]}")
        breakfast_selectbox = st.selectbox(label=f"Pick item which matches \"{breakfast_item}\":",key=f'breakfast_select_index_{breakfast_item}',options=match_items)
with col2:
    st.text_input(label="Enter breakfast quantity:", placeholder="Enter breakfast quantity...", key='breakfast_quantity')
st.button("Add breakfast item", key="add_breakfast_item", on_click=add_breakfast_item)
if not functions.check_if_item_exists(st.session_state['breakfast_item'].lower()):
    st.info("Add single item/meal to the database.")

#Create Smoothie
def add_smoothie_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = smoothie_selectbox.split(':')[0]
    quantity = float(st.session_state["smoothie_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
    fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'      
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = ['smoothie',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = ['smoothie',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["smoothie_item"] = ""
    st.session_state['smoothie_quantity'] = ""

st.subheader("Smoothie:")
if os.path.exists(fname):    
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df.loc[df['mealtype'] == 'smoothie']['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    df2 = df.loc[df['mealtype'] == 'smoothie']
    st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
    
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Add smoothie items:", placeholder="Enter smoothie item...", key='smoothie_item')
    if st.session_state['smoothie_item'] != "":  
        smoothie_item = st.session_state["smoothie_item"].lower()
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for i,key in enumerate(food_items):
            if smoothie_item in key:
                match_items.append(f"{key}:{measures[i]}")
        smoothie_selectbox = st.selectbox(label=f"Pick item which matches \"{smoothie_item}\":",key=f'smoothie_select_index_{smoothie_item}',options=match_items)
with col2:
    st.text_input(label="Enter smoothie quantity:", placeholder="Enter smoothie quantity...", key='smoothie_quantity')
st.button("Add smoothie item", key="add_smoothie_item", on_click=add_smoothie_item)
if not functions.check_if_item_exists(st.session_state['smoothie_item'].lower()):
    st.info("Add single item/meal to the database.")

#Create Lunch
def add_lunch_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = lunch_selectbox.split(':')[0]
    quantity = float(st.session_state["lunch_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
    fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'      
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = ['lunch',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = ['lunch',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["lunch_item"] = ""
    st.session_state['lunch_quantity'] = ""

st.subheader("Lunch:")
if os.path.exists(fname):    
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df.loc[df['mealtype'] == 'lunch']['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    df2 = df.loc[df['mealtype'] == 'lunch']
    st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
    
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Add lunch items:", placeholder="Enter lunch item...", key='lunch_item')
    if st.session_state['lunch_item'] != "":  
        lunch_item = st.session_state["lunch_item"].lower()
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for i,key in enumerate(food_items):
            if lunch_item in key:
                match_items.append(f"{key}:{measures[i]}")
        lunch_selectbox = st.selectbox(label=f"Pick item which matches \"{lunch_item}\":",key=f'lunch_select_index_{lunch_item}',options=match_items)
with col2:
    st.text_input(label="Enter lunch quantity:", placeholder="Enter lunch quantity...", key='lunch_quantity')
st.button("Add lunch item", key="add_lunch_item", on_click=add_lunch_item)
if not functions.check_if_item_exists(st.session_state['lunch_item'].lower()):
    st.info("Add single item/meal to the database.")

#Create Snack
def add_snack_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = snack_selectbox.split(':')[0]
    quantity = float(st.session_state["snack_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
    fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'      
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = ['snack',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = ['snack',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["snack_item"] = ""
    st.session_state['snack_quantity'] = ""

st.subheader("Snack:")
if os.path.exists(fname):    
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df.loc[df['mealtype'] == 'snack']['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    df2 = df.loc[df['mealtype'] == 'snack']
    st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
    
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Add snack items:", placeholder="Enter snack item...", key='snack_item')
    if st.session_state['snack_item'] != "":  
        snack_item = st.session_state["snack_item"].lower()
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for i,key in enumerate(food_items):
            if snack_item in key:
                match_items.append(f"{key}:{measures[i]}")
        snack_selectbox = st.selectbox(label=f"Pick item which matches \"{snack_item}\":",key=f'snack_select_index_{snack_item}',options=match_items)
with col2:
    st.text_input(label="Enter snack quantity:", placeholder="Enter snack quantity...", key='snack_quantity')
st.button("Add snack item", key="add_snack_item", on_click=add_snack_item)
if not functions.check_if_item_exists(st.session_state['snack_item'].lower()):
    st.info("Add single item/meal to the database.")

#Create Salad
def add_salad_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = salad_selectbox.split(':')[0]
    quantity = float(st.session_state["salad_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
    fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'      
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = ['salad',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = ['salad',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["salad_item"] = ""
    st.session_state['salad_quantity'] = ""

st.subheader("Salad:")
if os.path.exists(fname):    
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df.loc[df['mealtype'] == 'salad']['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    df2 = df.loc[df['mealtype'] == 'salad']
    st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
    
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Add salad items:", placeholder="Enter salad item...", key='salad_item')
    if st.session_state['salad_item'] != "":  
        salad_item = st.session_state["salad_item"].lower()
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for i,key in enumerate(food_items):
            if salad_item in key:
                match_items.append(f"{key}:{measures[i]}")
        salad_selectbox = st.selectbox(label=f"Pick item which matches \"{salad_item}\":",key=f'salad_select_index_{salad_item}',options=match_items)
with col2:
    st.text_input(label="Enter salad quantity:", placeholder="Enter salad quantity...", key='salad_quantity')
st.button("Add salad item", key="add_salad_item", on_click=add_salad_item)
if not functions.check_if_item_exists(st.session_state['salad_item'].lower()):
    st.info("Add single item/meal to the database.")

#Create Dinner
def add_dinner_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = dinner_selectbox.split(':')[0]
    quantity = float(st.session_state["dinner_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])  
    fname = 'daily_trackers' + os.sep + date_selectbox + '.csv'      
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write('mealtype,recipe_name,measure,calories,protein,fats,carbs\n')

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = ['dinner',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = ['dinner',key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["dinner_item"] = ""
    st.session_state['dinner_quantity'] = ""

st.subheader("Dinner:")
if os.path.exists(fname):    
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df.loc[df['mealtype'] == 'dinner']['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    df2 = df.loc[df['mealtype'] == 'dinner']
    st.write(f"Total Calories: {df2['calories'].sum()}, Total Proteins: {df2['protein'].sum()}, Total Fats: {df2['fats'].sum()}, Total Carbs: {df2['carbs'].sum()}")
    
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Add dinner items:", placeholder="Enter dinner item...", key='dinner_item')
    if st.session_state['dinner_item'] != "":  
        dinner_item = st.session_state["dinner_item"].lower()
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for i,key in enumerate(food_items):
            if dinner_item in key:
                match_items.append(f"{key}:{measures[i]}")
        dinner_selectbox = st.selectbox(label=f"Pick item which matches \"{dinner_item}\":",key=f'dinner_select_index_{dinner_item}',options=match_items)
with col2:
    st.text_input(label="Enter dinner quantity:", placeholder="Enter dinner quantity...", key='dinner_quantity')
st.button("Add dinner item", key="add_dinner_item", on_click=add_dinner_item)
if not functions.check_if_item_exists(st.session_state['dinner_item'].lower()):
    st.info("Add single item/meal to the database.")

fname = 'daily_trackers' + os.sep + date_selectbox + '.csv' 
df = pd.read_csv(fname, sep=',')
st.subheader("Total consumed today:")
st.write(f"Total Calories:{round(df['calories'].sum(),2)}, Total Protein:{round(df['protein'].sum(),2)}g, Total Fats:{round(df['fats'].sum(),2)}g, Total Carbs:{round(df['carbs'].sum(),2)}g")  