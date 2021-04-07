DROP DATABASE IF EXISTS mealSystemDBS;
CREATE DATABASE mealSystemDBS;
USE mealSystemDBS;
CREATE TABLE person(person_id INT NOT NULL AUTO_INCREMENT,first_name VARCHAR(30),last_name VARCHAR(30),age INT ,height DECIMAL(10,2) ,weight DECIMAL(10,2), password VARCHAR(250),PRIMARY KEY (person_id));
CREATE TABLE inventory (inventory_id INT NOT NULL AUTO_INCREMENT, name VARCHAR(100),PRIMARY KEY (inventory_id));
CREATE TABLE ingredient(ingred_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(100),category VARCHAR(30),calories DECIMAL(10,2),PRIMARY KEY (ingred_id));
CREATE TABLE measurement(base_unit VARCHAR(30) , abbreviation VARCHAR(7),PRIMARY KEY(base_unit));
CREATE TABLE meal (meal_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(150),PRIMARY KEY (meal_id));
CREATE TABLE type(type_no INT NOT NULL AUTO_INCREMENT,meal_type VARCHAR(30),PRIMARY KEY (type_no));
CREATE TABLE allergy (allergy_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(30),PRIMARY KEY (allergy_id));
CREATE TABLE nutrition (nutrition_no INT NOT NULL AUTO_INCREMENT, calories DECIMAL(10,2),total_fat DECIMAL(10,2),sugar DECIMAL(10,2),sodium DECIMAL(10,2), protein DECIMAL(10,2),saturated_fat DECIMAL(10,2),PRIMARY KEY (nutrition_no));
CREATE TABLE recipe (recipe_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(150),serving INT,nutrition_no INT,PRIMARY KEY (recipe_id),FOREIGN KEY (nutrition_no) REFERENCES nutrition(nutrition_no));
CREATE TABLE direction(recipe_id INT,dir_no INT,detail VARCHAR(400), PRIMARY KEY (recipe_id , dir_no),FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id) ON DELETE CASCADE);
CREATE TABLE image (meal_id INT,img_id INT,title VARCHAR(30),description VARCHAR(100),date_taken DATE, PRIMARY KEY (meal_id , img_id),FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE);
CREATE TABLE own(person_id INT ,inventory_id INT,PRIMARY KEY (person_id, inventory_id),FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id));
CREATE TABLE itemize (inventory_id INT,ingred_id  INT,quantity INT,inStock VARCHAR(1),expiration_date DATE,PRIMARY KEY (inventory_id , ingred_id),FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id),FOREIGN KEY (ingred_id) REFERENCES ingredient(ingred_id));
CREATE TABLE make (person_id INT,recipe_id INT,creation_date DATE,PRIMARY KEY (person_id,recipe_id),FOREIGN KEY (person_id) REFERENCES person(person_id),FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id));
CREATE TABLE contain (recipe_id INT,ingred_id INT,base_unit VARCHAR(30),numeric_measure DECIMAL(10,2),PRIMARY KEY (recipe_id , ingred_id, base_unit),FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),FOREIGN KEY (ingred_id) REFERENCES ingredient(ingred_id),FOREIGN KEY (base_unit) REFERENCES measurement(base_unit));
CREATE TABLE host(person_id  INT,allergy_id INT,PRIMARY KEY (person_id, allergy_id),FOREIGN KEY (person_id) REFERENCES person(person_id),FOREIGN KEY (allergy_id) REFERENCES allergy(allergy_id));
CREATE TABLE schedule(person_id INT, meal_id INT,type_no INT, meal_date DATE,auto_gen VARCHAR(1),PRIMARY KEY (person_id , meal_id, type_no),FOREIGN KEY (person_id) REFERENCES person(person_id),FOREIGN KEY (meal_id) REFERENCES meal(meal_id),FOREIGN KEY (type_no) REFERENCES type(type_no));
CREATE TABLE prepare(recipe_id INT,meal_id INT,PRIMARY KEY (recipe_id, meal_id),FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),FOREIGN KEY (meal_id) REFERENCES meal(meal_id));
CREATE TABLE reacts (allergy_id INT,ingred_id INT,PRIMARY KEY (allergy_id, ingred_id),FOREIGN KEY (allergy_id) REFERENCES allergy(allergy_id),FOREIGN KEY (ingred_id) REFERENCES ingredient(ingred_id));

DELIMITER //
CREATE PROCEDURE add_recipe( IN cal DECIMAL(10,2),
IN tot DECIMAL(10,2), IN sug DECIMAL(10,2) , IN sod DECIMAL(10,2), IN pro DECIMAL(10,2),
IN sat_fat DECIMAL(10,2), IN nam VARCHAR(150), IN ser DECIMAL(10,2))
BEGIN
DECLARE nut INT DEFAULT 0 ;
INSERT INTO nutrition (calories, total_fat, sugar ,
sodium , protein , saturated_fat) VALUES (cal , tot,sug , sod , pro, sat_fat );
SELECT count(*) INTO nut FROM nutrition;
INSERT INTO recipe (name , serving , nutrition_no) VALUES (nam , ser , nut);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE recipe_date( IN p_id INT , IN r_id INT )
BEGIN
SELECT * FROM make WHERE person_id = p_id AND recipe_id = r_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE generate_shopping_list( IN p_id INT , IN week_start_date DATE,
IN week_end_date DATE )
BEGIN
create view recipes_ingredients as select ingredient.ingred_id as ingred_id,
ingredient.name  as ingred_name, contain.recipe_id as recipe_id from ingredient
inner join contain on contain.ingred_id = ingredient.ingred_id;
select distinct t_2.ingred_name as Ingredient_Name from
(select ingred_id from itemize where inventory_id in
(select inventory_id from own where person_id = p_id) and inStock='N') as t_1 inner join
(select ingred_name, ingred_id from recipes_ingredients where recipe_id in
(select recipe_id from prepare where meal_id in (
select meal_id from schedule where person_id = p_id and (meal_date between
week_start_date and week_end_date)))) as t_2  on t_1.ingred_id = t_2.ingred_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE total_items( IN p_id INT )
BEGIN
select count(ingred_id) as total_items from itemize where inventory_id in
(select inventory_id from inventory where inventory_id in
(select inventory_id from own where person_id = p_id));
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE View_Meal_Plan( IN p_id INT , IN week_start_date DATE , week_end_date DATE)
BEGIN
select meal.name as meal_name , t_2.meal_type as meal_type , t_2.meal_date as meal_date from
(select t_1.meal_id as meal_id , type.meal_type as meal_type, t_1.meal_date as meal_date from
(select meal_id , type_no , meal_date from schedule
where person_id = p_id and meal_date between week_start_date and week_end_date )
as t_1 inner join type on type.type_no = t_1.type_no) as t_2 inner join  meal
on meal.meal_id = t_2.meal_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE schedule_calorie_count( IN p_id INT , IN week_start_date DATE , IN week_end_date DATE)
BEGIN
select SUM(calories) as Total_Calories from nutrition
where nutrition_no in ( select nutrition_no from recipe where
recipe_id in (select recipe_id from prepare where meal_id in
(select meal_id from schedule where person_id = p_id and
meal_date between week_start_date and week_end_date)));
END //
DELIMITER ;
