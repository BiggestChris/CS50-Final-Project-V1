import re, os
from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect



app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fitness.db")

# Import workout after defining db and app
from workout import exercise, weight_import



@app.route("/")
def home():
    return render_template("home.html")


# Help received from ChatGPT refining this function
@app.route("/workout", methods=('GET', 'POST'))
def workout():
    if request.method == 'POST':
        exercise()

        return redirect("/")
    else:
        return render_template("workout.html")



@app.route("/food")
def food():
    return render_template("food.html")


@app.route("/weight", methods=('GET', 'POST'))
def weight():
    if request.method == 'POST':
        weight_import()

        return redirect("/")
    else:
        return render_template("weight.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")