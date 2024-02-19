import re, os
from datetime import datetime
import pandas as pd

from flask import request
from sqlalchemy import create_engine

from app import db
    
# Help received from ChatGPT refining this function
def exercise():
    # TODO: Add Server-side checks on entries
    exercise_name = request.form.get("exercise")
    weights =[]
    sets = []
    numbers = ["one","two","three","four","five"]

    # Loop through all possible sets
    for i in numbers:       
        set_value = request.form.get(f"set-{i}-reps")
        set_weight = request.form.get(f"set-{i}-weight")
        if set_value:
            sets.append(int(set_value))
            weights.append(set_weight)

    # Upload into SQL tables
    db.execute("INSERT INTO exercise (Exercise) VALUES (?)", exercise_name)
    
    # Get the last inserted row ID (primary key)
    last_inserted_id = db.execute("SELECT last_insert_rowid()")[0]['last_insert_rowid()']

    # Upload into SQL tables
    # TODO: Error deriving from zero-indexing arrays and first numbers being "one" (suspected) - Fix
    for i in range(len(sets)):
        try:
            if sets[i]:
                db.execute("UPDATE exercise SET ? = ?, ? = ? WHERE ID = ?", f"Set{numbers[i].capitalize()}_Reps", sets[i], f"Set{numbers[i].capitalize()}_Weight", weights[i], last_inserted_id)
        except IndexError:
            pass

    return "success"

# Help received from ChatGPT refining this function
def weight_import():
    # Look for CSV file
    data = r"C:\Users\styli\OneDrive\Documents\Coding\CS50\CS50 - Final Project - Git\Renpho Data\Renpho-Christopher 2024-02-19.csv"


    # Read CSV file
    df = pd.read_csv(data)

    # Transpose CSV file into SQL
    engine = create_engine("sqlite:///fitness.db")
    df.to_sql('weight-1', engine, if_exists='replace', index=False)
    engine.dispose()

    return "success"