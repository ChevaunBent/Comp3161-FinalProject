from app import app
from app.views import genId
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
from faker import Faker
from sqlalchemy.orm import scoped_session, sessionmaker
from collections import defaultdict
from sqlalchemy import create_engine
from sqlfaker.database import Database
import time

#Execution start time
start = time.time()

# Sets up connections to database using database settings stored in environment variable
conn = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

#faker object
fake = Faker()

# add database
my_db = Database(db_name="finalproject")

# add tables wit n_rows specifying number of records
my_db.add_table(table_name="person", n_rows = 200000)
my_db.add_table(table_name="inventory", n_rows=10) 
my_db.add_table(table_name="ingredient", n_rows=10)
my_db.add_table(table_name="measurement", n_rows=10)
my_db.add_table(table_name="meal", n_rows=10)
my_db.add_table(table_name="type", n_rows=10)
my_db.add_table(table_name="allergy", n_rows=10)
my_db.add_table(table_name="nutrition", n_rows=10)
my_db.add_table(table_name="recipe", n_rows=600000)
my_db.add_table(table_name="direction", n_rows=10)
my_db.add_table(table_name="image", n_rows=10)
my_db.add_table(table_name="own", n_rows=10)
my_db.add_table(table_name="itemize", n_rows=10)
my_db.add_table(table_name="make", n_rows=10)
my_db.add_table(table_name="contain", n_rows=10)
my_db.add_table(table_name="host", n_rows=10)
my_db.add_table(table_name="schedule", n_rows=10)
my_db.add_table(table_name="prepare", n_rows=10)
my_db.add_table(table_name="reacts", n_rows=10)

#Generate fake data to add to person table
my_db.tables["person"].add_primary_key(column_name="person_id")
my_db.tables["person"].add_column(column_name="first_name", data_type="varchar(50)", data_target="first_name")
my_db.tables["person"].add_column(column_name="last_name", data_type="varchar(50)", data_target="last_name")
my_db.tables["person"].add_column(column_name="age", data_type = "varchar(10)", data_target = "random_int")
my_db.tables["person"].add_column(column_name="height", data_type = "varchar(10)", data_target = "random_int")
my_db.tables["person"].add_column(column_name="weight", data_type = "varchar(10)", data_target = "random_int")
my_db.tables["person"].add_column(column_name="email", data_type = "varchar(50)", data_target = "email")
my_db.tables["person"].add_column(column_name="username", data_type = "varchar(50)", data_target = "first_name")
my_db.tables["person"].add_column(column_name="password", data_type = "varchar(250)", data_target = "sha256")

#Generate fake data to add to inventry table
my_db.tables["inventory"].add_primary_key(column_name="inventory_id")
my_db.tables["inventory"].add_column(column_name="name", data_type="varchar(50)", data_target="company")

#Generate fake data to add to ingredient table
my_db.tables["ingredient"].add_primary_key(column_name="ingred_id")
my_db.tables["ingredient"].add_column(column_name="name", data_type="varchar(50)", data_target="color")
my_db.tables["ingredient"].add_column(column_name="category", data_type="varchar(20)", data_target="color")
my_db.tables["ingredient"].add_column(column_name="calories", data_type="varchar(10)", data_target="random_int")

#Generate fake data to add to measurement table
my_db.tables["measurement"].add_primary_key(column_name="base_unit")
my_db.tables["measurement"].add_column(column_name="abbreviation", data_type="varchar(20)", data_target="color")

#Generate fake data to add to meal table
my_db.tables["meal"].add_primary_key(column_name="meal_id")
my_db.tables["meal"].add_column(column_name="name", data_type="varchar(50)", data_target="job")

#Generate fake data to add to type table
my_db.tables["type"].add_primary_key(column_name="type_no")
my_db.tables["type"].add_column(column_name="meal_type", data_type="varchar(20)", data_target="color")

#Generate fake data to add to allergy table
my_db.tables["allergy"].add_primary_key(column_name="allergy_id")
my_db.tables["allergy"].add_column(column_name="name", data_type="varchar(50)", data_target="color")

