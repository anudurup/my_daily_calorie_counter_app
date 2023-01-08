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

def delete_item_from_meal(title,item):
    print(title)
    print(item)
    filepath = fpath + os.sep + title + '.txt'
    lines = open(filepath).readlines()
    for i,line in enumerate(lines):
        if item in line:
            print(i)
            lines.pop(i+1)
            lines.pop(i)
            break
    with open(filepath, 'w') as f:
        f.writelines(lines)

st.title("Add meals per day to track")
dates = os.listdir("daily_trackers")
dates = dates[::-1]
date_selectbox = st.selectbox("Select Date you want to add meal:", options=dates)
day_folder = 'daily_trackers' + os.sep + f'{date_selectbox}'
fpath = "daily_trackers" + os.sep + date_selectbox
functions.create_total_nutrition_details(date_selectbox) 

#Create Breakfast
def add_breakfast_item():
    measures,food_items,calories,proteins,fats,carbohydrates = functions.load_item_calorie_dict()    
    key = breakfast_selectbox.split(':')[0]
    quantity = float(st.session_state["breakfast_quantity"])
    index = food_items.index(key)      
    calorie,measure,protein,fat,carbs = int(calories[index]), measures[index],int(proteins[index]),int(fats[index]),int(carbohydrates[index])        
    fname = day_folder + os.sep + 'breakfast.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["breakfast_item"] = ""
    st.session_state['breakfast_quantity'] = ""

st.subheader("Breakfast:")
if os.path.exists(fpath + os.sep + 'breakfast.txt'):
    fname = fpath + os.sep + 'breakfast.txt'
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    st.write(f"Total Calories: {df['calories'].sum()}, Total Proteins: {df['protein'].sum()}, Total Fats: {df['fats'].sum()}, Total Carbs: {df['carbs'].sum()}" + "\n\n")
    
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
        breakfast_selectbox = st.selectbox(label=f"Pick item which matches \"{breakfast_item}\":",key=f'select_index_{breakfast_item}',options=match_items)
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
    fname = day_folder + os.sep + 'smoothie.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["smoothie_item"] = ""
    st.session_state['smoothie_quantity'] = ""

st.subheader("Smoothie:")
if os.path.exists(fpath + os.sep + 'smoothie.txt'):
    fname = fpath + os.sep + 'smoothie.txt'
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    st.write(f"Total Calories: {df['calories'].sum()}, Total Proteins: {df['protein'].sum()}, Total Fats: {df['fats'].sum()}, Total Carbs: {df['carbs'].sum()}" + "\n\n")
    
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
        smoothie_selectbox = st.selectbox(label=f"Pick item which matches \"{smoothie_item}\":",key=f'select_index_{smoothie_item}',options=match_items)
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
    fname = day_folder + os.sep + 'lunch.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["lunch_item"] = ""
    st.session_state['lunch_quantity'] = ""

st.subheader("Lunch:")
if os.path.exists(fpath + os.sep + 'lunch.txt'):
    fname = fpath + os.sep + 'lunch.txt'
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    st.write(f"Total Calories: {df['calories'].sum()}, Total Proteins: {df['protein'].sum()}, Total Fats: {df['fats'].sum()}, Total Carbs: {df['carbs'].sum()}" + "\n\n")
    
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
        lunch_selectbox = st.selectbox(label=f"Pick item which matches \"{lunch_item}\":",key=f'select_index_{lunch_item}',options=match_items)
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
    fname = day_folder + os.sep + 'snack.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["snack_item"] = ""
    st.session_state['snack_quantity'] = ""

st.subheader("Snack:")
if os.path.exists(fpath + os.sep + 'snack.txt'):
    fname = fpath + os.sep + 'snack.txt'
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    st.write(f"Total Calories: {df['calories'].sum()}, Total Proteins: {df['protein'].sum()}, Total Fats: {df['fats'].sum()}, Total Carbs: {df['carbs'].sum()}" + "\n\n")
    
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
        snack_selectbox = st.selectbox(label=f"Pick item which matches \"{snack_item}\":",key=f'select_index_{snack_item}',options=match_items)
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
    fname = day_folder + os.sep + 'salad.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["salad_item"] = ""
    st.session_state['salad_quantity'] = ""

