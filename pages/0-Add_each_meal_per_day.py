import streamlit as st
import functions
import pandas as pd
import os
from datetime import datetime

st.title("Add meals per day to track")
dates = os.listdir("daily_trackers")
date_selectbox = st.selectbox("Select Date you want to add meal:", options=dates)
day_folder = 'daily_trackers' + os.sep + f'{date_selectbox}'

#Create Breakfast
def add_breakfast_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()
    key = breakfast_selectbox
    index = food_items.index(key)         
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index]) 
    fname = day_folder + os.sep + 'breakfast.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass
    with open(fname, 'a') as f:
        f.write(key + " :\n")
        quantity = float(st.session_state["breakfast_quantity"])
        if not isinstance(measure,int):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)           
        f.write(f"Calories: {float(calorie)*quantity}, Measure: {measure_quantity}, Protein: {float(protein)*quantity}, Fats: {float(fat)*quantity}, Carbs: {float(carbs)*quantity}\n")
    
st.subheader("Enter breakfast items:")
col1, col2 = st.columns(2)
with col1:
    st.text_input(label="Enter breakfast item:", placeholder="Enter breakfast item...", key='breakfast_item')
    if st.session_state['breakfast_item'] != "":   
        breakfast_item = st.session_state["breakfast_item"]
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for key in food_items:
            if breakfast_item in key:
                match_items.append(key)
        breakfast_selectbox = st.selectbox(label=f"Pick item which matches \"{breakfast_item}\":",key=f'select_index_{breakfast_item}',options=match_items)
with col2:
    st.text_input(label="Enter breakfast quantity:", placeholder="Enter breakfast quantity...", key='breakfast_quantity')
st.button("Add breakfast item", key="add_breakfast_item", on_click=add_breakfast_item)
if not functions.check_if_item_exists(st.session_state['breakfast_item']):
    st.info("Add single item/meal to the database.")

#Create Smoothie
def add_smoothie_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()
    key = smoothie_selectbox
    index = food_items.index(key)         
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index]) 
    fname = day_folder + os.sep + 'smoothie.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass
    with open(fname, 'a') as f:
        f.write(key + " :\n")
        quantity = float(st.session_state["smoothie_quantity"])
        if not isinstance(measure,int):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)           
        f.write(f"Calories: {float(calorie)*quantity}, Measure: {measure_quantity}, Protein: {float(protein)*quantity}, Fats: {float(fat)*quantity}, Carbs: {float(carbs)*quantity}\n")

st.subheader("Enter smoothie items:")
col3, col4 = st.columns(2)
with col3:
    st.text_input(label="Enter smoothie item:", placeholder="Enter smoothie item...", key='smoothie_item')
    if st.session_state['smoothie_item'] != "":   
        smoothie_item = st.session_state["smoothie_item"]
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for key in food_items:
            if smoothie_item in key:
                match_items.append(key)
        smoothie_selectbox = st.selectbox(label=f"Pick item which matches \"{smoothie_item}\":",key=f'select_index_{smoothie_item}',options=match_items)
with col4:
    st.text_input(label="Enter smoothie quantity:", placeholder="Enter smoothie quantity...", key='smoothie_quantity')
st.button("Add smoothie item", key="add_smoothie_item", on_click=add_smoothie_item)
if not functions.check_if_item_exists(st.session_state['smoothie_item']):
    st.info("Add single item/meal to the database.")

#Create Lunch
def add_lunch_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()
    key = lunch_selectbox
    index = food_items.index(key)         
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index]) 
    fname = day_folder + os.sep + 'lunch.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass
    with open(fname, 'a') as f:
        f.write(key + " :\n")
        quantity = float(st.session_state["lunch_quantity"])
        if not isinstance(measure,int):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)           
        f.write(f"Calories: {float(calorie)*quantity}, Measure: {measure_quantity}, Protein: {float(protein)*quantity}, Fats: {float(fat)*quantity}, Carbs: {float(carbs)*quantity}\n")

st.subheader("Enter lunch items:")
col5, col6 = st.columns(2)
with col5:
    st.text_input(label="Enter lunch item:", placeholder="Enter lunch item...", key='lunch_item')
    if st.session_state['lunch_item'] != "":   
        lunch_item = st.session_state["lunch_item"]
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for key in food_items:
            if lunch_item in key:
                match_items.append(key)
        lunch_selectbox = st.selectbox(label=f"Pick item which matches \"{lunch_item}\":",key=f'select_index_{lunch_item}',options=match_items)
with col6:
    st.text_input(label="Enter lunch quantity:", placeholder="Enter lunch quantity...", key='lunch_quantity')
st.button("Add lunch item", key="add_lunch_item", on_click=add_lunch_item)
if not functions.check_if_item_exists(st.session_state['lunch_item']):
    st.info("Add single item/meal to the database.")

#Create Snack
def add_snack_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()
    key = snack_selectbox
    index = food_items.index(key)         
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index]) 
    fname = day_folder + os.sep + 'snack.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass
    with open(fname, 'a') as f:
        f.write(key + " :\n")
        quantity = float(st.session_state["snack_quantity"])
        if not isinstance(measure,int):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)           
        f.write(f"Calories: {float(calorie)*quantity}, Measure: {measure_quantity}, Protein: {float(protein)*quantity}, Fats: {float(fat)*quantity}, Carbs: {float(carbs)*quantity}\n")