#Generate fake data to add to nutrition table
my_db.tables["nutrition"].add_primary_key(column_name="nutrition_no")
my_db.tables["nutrition"].add_column(column_name="name", data_type="varchar(50)", data_target="company")
my_db.tables["nutrition"].add_column(column_name="calories", data_type="varchar(50)", data_target="random_int")
my_db.tables["nutrition"].add_column(column_name="total_fat", data_type="varchar(50)", data_target="random_int")
my_db.tables["nutrition"].add_column(column_name="sugar", data_type="varchar(50)", data_target="random_int")
my_db.tables["nutrition"].add_column(column_name="sodium", data_type="varchar(50)", data_target="random_int")
my_db.tables["nutrition"].add_column(column_name="protein", data_type="varchar(50)", data_target="random_int")
my_db.tables["nutrition"].add_column(column_name="saturated_fat", data_type="varchar(50)", data_target="random_int")

#Generate fake data to add to recipe table
my_db.tables["recipe"].add_primary_key(column_name="recipe_id")
my_db.tables["recipe"].add_column(column_name="name", data_type="varchar(50)", data_target="color")
my_db.tables["recipe"].add_column(column_name="serving", data_type="varchar(20)", data_target="random_int")
my_db.tables["recipe"].add_foreign_key(column_name="nutrition_no", target_table="nutrition", target_column="nutrition_no")

#Generate fake data to add to direction table
my_db.tables["direction"].add_primary_key(column_name="recipe_id")
my_db.tables["direction"].add_primary_key(column_name="dir_no")
my_db.tables["direction"].add_column(column_name="detail", data_type="varchar(500)", data_target="job")
my_db.tables["direction"].add_foreign_key(column_name="recipe_id", target_table="recipe", target_column="recipe_id")

#Generate fake data to add to image table
my_db.tables["image"].add_primary_key(column_name="meal_id")
my_db.tables["image"].add_primary_key(column_name="img_id")
my_db.tables["image"].add_column(column_name="title", data_type="varchar(50)", data_target="color")
my_db.tables["image"].add_column(column_name="description", data_type="varchar(50)", data_target="job")
my_db.tables["image"].add_column(column_name="date_taken", data_type="date", data_target="date_time")
my_db.tables["image"].add_foreign_key(column_name="meal_id", target_table="meal", target_column="meal_id")

#Generate fake data to add to own table
my_db.tables["own"].add_primary_key(column_name="person_id")
my_db.tables["own"].add_primary_key(column_name="inventory_id")
my_db.tables["own"].add_foreign_key(column_name="person_id", target_table="person", target_column="person_id")
my_db.tables["own"].add_foreign_key(column_name="inventory_id", target_table="inventory", target_column="inventory_id")

#Generate fake data to add to itemize table
my_db.tables["itemize"].add_primary_key(column_name="inventory_id")
my_db.tables["itemize"].add_primary_key(column_name="ingred_id")
my_db.tables["itemize"].add_column(column_name="quantity", data_type="varchar(50)", data_target="random_int")
my_db.tables["itemize"].add_column(column_name="inStock", data_type="varchar(20)", data_target="color")
my_db.tables["itemize"].add_column(column_name="expiration_date", data_type="date", data_target="date_time")
my_db.tables["itemize"].add_foreign_key(column_name="inventory_id", target_table="inventory", target_column="inventory_id")
my_db.tables["itemize"].add_foreign_key(column_name="ingred_id", target_table="ingredient", target_column="ingred_id")

#Generate fake data to add to make table
my_db.tables["make"].add_primary_key(column_name="person_id")
my_db.tables["make"].add_primary_key(column_name="recipe_id")
my_db.tables["make"].add_column(column_name="creation_date", data_type="date", data_target="date_time")
my_db.tables["make"].add_foreign_key(column_name="person_id", target_table="person", target_column="person_id")
my_db.tables["make"].add_foreign_key(column_name="recipe_id", target_table="recipe", target_column="recipe_id")