st.subheader("Salad:")
if os.path.exists(fpath + os.sep + 'salad.txt'):
    fname = fpath + os.sep + 'salad.txt'
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    st.write(f"Total Calories: {df['calories'].sum()}, Total Proteins: {df['protein'].sum()}, Total Fats: {df['fats'].sum()}, Total Carbs: {df['carbs'].sum()}" + "\n\n")
    
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
        salad_selectbox = st.selectbox(label=f"Pick item which matches \"{salad_item}\":",key=f'select_index_{salad_item}',options=match_items)
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
    fname = day_folder + os.sep + 'dinner.txt'
    if not os.path.exists(fname):
        with open(fname, 'x') as f:
            pass

    df = pd.read_csv(fname,sep=',')           
    if (len(measure.split()) > 1):
        measure_quantity = float(quantity) * float(measure.split()[0])
        measure_quantity = str(measure_quantity) + " " + measure.split()[1]
    else:
        measure_quantity = float(quantity) * float(measure)  
    if (key in df['recipe_name'].to_list()):
        df.loc[df['recipe_name']==key] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity] 
    else:
        df.loc[len(df.index)] = [key,measure_quantity,float(calorie)*quantity,float(protein)*quantity,float(fat)*quantity,float(carbs)*quantity]         
    df.to_csv(fname,sep=',',index=False)
    st.session_state["dinner_item"] = ""
    st.session_state['dinner_quantity'] = ""

st.subheader("Dinner:")
if os.path.exists(fpath + os.sep + 'dinner.txt'):
    fname = fpath + os.sep + 'dinner.txt'
    df = pd.read_csv(fname,sep=',')
    for i,recipe_name in enumerate(df['recipe_name'].to_list()):
        checkbox = st.checkbox(recipe_name,key = recipe_name)
        st.write(f"Measure: {df.loc[df['recipe_name']==recipe_name]['measure'].squeeze()},Calories:{df.loc[df['recipe_name']==recipe_name]['calories'].squeeze()},Protein:{df.loc[df['recipe_name']==recipe_name]['protein'].squeeze()},Fats:{df.loc[df['recipe_name']==recipe_name]['fats'].squeeze()},Carbs:{df.loc[df['recipe_name']==recipe_name]['carbs'].squeeze()}")  
        if checkbox:  
            df = df.drop(df.index[df["recipe_name"] == recipe_name])
            df.to_csv(fname,sep=',',index=False)
            del st.session_state[recipe_name]
            st.experimental_rerun()   
    st.write(f"Total Calories: {df['calories'].sum()}, Total Proteins: {df['protein'].sum()}, Total Fats: {df['fats'].sum()}, Total Carbs: {df['carbs'].sum()}" + "\n\n")
    
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
        dinner_selectbox = st.selectbox(label=f"Pick item which matches \"{dinner_item}\":",key=f'select_index_{dinner_item}',options=match_items)
with col2:
    st.text_input(label="Enter dinner quantity:", placeholder="Enter dinner quantity...", key='dinner_quantity')
st.button("Add dinner item", key="add_dinner_item", on_click=add_dinner_item)
if not functions.check_if_item_exists(st.session_state['dinner_item'].lower()):
    st.info("Add single item/meal to the database.")

def get_calorie_deficit():
    bmr = (10 * float(current_weight)) + (6.25 * 155) - (5 * 30) - 161
    total_cals_to_consume_per_day = 1.55 *  bmr
    calorie_deficit = total_cals_to_consume_per_day - total_calories_consumed_today + float(calories_burnt_with_exercise)
    with open(fpath + os.sep + 'calorie_deficit.txt', 'w') as f: 
        f.write("Title:Expected/Max:Current/Consumed Today\n")
        f.write(f"Weight:55:{current_weight}\n")
        f.write(f"Calories burned with exercise:600:{calories_burnt_with_exercise}\n")
        f.write(f"BMR:1207.75:{bmr}\n")
        f.write(f"Calories Consumed:{total_cals_to_consume_per_day}:{total_calories_consumed_today}\n")
        f.write(f"Calorie Deficit:500:{round(calorie_deficit,2)}\n")
        f.write(f"Protein Consumed:{round(total_cals_to_consume_per_day*0.35*0.129598,2)}g:{total_protein_consumed_today}g\n")
        f.write(f"Fats Consumed:{round(total_cals_to_consume_per_day*0.35*0.129598,2)}g:{total_fats_consumed_today}g\n")
        f.write(f"Carbs Consumed:{round(total_cals_to_consume_per_day*0.65*0.129598,2)}g:{total_carbs_consumed_today}g")

st.subheader("Calculate calorie deficit chart for the day")    
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