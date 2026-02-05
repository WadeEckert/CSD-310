"""
===================================================================================
Title: Module 6.2 Movies: Table Queries
Original Author: Dr. Mortoza Abdullah
Modified By: Wade Eckert
Date Modified: 28 January 2026
Description:
===================================================================================
"""

""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode

import dotenv  # to use .env file
from dotenv import dotenv_values

from pathlib import Path # to handle file paths

""" Load environment variables from .env file """
# Get the directory where THIS script lives
BASE_DIR = Path(__file__).resolve().parent

# Build the full path to the .env file
env_path = BASE_DIR / ".env"

# Load environment variables
secrets = dotenv_values(env_path)

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}

""" Helper functions for database queries and display"""

# Generic function to display table records by ID and Name.
def display_table_records(title, query, id_field, name_field):
    print(f"\n\n  -- DISPLAYING {title} RECORDS --")
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        print(f"  {id_field.replace("_", " ").title()}: {record[id_field.lower()]}")
        print(f"  {name_field.replace("_", " ").title()}: {record[name_field.lower()]}\n")

# Generic Function to display films under a certain runtime."""
def display_short_films(max_runtime):
    print("\n\n  -- DISPLAYING Short Film RECORDS --")
    cursor.execute(f"SELECT film_name, film_runtime FROM film WHERE film_runtime < {max_runtime}")
    short_films = cursor.fetchall()
    for film in short_films:
        print(f"  Film Name: {film['film_name']}")
        print(f"  Runtime: {film['film_runtime']}\n")

# Display directors grouped and sorted by director name.
def display_directors_by_name():
    print("\n\n  -- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director, film_name")
    directors = cursor.fetchall()
    for record in directors:
        print(f"  Film Name: {record['film_name']}")
        print(f"  Director: {record['film_director']}\n")

""" MySQL: mysql_test.py. Connection test code """
try:
    """ try/catch block for handling potential MySQL database errors """ 
    db = mysql.connector.connect(**config)  # connect to the movies database 
    
    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
    
    input("\n\n  Press any key to continue...")
    
    # Create cursor object for MySQL queries and set dictionary=True to return results as dictionaries
    cursor = db.cursor(dictionary=True)
    
    # Execute Queries and display results
    display_table_records("Studio", "SELECT studio_id, studio_name FROM studio", "studio_id", "studio_name") # Execute Query 1
    display_table_records("Genre", "SELECT genre_id, genre_name FROM genre", "genre_id", "genre_name") # Execute Query 2
    display_short_films(120) # Execute Query 3
    display_directors_by_name() # Execute Query 4
    
    # close the cursor
    cursor.close()

except mysql.connector.Error as err:
    """ on error code """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    """ close the connection to MySQL """
    if 'db' in locals() and db.is_connected():
        db.close()