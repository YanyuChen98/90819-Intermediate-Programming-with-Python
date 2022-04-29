# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:03:28 2021

@author: Xintong Zheng
"""
# Graphs
# Graph1: Distribution of Calories in the Recipe Pool 
import pandas as pd
import matplotlib.pyplot as plt
data_recipe = pd.read_csv('recipe_nutrient.csv')
#plt.title('Scatter:Calories')
#plt.scatter(data_recipe['Recipe'], data_recipe['Calories'], marker='*', color='blue')
plt.title('Histogram: Calories')
plt.xlabel('Calories')
plt.ylabel('Recipe_Count')
plt.hist(data_recipe['Calories'],bins=25)

# Graph2: Anticipated Weight Losing Process
# Ask users if they would like to see the graph of anticipated weight losing process. If they answer YES, display it.
show_WLP = input('Type Y if you hope to see your anticipated Weight Lossing Process\
                 / Type N if you do NOT hope to see your anticipated Weight Lossing Process:')
if show_WLP == 'Y':
    plt.title('Weight Losing Process')
    plt.xlabel('loss_time')
    plt.ylabel('# weight_loss')
    plt.plot(loss_time, weight_loss,color='blue'，linewidth=3)   #variable names referring to Olivia's

#shopping list
import json
with open ('cooking_detail_dict.json','r') as f:
    t = json.load(f)
    print(f)

# weekyly_recipe needs revise- refer to Yanyu's code
weekly_recipe=['Asian Bean and Rice Rolls','Bagel Chips']

# To get lists of ingredients and cooking directions from web scraped recipe data which is a dict of dicts
ingred = [] #ingredients
direc = [] #directions
for i in range(0,len(weekly_recipe)):
    j = t.get(weekly_recipe[i])
    ingred.append(j['ingredients'])
    direc.append(j['directions'])
# """print optional"""
    # print(j)
    # print(ingred)
    # print(direc)

# Ingredients needed for dishes we recommend
# below is how I format the ingredients for each recipe
for i in ingred:
    for j in i:
        k = j.split(',')
        print(k[0])
    print('', sep='\n')

df_1 = pd.DataFrame(ingred[:2], index=weekly_recipe) # index change needed
print(df_1)  #df of ingredients, including recipe name and ingredients

# Ask users if they would like to see the cooking directions. If they answer YES, display directions as a dataframe
show_direc = input('Type Y if you hope to refer to cooking directions/ Type N if you do NOT hope to refer to cooking directions:')
if show_direc == 'Y':
    df_2 = pd.DataFrame(direc[:2], index=weekly_recipe)  # index change needed
    print(df_2)  #df of directions