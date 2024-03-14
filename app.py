import re, os
from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
import json
from flask_basicauth import BasicAuth



app = Flask(__name__)


# ChatGPT helped with authorisation code
# Load the JSON configuration
with open(r'/home/BiggestChris/Keys/MySQL-keys.json') as sql_file:
    sql_keys = json.load(sql_file)
# Configure CS50 Library to use MySQL database on PythonAnywhere
db = SQL(f"mysql://{sql_keys['username']}:{sql_keys['password']}@BiggestChris.mysql.eu.pythonanywhere-services.com/BiggestChris$fitness")


# Import workout after defining db and app
from workout import exercise, weight_import, food_import, weight_export, food_export, exercise_export, retrieve_workout
from workoutobject import workout_list
workout_list_json = json.dumps(workout_list)

# ChatGPT helped with authorisation code
# Load the JSON configuration
with open(r'/home/BiggestChris/Keys/flash-auth-keys.json') as config_file:
    config = json.load(config_file)

# Set the basic authentication credentials

app.config['BASIC_AUTH_USERNAME'] = config['username']
app.config['BASIC_AUTH_PASSWORD'] = config['password']
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

@basic_auth.required
def basic_auth_check():
    pass  # This function is needed to ensure basic auth is checked for all routes


@app.route("/")
def home():
    return render_template("home.html")


# Help received from ChatGPT refining this function
@app.route("/workout", methods=('GET', 'POST'))
def workout():
    if request.method == 'POST':
        exercise_variable = exercise()

        if exercise_variable == 'ERROR':
            return redirect("/upload_error")
        else:
            return redirect("/workout")
    
    else:
        last_workout = retrieve_workout()
        last_workout_json = json.dumps(last_workout)

        return render_template("workout.html", workout_list=workout_list, workout_list_json=workout_list_json, last_workout_json=last_workout_json)



@app.route("/food", methods=('GET', 'POST'))
def food():
    if request.method == 'POST':
        food_import()

        return redirect("/")
    else:
        return render_template("food.html")


@app.route("/weight", methods=('GET', 'POST'))
def weight():
    if request.method == 'POST':
        weight_import()

        return redirect("/")
    else:
        return render_template("weight.html")


@app.route("/export")
def export_page():
    return render_template("export.html")


@app.route("/weight_export", methods=('GET', 'POST'))
def get_data_weight():
    if request.method == 'POST':
        weight_export()

        return redirect("/")
    else:
        return render_template("export.html")

@app.route("/food_export", methods=('GET', 'POST'))
def get_data_food():
    if request.method == 'POST':
        food_export()

        return redirect("/")
    else:
        return render_template("export.html")

@app.route("/exercise_export", methods=('GET', 'POST'))
def get_data_exercise():
    if request.method == 'POST':
        exercise_export()

        return redirect("/")
    else:
        return render_template("export.html")
    
@app.route("/upload_error")
def upload_error():
    return render_template("error.html")