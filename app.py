import re, os
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect

# From SQLAlchemy notation
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text

app = Flask(__name__)



## From DigitalOcean tutorial (https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import workout after defining db and app
from workout import exercise


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'





@app.route("/")
def home():
    students = Student.query.all()
    return render_template("home.html", students=students)


# Help received from ChatGPT refining this function
@app.route("/workout", methods=('GET', 'POST'))
def workout():
    if request.method == 'POST':
        exercise(app)

        return redirect("/")
    else:
        return render_template("workout.html")



@app.route("/food")
def food():
    return render_template("food.html")


@app.route("/weight")
def weight():
    return render_template("weight.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")