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
    if 'weight_file' not in request.files:
        return 'No file part'
    file = request.files['weight_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        # Process the CSV file
        pass
    else:
        return 'Please upload a CSV file'


    # Read CSV file
    if file:
        df = pd.read_csv(file)

    # Transpose CSV file into SQL
    # TODO: Be able to upload multiple weight files without deleting prior data
    engine = create_engine("sqlite:///fitness.db")
    df.to_sql('weight', engine, if_exists='replace', index=False)
    engine.dispose()

    return "success"

# Taken using weight_import as a template
def food_import():
    # Look for CSV file
    if 'food_file' not in request.files:
        return 'No file part'
    file = request.files['food_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        # Process the CSV file
        pass
    else:
        return 'Please upload a CSV file'


    # Read CSV file
    if file:
        df = pd.read_csv(file)

    # Transpose CSV file into SQL
    # TODO: Be able to upload multiple weight files without deleting prior data
    engine = create_engine("sqlite:///fitness.db")
    df.to_sql('food', engine, if_exists='replace', index=False)
    engine.dispose()

    return "success"

# Help received from ChatGPT refining this function
def export():
    # Retrieve data from SQL table
    engine = create_engine("sqlite:///fitness.db")

    # TODO: Select tables
    for var in ['exercise', 'weight', 'food']:
        sql_query = f"SELECT * FROM {var}"
        df = pd.read_sql_query(sql_query, engine)

        # Define the file path for the CSV file
        csv_file_path = f'{var}.csv'

        # Export DataFrame to CSV file
        df.to_csv(csv_file_path, index=False)

        # Check if the file was created successfully
        if os.path.exists(csv_file_path):
            print(f"CSV file '{csv_file_path}' created successfully.")
        else:
            print("Failed to create CSV file.")