st.subheader("Enter snack items:")
col7, col8 = st.columns(2)
with col7:
    st.text_input(label="Enter snack item:", placeholder="Enter snack item...", key='snack_item')
    if st.session_state['snack_item'] != "":   
        snack_item = st.session_state["snack_item"]
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for key in food_items:
            if snack_item in key:
                match_items.append(key)
        snack_selectbox = st.selectbox(label=f"Pick item which matches \"{snack_item}\":",key=f'select_index_{snack_item}',options=match_items)
with col8:
    st.text_input(label="Enter snack quantity:", placeholder="Enter snack quantity...", key='snack_quantity')
st.button("Add snack item", key="add_snack_item", on_click=add_snack_item)
if not functions.check_if_item_exists(st.session_state['snack_item']):
    st.info("Add single item/meal to the database.")

#Create Salad
def add_salad_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()
    key = salad_selectbox
    index = food_items.index(key)         
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index]) 
    fname = day_folder + os.sep + 'salad.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass
    with open(fname, 'a') as f:
        f.write(key + " :\n")
        quantity = float(st.session_state["salad_quantity"])
        if not isinstance(measure,int):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)           
        f.write(f"Calories: {float(calorie)*quantity}, Measure: {measure_quantity}, Protein: {float(protein)*quantity}, Fats: {float(fat)*quantity}, Carbs: {float(carbs)*quantity}\n")

st.subheader("Enter salad items:")
col9, col10 = st.columns(2)
with col9:
    st.text_input(label="Enter salad item:", placeholder="Enter salad item...", key='salad_item')
    if st.session_state['salad_item'] != "":   
        salad_item = st.session_state["salad_item"]
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for key in food_items:
            if salad_item in key:
                match_items.append(key)
        salad_selectbox = st.selectbox(label=f"Pick item which matches \"{salad_item}\":",key=f'select_index_{salad_item}',options=match_items)
with col10:
    st.text_input(label="Enter salad quantity:", placeholder="Enter salad quantity...", key='salad_quantity')
st.button("Add salad item", key="add_salad_item", on_click=add_salad_item)
if not functions.check_if_item_exists(st.session_state['salad_item']):
    st.info("Add single item/meal to the database.")

#Create Dinner
def add_dinner_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()
    key = dinner_selectbox
    index = food_items.index(key)         
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index]) 
    fname = day_folder + os.sep + 'dinner.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass
    with open(fname, 'a') as f:
        f.write(key + " :\n")
        quantity = float(st.session_state["dinner_quantity"])
        if not isinstance(measure,int):
            measure_quantity = float(quantity) * float(measure.split()[0])
            measure_quantity = str(measure_quantity) + " " + measure.split()[1]
        else:
            measure_quantity = float(quantity) * float(measure)           
        f.write(f"Calories: {float(calorie)*quantity}, Measure: {measure_quantity}, Protein: {float(protein)*quantity}, Fats: {float(fat)*quantity}, Carbs: {float(carbs)*quantity}\n")

st.subheader("Enter dinner items:")
col11, col12 = st.columns(2)
with col11:
    st.text_input(label="Enter dinner item:", placeholder="Enter dinner item...", key='dinner_item')
    if st.session_state['dinner_item'] != "":   
        dinner_item = st.session_state["dinner_item"]
        measures,food_items,calories,protein,fats,carbohydrates = functions.load_item_calorie_dict()
        match_items = list()
        for key in food_items:
            if dinner_item in key:
                match_items.append(key)
        dinner_selectbox = st.selectbox(label=f"Pick item which matches \"{dinner_item}\":",key=f'select_index_{dinner_item}',options=match_items)
with col12:
    st.text_input(label="Enter dinner quantity:", placeholder="Enter dinner quantity...", key='dinner_quantity')
st.button("Add dinner item", key="add_dinner_item", on_click=add_dinner_item)
if not functions.check_if_item_exists(st.session_state['dinner_item']):
    st.info("Add single item/meal to the database.")

fpath = "daily_trackers" + os.sep + date_selectbox
mealtime_list = ['breakfast','smoothie','lunch','snack','salad','dinner']
total_calories = 0
total_proteins = 0
total_fats = 0
total_carbs = 0
f = open(fpath + os.sep + "total_nutrition_today.txt", "w")
for i,mealtype in enumerate(mealtime_list):
    f.write(mealtype.capitalize() + "\n")
    if os.path.exists(fpath + os.sep + mealtype + '.txt'):
        fname = open(fpath + os.sep + mealtype + '.txt')
        lines = fname.readlines()
        recipe_list = list()
        calories = list()
        proteins = list()
        fats = list()
        carbs = list()

        for line in lines:
            f.write(line)
            if not ('Calories' in line) and not ('' == line):
                recipe_list.append(line.split(":")[0].rstrip())
            if 'Calories' in line:
                values = line.split(',')
                calories.append(float(values[0].split(':')[1]))
                proteins.append(float(values[2].split(':')[1]))
                fats.append(float(values[3].split(':')[1]))
                carbs.append(float(values[4].split(':')[1]))
        f.write(f"Total Calories: {sum(calories)}, Total Proteins: {sum(proteins)}, Total Fats: {sum(fats)}, Total Carbs: {sum(carbs)}" + "\n\n")
        total_calories += sum(calories)
        total_proteins += sum(proteins)
        total_fats += sum(fats)
        total_carbs += sum(carbs)
f.write("Total consumed today" + "\n")
f.write(f"Total Calories: {total_calories}, Total Proteins: {total_proteins}, Total Fats: {total_fats}, Total Carbs: {total_carbs}" + "\n\n")      
f.close()         