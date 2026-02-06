"""
===================================================================================
Title: Module 6.2 Movies: Table Queries
Original Author: Dr. Mortoza Abdullah
Modified By: Wade Eckert
Date Modified: 5 February 2026
Description: This script demonstrates how to perform various SQL operations 
(SELECT, INSERT, UPDATE, DELETE) on a MySQL database containing movie information.
It includes functions to display film information, insert new films, update film genres,
and delete films from the database.  
===================================================================================
"""

""" import statements """
import mysql.connector  # To connect to MySQL database
from mysql.connector import errorcode # To handle MySQL errors

import dotenv  # To use .env file for storing database credentials
from dotenv import dotenv_values # To load environment variables from the .env file

from pathlib import Path # To handle file paths for loading .env file

""" Load environment variables from .env file """
BASE_DIR = Path(__file__).resolve().parent # Get the directory where THIS script lives

""" Build the full path to the .env file """
env_path = BASE_DIR / ".env" 
secrets = dotenv_values(env_path) # Load environment variables from the .env file into a dictionary called secrets

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # Not in .env file - This option will cause MySQL warnings to raise exceptions
}


""" Function to delete a film record from the database based on the film name """
def delete_film(cursor, film_name):
    # Ask for confirmation before deleting
    confirm = input(f"\n  Are you sure you want to delete '{film_name}'? (yes/no): ").lower()
    
    if confirm != 'yes' and confirm != 'y':
        print(f"\n  Deletion of '{film_name}' cancelled.")
        return
    
    delete_query = """
        DELETE FROM film
        WHERE film_name = %s
    """
    values = (film_name,)

    try:
        cursor.execute(delete_query, values)  # Execute the DELETE query with the provided values 
        db.commit()  # Commit the transaction to save changes to the database
        print(f"\n  Film '{film_name}' deleted successfully.")
    except mysql.connector.Error as err:
        print(f"\n  Error deleting film: {err}")


""" Function to update the genre of a film in the database based on the film name and new genre ID """
def update_film_genre(cursor, film_name, new_genre_id):
    update_query = """
        UPDATE film
        SET genre_id = %s
        WHERE film_name = %s
    """
    values = (new_genre_id, film_name)
    
    try:
        cursor.execute(update_query, values)  # Execute the UPDATE query with the provided values 
        db.commit()  # Commit the transaction to save changes to the database
        print(f"\n  Film '{film_name}' updated successfully to new genre ID {new_genre_id}.")
    except mysql.connector.Error as err:
        print(f"\n  Error updating film: {err}")


""" Function to insert a new film record into the database """
def insert_film(cursor, film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id):
    insert_query = """
        INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    
    try:
        cursor.execute(insert_query, values)  # Execute the INSERT query with the provided values 
        db.commit()  # Commit the transaction to save changes to the database
        print(f"\n  Film '{film_name}' inserted successfully.")
    except mysql.connector.Error as err:
        print(f"\n  Error inserting film: {err}")


""" Function to display selected film information from the database """
def show_films(cursor, title):

    print(f"\n\n  -- {title} --")
    
    # SQL query to select film name, director, genre name, and studio name using INNER JOINs
    query = """
        SELECT 
            film_name AS Name, 
            film_director AS Director, 
            genre_name AS Genre, 
            studio_name AS 'Studio Name'
        FROM film f
        INNER JOIN genre g ON f.genre_id = g.genre_id
        INNER JOIN studio s ON f.studio_id = s.studio_id
    """

    cursor.execute(query)  # Execute the SQL query using the provided cursor 
    films = cursor.fetchall()  # Fetch all results from the executed query 
    
    # Iterate over the results and display formatted output for each film 
    for film in films:
        print(f"  Film Name: {film['Name']}")
        print(f"  Director: {film['Director']}")
        print(f"  Genre Name ID: {film['Genre']}")
        print(f"  Studio Name: {film['Studio Name']}\n")


""" Connection test code try/catch block for handling potential MySQL database errors """
try:
    db = mysql.connector.connect(**config)  # Connect to the movies database 
    
    # Output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
    
    input("\n\n  Press any key to continue...")
    
    # Create cursor object for MySQL queries and set dictionary=True to return results as dictionaries
    cursor = db.cursor(dictionary=True)
    
    """ Various Database Functions to Insert, Update, Delete and display results after each operation """
    # Call the show_films function to display film information
    show_films(cursor, "-- DISPLAYING FILMS  --")

    # Call the insert_film function to insert a new film record into the database
    #insert_film(cursor, "Inception", "2010-07-16", 148, "Christopher Nolan", 3, 2)

    # Call the show_films function again to display updated film information after insertion
    #show_films(cursor, "-- DISPLAYING FILMS AFTER INSERTION --")
    
    # Call the update_film_genre function to update the genre of a film in the database
    #update_film_genre(cursor, "Alien", 1)

    # Call the show_films function again to display updated film information after update
    #show_films(cursor, "-- DISPLAYING FILMS AFTER UPDATE --")

    # Call the delete_film function to delete a film record from the database
    #delete_film(cursor, "Gladiator")

    # call the show_films function again to display updated film information after deletion
    #show_films(cursor, "-- DISPLAYING FILMS AFTER DELETION --")

    # Close the cursor
    cursor.close()

except mysql.connector.Error as err:
    """ On error code, print the appropriate error message """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    """ Close the connection to MySQL """
    if 'db' in locals() and db.is_connected():
        db.close()