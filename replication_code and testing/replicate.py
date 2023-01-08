mealtype = ['breakfast','smoothie','lunch','snack','salad','dinner']
out_f = open('replication_code and testing/replicated.txt','a')
for meal in mealtype:
    f = open('replication_code and testing/replicate.txt')
    lines = f.readlines()
    for i,line in enumerate(lines):
        if 'Breakfast' in line:
            lines[i] = lines[i].replace('Breakfast',meal.title())
        elif 'breakfast' in line:
            lines[i] = lines[i].replace('breakfast',meal)
    out_f.writelines(lines)
    out_f.write("\n\n")
    f.close()
out_f.close()
