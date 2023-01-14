# Write a new controller for entity pet
# Each pet has id, name, and species, owner ID
# Pet can be associated with a user
# Each user may or may not have pet
#  either belongs to user or doesn't belong to anyone
# Implements CRUD controller for Pet[same as for user]

# Create a controller called pet adoption controller
# One method has to be To search for pet with no owner
# There is end point: Find owner for a pet
# On the search page each pet is presented on each line
# For each pet there is two links
# One link to show pet profile [Show_Pets on pets' controller]
# Second link is find_owner
# Find owner page shows the pet name species, and has a dropdown <input type='select'>
# In this select input the users that don't own any pets Are shown usernames of users that don't have any pets
# When administrator selects a username the user id is selected for the input
# When administrator submits the form the user and pet get associated on the database and gets persisted

# Add new feature to show user page
# There should be a section called pet which shows user's pet name and species if it has one
# If user doesn't have any pets, this section is not shown


# BONUS REQUIREMENTS
# If on the user edit page if the name is empty and user tries to submit the form controller should not persist the user
# And redirect back to the edit page with error message []


import sqlite3



def connect_to_db():
    connection = sqlite3.connect('site.db')
    connection.execute("PRAGMA foreign_key = 1")
    return connection



query = (""" CREATE TABLE IF NOT EXISTS user
        (userId         INTEGER         PRIMARY KEY AUTOINCREMENT,
        firstname            TEXT            NOT NULL,
        lastname         TEXT            NOT NULL,
        petId          INTEGER        DEFAULT '0' NOT NULL,
        FOREIGN KEY (petId) REFERENCES pet (ownerId));""")

connect_to_db().execute(query)