#Generate fake data to add to contain table
my_db.tables["contain"].add_primary_key(column_name="recipe_id")
my_db.tables["contain"].add_primary_key(column_name="ingred_id")
my_db.tables["contain"].add_primary_key(column_name="base_unit")
my_db.tables["contain"].add_column(column_name="numeric_measure", data_type="varchar(10)", data_target="color")
my_db.tables["contain"].add_foreign_key(column_name="recipe_id", target_table="recipe", target_column="recipe_id")
my_db.tables["contain"].add_foreign_key(column_name="ingred_id", target_table="ingredient", target_column="ingred_id")
my_db.tables["contain"].add_foreign_key(column_name="base_unit", target_table="measurement", target_column="base_unit")

#Generate fake data to add to host table
my_db.tables["host"].add_primary_key(column_name="person_id")
my_db.tables["host"].add_primary_key(column_name="allergy_id")
my_db.tables["host"].add_foreign_key(column_name="person_id", target_table="person", target_column="person_id")
my_db.tables["host"].add_foreign_key(column_name="allergy_id", target_table="allergy", target_column="allergy_id")

#Generate fake data to add to make table
my_db.tables["schedule"].add_primary_key(column_name="person_id")
my_db.tables["schedule"].add_primary_key(column_name="meal_id")
my_db.tables["schedule"].add_primary_key(column_name="type_no")
my_db.tables["schedule"].add_column(column_name="meal_date", data_type="date", data_target="date_time")
my_db.tables["schedule"].add_column(column_name="auto_gen", data_type="varchar(20)", data_target="color")
my_db.tables["schedule"].add_foreign_key(column_name="person_id", target_table="person", target_column="person_id")
my_db.tables["schedule"].add_foreign_key(column_name="meal_id", target_table="meal", target_column="meal_id")
my_db.tables["schedule"].add_foreign_key(column_name="type_no", target_table="type", target_column="type_no")

#Generate fake data to add to make table
my_db.tables["prepare"].add_primary_key(column_name="recipe_id")
my_db.tables["prepare"].add_primary_key(column_name="meal_id")
my_db.tables["prepare"].add_foreign_key(column_name="recipe_id", target_table="recipe", target_column="recipe_id")
my_db.tables["prepare"].add_foreign_key(column_name="meal_id", target_table="meal", target_column="meal_id")

#Generate fake data to add to make table
my_db.tables["reacts"].add_primary_key(column_name="allergy_id")
my_db.tables["reacts"].add_primary_key(column_name="ingred_id")
my_db.tables["reacts"].add_foreign_key(column_name="allergy_id", target_table="allergy", target_column="allergy_id")
my_db.tables["reacts"].add_foreign_key(column_name="ingred_id", target_table="ingredient", target_column="ingred_id")


#Generate sql data
my_db.generate_data()

#Export sql data to .sql file
my_db.export_sql("sqlfile.sql")


#Runs SQL file to populate database on server
with conn.connect() as con:
    file = open('sqlfile.sql')
    query = text(file.read())
    #Creates tables and populates
    con.execute(query)
    #Creates stored procedures 
    proc1 = "CREATE PROCEDURE recipe_date( IN p_id INT , IN r_id INT ) \
			BEGIN\
            SELECT * FROM make WHERE person_id = p_id AND recipe_id = r_id;\
            END"
    proc2 = "CREATE PROCEDURE total_items( IN p_id INT )\
            BEGIN\
            select count(ingred_id) as total_items from itemize where inventory_id in\
            (select inventory_id from inventory where inventory_id in\
            (select inventory_id from own where person_id = p_id));\
            END"
    #creates stored procedures from server end
    con.execute(proc1)
    con.execute(proc2)
    #Closes server
    con.close()
    #Execution end time
    end=time.time()
    #Calculate total execution time
    lapse = end-start

print("SQL File successfuly created and executed in", lapse , "seconds")