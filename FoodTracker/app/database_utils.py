from pymongo import MongoClient
import time as t
from datetime import date

TEAM_NAME = 'FoodTrackData'

def GetCollection():
    return MongoClient()[TEAM_NAME].articles

# This function inserts another section of 
def InsertMeal(single_sub):

    # Get the day and current time
    today = date.today()

    coll = GetCollection();
    existing = coll.find_one({"UserName" : single_sub["UserName"]});
    
    # This checks to see if the username is already in the database
    if existing is not None:
        print "The user %s is registered" % (single_sub["UserName"])
        # Now we need to append to this existing user the meal that we just had
        meal = dict(
            Meal=single_sub["Meal"],
            Price=float(single_sub["Price"]),
            Time=t.time(),
            UserName=single_sub["UserName"],
            Year=today.year,
            Month=today.month,
            Day=today.day
        )

        # Inster anotehr meal for this database entry
        coll.insert(meal)
    
    
    # This creates a new section of the database with a new username,
    # and creates the meal object
    else:
        print "Adding new user: ", single_sub["UserName"]
        meal = dict(
            Meal=single_sub["Meal"],
            Price=float(single_sub["Price"]),
            Time=t.time(),
            UserName=single_sub["UserName"],
            Year=today.year,
            Month=today.month,
            Day=today.day
        )

        # Add a meal to the database
        coll.insert(meal)
        
    return True


# This gets all of the meals from a person
def GetMeals(UserName):
    coll = GetCollection()
    meals_for_user = coll.find({"UserName" : UserName})
    return meals_for_user

# This calulates the money that we have spent in the past month, week, and day
def GetValuesforDisplay(UserName):

    # Get the current time
    current_sec = t.time()

    # Get the current date
    today = date.today()
    curr_year = today.year
    curr_mon = today.month
    curr_day = today.day


    # This function gets the amount of money that the person has spent in
    # the past day
    coll = GetCollection()
    meals_for_user = list(coll.find({"UserName" : UserName}))

    # Values to hold the amount of money sent
    money_this_week = 0
    money_today = 0
    money_this_month = 0

    # Now loop through the loop to get the cost of what we have spent during a timeframe
    for meal in meals_for_user:
        # Check to see if this is in the today
        if curr_year == meal["Year"] and curr_mon == meal["Month"] and curr_day == meal["Day"]:
            money_this_week += meal["Price"]
            money_today += meal["Price"]
            money_this_month += meal["Price"]

        # Check to see if we are in the most recent week
        elif current_sec - meal["Time"] < 604800:
            money_this_week += meal["Price"]
            money_this_month += meal["Price"]

        # Check to see if we are in the most recent month
        elif current_sec - meal["Time"] < 43829.1*60:
            money_this_month += meal["Price"]

    # We want the average amount of money spent
    avg_money_this_week = money_this_week/float(7)
    avg_money_this_month = money_this_month/float(30)

    return money_today, avg_money_this_week, avg_money_this_month, meals_for_user
