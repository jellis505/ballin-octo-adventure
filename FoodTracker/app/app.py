from flask import Flask, render_template, request, redirect, abort
from flask.ext.script import Manager
import database_utils

app = Flask(__name__, static_url_path="/static")
app.debug = True

@app.route('/')
def index():
    return render_template('index.jinja2.html', message="Now Let's get tracking!");

@app.route('/tracked_meals', methods=['POST'])
def home():
        if request.method == 'POST':
            form = request.form
            # Get the meal info from the form
            meal_info = dict()
            meal_info['UserName'] = form['UserName']
            meal_info['Meal'] = form['Meal']
            meal_info['Price'] = form['Price']
            meal_info['FoodType'] = form['FoodType']

            # Check to make sure that the 
            if meal_info['FoodType'] not in ['Food', 'Alcohol']:
                return render_template('index.jinja2.html', message="You didn't enter proper information, please try again")
            
            # insert meal into database
            database_utils.InsertMeal(meal_info)
            
            # Get the UserName and meals
            UserName = meal_info["UserName"]
            Meals = database_utils.GetMeals(UserName)
            
            # Debug Purposes
            print "The UserName is", UserName

            # Now let's get the cost and all of the meals
            day,week,month,meals = database_utils.GetValuesforDisplay(UserName)
            print "Money Spent Today =", day
            print "Avg Money Spent this week =", week
            print "Avg Money Spent this month =", month
            print "These are the meals =", meals


            # Now add template rendering based on the data
        return render_template('trackedmeals.jinja2.html', day=day, month=month, week=week);

# This runs the app manager      
manager = Manager(app);

if __name__ == "__main__":
    manager.run()