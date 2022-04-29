from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt


#BMR Info - The following inquires about user's information neeeded to compute their basal metabolism rate
ws = Tk()
ws.title("Meal and Exercise Plan Recommendation")

gender = simpledialog.askstring("Basic Info", "Please enter your gender (M/F)",
                                parent=ws)

age = simpledialog.askinteger("Basic Info", "What is your age?",
                                 parent=ws,
                                 minvalue=0, maxvalue=100)

if age < 18:
    print("Please leave this program as it is not designed for minors" )
    
weight = simpledialog.askinteger("Basic Info", "Please enter your current weight in lbs",
                                 parent=ws,
                                 maxvalue=800)

height = simpledialog.askinteger("Basic Info", "Please enter your height in inches",
                                 parent=ws,
                                 maxvalue=100)

if gender == "M":
    BMR = 66.47 + (6.24 * weight) + (12.7 * height ) - (6.755 * age)
    print('Your basal metabolism rate is {:.0f} calories/day'.format(BMR))
if gender == "F":
    BMR = 655.1 + (4.35 * weight) + (4.7 * height ) - (4.7 * age)
    print('Your basal metabolism rate is {:.0f} calories/day'.format(BMR))

#Weight Loss Plan - The following inquires about user's weight loss goals.
#The information received is used to calculate user's daily calorie burn. The estimated calories burned required to lose 1 pound of fat is 3,500 
weight_loss = simpledialog.askinteger("Weight Goals", "Please enter the amount of weight you would like to lose in lbs",
                                 parent=ws)

loss_time = simpledialog.askinteger("Weight Goals", "Please enter the number of days you wish to lose the weight in",
                                 parent=ws)

daily_calorie_burn = (weight_loss * 3500) / loss_time
print ('Your daily calorie burn should be {:.0f} cal'.format(daily_calorie_burn))

# The baseline_food variable sets the baseline calorie intake at 1,800 calories/day.
# We are assuming that this allowance should be sufficient to build a non-restrictive meal plan for our users.
baseline_food = 1800

# The baseline_exercise variable sets the baseline calories burned through exercise at 500 calories/day.
# We are assuming that this basline should be adequate to build a light exercie plan for our users.

baseline_exercise = 500
plan_preference = simpledialog.askstring("Plan Pereference", "Type 'Y' if you prefer to have a more restrictive diet/ Type 'N' if you prefer to have a more rigorous work out plan",
                                parent=ws)
if plan_preference == 'Y':
    food_calories = baseline_exercise + BMR - daily_calorie_burn
    exercise_calories = baseline_exercise
    print('Your daily calories intake will be {:.0f} cal'.format(food_calories))
    print('Your daily calories burnt through exercising will be {:.0f} cal'.format(exercise_calories))

if plan_preference == 'N':
    food_calories = baseline_food
    exercise_calories = daily_calorie_burn + baseline_food - BMR
    print('Your daily calories intake will be {:.0f} cal'.format(food_calories))
    print('Your daily calories burnt through exercising will be {:.0f} cal'.format(exercise_calories))

from recomm_plan import recomm

from recomm_plan import recomm_e

#shopping list
with open ('cooking_detail_dict.json','r') as f:
    t = json.load(f)

daily_recipe = recomm(food_calories)

# To get lists of ingredients and cooking directions from web scraped recipe data which is a dict of dicts
ingred = [] #ingredients
direc = [] #directions
for i in range(0,len(daily_recipe)):
    j = t.get(daily_recipe[i])
    ingred.append(j['ingredients'])
    direc.append(j['directions'])


# Ingredients needed for dishes we recommend
# below is how I format the ingredients for each recipe

print('\n')
exercise_list = recomm_e(exercise_calories,weight)
for i in exercise_list:
    print(i)
print('\n')

count = 0
for i in ingred:
    print(daily_recipe[count])
    count += 1
    for j in i:
        k = j.split(',')
        print(k[0])
    print('', sep='\n')
    
#df of ingredients, including recipe name and ingredients

# Ask users if they would like to see the cooking directions. If they answer YES, display directions as a dataframe
df_1 = pd.DataFrame(ingred[0:len(daily_recipe)], index=daily_recipe) # index c=hange needed
#print(df_1)  #df of ingredients, including recipe name and ingredients

# Ask users if they would like to see the cooking directions. If they answer YES, display directions as a dataframe
show_direc = simpledialog.askstring("Cooking Directions", "Type Y if you hope to refer to cooking directions / Type N if you do NOT hope to refer to cooking directions: ",
                                parent=ws)
if show_direc == 'Y':
    df_2 = pd.DataFrame(direc[0:len(daily_recipe)], index=daily_recipe) 
    print(df_2) 

# Graph1: Distribution of Calories in the Recipe Pool 

data_recipe = pd.read_csv('recipe_nutrient.csv')
#plt.title('Scatter:Calories')
#plt.scatter(data_recipe['Recipe'], data_recipe['Calories'], marker='*', color='blue')
plt.title('Histogram: Calories')
plt.xlabel('Calories')
plt.ylabel('Recipe_Count')
plt.hist(data_recipe['Calories'],bins=25)

# Graph2: Anticipated Weight Losing Process
# Ask users if they would like to see the graph of anticipated weight losing process. If they answer YES, display it.

show_WLP = simpledialog.askstring("Weight Loss Process","Type Y if you hope to see your anticipated weight loss progress / Type N if you do NOT hope to see your anticipated weight loss process: ",
                                  parent=ws)
if show_WLP == 'Y':
    plt.title('Weight Loss Process')
    plt.xlabel('loss time')
    plt.ylabel('weight loss')
    plt.plot(loss_time, weight_loss,color='blue', linewidth=3)   
    plt.show()
    
ws.destroy()    
    
    