from datetime import date
from datetime import datetime
import streamlit as st
import math
import pandas as pd
import os
import json

def get_todos(filepath='todo.txt'):
    with open(filepath, 'r') as file_local:
        lines = file_local.readlines()
        for line in lines:
            if (line.strip() == ''):
                del line
        todos_local = lines
    return todos_local

def write_todos(todos_local,filepath='todo.txt'):
    with open(filepath, 'w') as file_local:
        file_local.writelines(todos_local)

def create_weekly_tracker_pages():
    pass

def get_dayname():
    dt = datetime.now()
    day_name = dt.strftime('%A')
    return day_name

def load_item_calorie_dict():
        cd = pd.read_excel('item_calorie_dict.xlsx',engine = 'openpyxl')
        measures = list(cd['measure'])
        food_items = list(cd['food_item'])
        calories = list(cd['calories'])
        protein = list(cd['protein'])
        fats = list(cd['fats'])
        carbohydrates = list(cd['carbohydrates'])
        return measures,food_items,calories,protein,fats,carbohydrates

def update_excel_file(df,fname):
        with pd.ExcelWriter(fname, engine="openpyxl", mode="a") as writer:
            workBook = writer.book
            try:
                workBook.remove(workBook["Sheet1"])
            except:
                print("Worksheet does not exist")
            finally:
                df.to_excel(writer, sheet_name="Sheet1",index=False)
                writer.save()

def get_calories_per_food_item(ingredient):
        measures,food_items,calories,protein,fats,carbohydrates = load_item_calorie_dict()
        key = ingredient
        index = food_items.index(key)         
        return int(calories[index]), measures[index],int(protein[index]),int(fats[index]),int(carbohydrates[index]) 

def get_nutrition_facts(recipe,no_of_servings):       
    for recipe_name,recip in recipe.items():
        ingre_dict = dict()
        total_cals = 0
        total_protein = 0
        total_fats = 0
        total_carbs = 0
        for ingredient,quantity in recip.items():
            if len(quantity.split()) < 1:
                quantity = float(quantity)
            else:
                quantity = float(quantity.split()[0])
            calories,measure,protein,fats,carbohydrates = get_calories_per_food_item(ingredient)
            measure = str(measure)
            measure_list = measure.split(" ")
            if len(measure_list) > 1:
                measure = measure.split(" ").pop()
            else:
                measure = ""
            ingre_dict[ingredient] = str(quantity) + " " + measure
            total_cals += calories * quantity
            total_protein += protein * quantity
            total_fats += fats * quantity
            total_carbs += carbohydrates * quantity
    total_cals /= no_of_servings
    total_protein /= no_of_servings
    total_fats /= no_of_servings
    total_carbs /= no_of_servings
    return recipe_name,ingre_dict,total_cals,total_protein,total_fats,total_carbs

def check_if_item_exists(ingredient):
    measures,food_items,calories,protein,fats,carbohydrates = load_item_calorie_dict()
    
    found_flag = 0
    for item in food_items:
        if ingredient in item:
            found_flag = 1
            break
    return found_flag

def write_to_recipes_json_file(recipes):
        file = 'recipes.json'
        if (os.path.exists(file)):
            os.remove(file)
        json_object = json.dumps(recipes, indent=4)
        with open("recipes.json", "w") as outfile:
            outfile.write(json_object)

def create_total_nutrition_details(date_selectbox):
    fpath = "daily_trackers" + os.sep + date_selectbox
    mealtime_list = ['breakfast','smoothie','lunch','snack','salad','dinner']
    total_calories = 0
    total_proteins = 0
    total_fats = 0
    total_carbs = 0
    with open(fpath + os.sep + "total_nutrition_today.txt", "w") as f:
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
