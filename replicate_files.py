import os

mealtime_list = ['breakfast','smoothie','lunch','snack','salad','dinner']
index = 1
for meal in mealtime_list:
    with open("replicate_file.txt",'r') as file:
        with open('copied_items.txt','a') as out_file:
            lines = file.readlines()
            for i,line in enumerate(lines):
                if 'Breakfast' in line:
                    lines[i] = lines[i].replace('Breakfast', meal.capitalize())
                if 'breakfast' in line:
                    lines[i] = lines[i].replace('breakfast', meal)
                if 'col1' in line:
                    lines[i] = lines[i].replace('col1','col'+str(index))
                if 'col2' in line:
                    lines[i] = lines[i].replace('col2','col'+str(index+1))
    
            out_file.writelines(lines)
            out_file.write("\n\n")
    index += 2
            
