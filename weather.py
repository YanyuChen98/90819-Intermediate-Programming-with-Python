# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 17:34:49 2021

@author: Peijun Chen
"""

import json
import requests
import pandas as pd
import datetime
import csv


# Let user type their start date
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

def exercise():
    ws = Tk()
    ws.title("Meal and Exercise Plan Recommendation")
    
    date = simpledialog.askstring("Today's Date", "Please enter today's date (MM-DD)",
                                     parent=ws)
    
    
    # A condition that will get to the correct date format and will loop until correct input
    # We will use the historcial weather to refer the climate condition at that time
    a = 1
    while a == 1:
        try:
            datetime.datetime.strptime(date, '%m-%d')
        # If getting error message, we can let them to revise until the correct one
        except ValueError:
            print('Incorrect data format, should be MM-DD')
            date = input('Please enter today\'s date (MM-DD)')
        # when they get the correct input, end the for loop
        if datetime.datetime.strptime(date, '%m-%d'):
            a = 0
    
    headers = {'Content-Type': 'application/json'}
    # the Historical Weather Data API LINK
    # We assume that the person is in the zipcode of 15213, which is the campus zip code
    url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=35519dfd1a144f5883b162618210410&q=15213&format=json&extra=3&date=2020-'+str(date)
    response = requests.get(url, headers)
    # This is the function to make sure that API could be successfully imported to our data
    if response.status_code == 200:
        data = json.loads(response.content.decode())
    else:
        print('API Error')
    
    # Get the day's climate condition including the temperature and weather
    daydata = data['data']['weather'][0]['hourly'][3]
    # Getting Temperature
    temperature = daydata['tempC']
    temperature = int(temperature)
    # Getting weather data (sunny or rainy)
    weather = daydata['weatherDesc'][0]['value']
    # print('Today the temperature is ', temperature, ' celsius degree')
    # print('Today the weather is ', weather)
    
    
    
    # From here, getting the receipt from a csv file
    with open('recipe_nutrient.csv') as f:
        reader = csv.reader(f)
        receiptdata = list(reader)
        receiptdata = receiptdata[1:]
        # data cleaning
    for line in receiptdata:
        line[-1] = line[-1][:-1]
            # Also need to remove the first column
    
    # Select recommended food via climate conditions
    recommendedfood = []
    for item in receiptdata:
        # According to health experts, cold food/raw food like salads are not recommended in winter
        # 12 celsius degree is the standard for 'cold weather' or 'winter'
        if temperature < 12:
            # if the temperature is less than 12, we don't recommend cold or raw food based on health experts
            if item[2] == 'Cold Desserts' or item[2] =='Frozen Desserts' or item[2] == 'Salads':
                continue
            else:
                recommendedfood.append(item)
        else:
            recommendedfood.append(item)
    
    # change the recommended food to dataframe
    food_df = pd.read_csv('recipe_nutrient.csv')
    recommendedfood_list=[]
    for i in recommendedfood:
        recommendedfood_list.append(i[2])
    
    recommendedfood_df = food_df[food_df['Subcat'].isin(recommendedfood_list)]
    # print(recommendedfood_df)
    
    
    
    
    # read the exercise csv and basic cleaning
    with open('exercise_dataset_adjusted.csv', encoding='UTF-8') as f:
        reader = csv.reader(f)
        exercisedata = list(reader)
        exercisedata = exercisedata[1:]
    
    # get in-door exercise list
    indooractivity = []
    weather_activity = []
    for item in exercisedata:
        # It is to select all in-door activities for rainy/snow days
        if 'cycling' in item[0] or 'Calisthenics' in item[0] or 'Circuit training' in item[0] or\
            'lifting' in item[0] or 'club exercise' in item[0] or 'machine' in item[0] or\
            'aerobics' in item[0] or 'Jazzercise' in item[0] or 'Stretching' in item[0] or\
            'aerobic' in item[0] or 'Ballet' in item[0] or 'dancing' in item[0] or\
            'Bowing' in item[0] or 'Boxing' in item[0] or 'Curling' in item[0] or\
            'Darts' in item[0] or 'Fencing' in item[0] or 'Gymnastics' in item[0] or\
             'Hockey' in item[0] or 'Jai alai' in item[0] or 'Martial arts' in item[0] or\
            'Krav maga training' in item[0] or 'Juggling' in item[0] or 'Racquetball' in item[0] or\
            'racquetball' in item[0] or 'Jumping rope' in item[0] or 'Shuffleboard' in item[0] or\
            'Roller skating' in item[0] or 'Squash' in item[0] or 'tennis' in item[0] or 'Tennis' in item[0] or\
            'Trampoline' in item[0] or 'Wrestling' in item[0] or 'Wallerball' in item[0] or 'Carrying' in item[0] or\
            'downstair' in item[0] or 'Pushing a wheelchair' in item[0] or 'General housework' in item[0] or\
            'Painting' in item[0] or 'Sit, playing with animals' in item[0] or 'General cleaning' in item[0] or\
            'dusting' in item[0]:
                indooractivity.append(item)
        else:
            continue
    
    # Convert the recommended exercise to dataframe
    
    exercisedata_df = pd.read_csv('exercise_dataset_adjusted.csv', encoding = 'utf-8')
    indooractivity_list=[]
    for i in indooractivity:
        indooractivity_list.append(i[0])
        
    # Change the unit from kg to lb, make our data consistent
    indooractivity_df = exercisedata_df[exercisedata_df['Activity, Exercise or Sport (1 hour)'].isin(indooractivity_list)]
    
    indooractivity_df.insert(6, 'Calories / lb', (indooractivity_df['130 lb']/130).to_numpy()) 
    # print(indooractivity_df)
    
    weather_activity = pd.DataFrame()
    
    # apply the term for in-door activity
    if 'rain' in weather or 'drizzle' in weather or 'snow' in weather:
        weather_activity = indooractivity_df
        weather_activity.reset_index(drop=True)
        return weather_activity, temperature, date
    else:
        weather_activity = exercisedata_df
        weather_activity.reset_index(drop=True)
        return weather_activity, temperature, date

