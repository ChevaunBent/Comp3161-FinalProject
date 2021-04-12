/*

Requires node.js
Install the following packages using the command: npm i < package >
faker
fs

npm install sha1


GROUP MEMBERS:


*/

var faker = require('faker');
var fs = require('fs');
var sha1 = require('sha1');
var sql_output = "";
var int_sql = "";

//collection of person data
var p_inserts = "";
//collection of inventory data
var inventory_inserts = "";
// collection of records for owns table
var own_inserts = "";

var nutrition_inserts = "";

var recipe_inserts = "";

var direction_inserts = "";

var meal_inserts = "INSERT INTO meal (name) VALUES ";

var meal_type_inserts = "INSERT INTO type (meal_type) VALUES ";

var schedule_inserts = "INSERT INTO schedule VALUES ";

var ingredient_inserts = "INSERT INTO ingredient(name,category,calories) VALUES ";

var measurement_inserts = "INSERT INTO measurement( base_unit , abbreviation) VALUES ";

var itemize_inserts = "INSERT INTO itemize VALUES ";

var make_inserts = "INSERT INTO make VALUES ";

var contain_inserts = "INSERT INTO contain VALUES ";

var prepare_inserts = "INSERT INTO prepare VALUES ";

var host_inserts = "INSERT INTO host VALUES ";

var allergy_inserts = "INSERT INTO allergy (name) VALUES ";

var reacts_inserts = "INSERT INTO reacts VALUES ";



var stored_recipe_name = [];

var count_r = 0 ;
var count_n = 0 ;
var count_p = 0 ;

var n_p_1 = 1 ,  n_p_2 = 2 , n_p_3 = 3 , n_p_4 = 4,
n_p_5 = 5 ,  n_p_6 = 6 , n_p_7 = 7 , n_p_8 = 8 ,
n_p_9 = 9 , n_p_10 = 10;

person_table_query = "CREATE TABLE person("
 +"person_id INT NOT NULL AUTO_INCREMENT,"
 +"first_name VARCHAR(30),"
 +"last_name VARCHAR(30),"
 +"age INT ,"
 +"height DECIMAL(10,2) ,"
 +"weight DECIMAL(10,2), password VARCHAR(40),"
 +"PRIMARY KEY (person_id))";



 inventory_table_query = "CREATE TABLE inventory ("
   +"inventory_id INT NOT NULL AUTO_INCREMENT, name VARCHAR(100),"
   +"PRIMARY KEY (inventory_id))";



 ingredient_table_query = "CREATE TABLE ingredient("
   +"ingred_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(100),"
   +"category VARCHAR(30),calories DECIMAL(10,2),"
   +"PRIMARY KEY (ingred_id))";


 measurement_table_query = "CREATE TABLE measurement("
   +"base_unit VARCHAR(30) , abbreviation VARCHAR(7),"
   +"PRIMARY KEY(base_unit))";


 meal_table_query = "CREATE TABLE meal ("
    +"meal_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(150),"
    +"PRIMARY KEY (meal_id))";



 type_table_query = "CREATE TABLE type("
   +"type_no INT NOT NULL AUTO_INCREMENT,meal_type VARCHAR(30),"
   +"PRIMARY KEY (type_no))";



 allergy_table_query = "CREATE TABLE allergy ("
   +"allergy_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(30),"
   +"PRIMARY KEY (allergy_id))";



 nutrition_table_query = "CREATE TABLE nutrition ("
   +"nutrition_no INT NOT NULL AUTO_INCREMENT, calories DECIMAL(10,2),"
   +"total_fat DECIMAL(10,2),sugar DECIMAL(10,2),"
   +"sodium DECIMAL(10,2), protein DECIMAL(10,2),"
   +"saturated_fat DECIMAL(10,2),"
   +"PRIMARY KEY (nutrition_no))";



 recipe_table_query = "CREATE TABLE recipe ("
   +"recipe_id INT NOT NULL AUTO_INCREMENT,name VARCHAR(150),"
   +"serving INT,"
   +"nutrition_no INT,"
   +"PRIMARY KEY (recipe_id),"
   +"FOREIGN KEY (nutrition_no) REFERENCES nutrition(nutrition_no))";

 direction_table_query = "CREATE TABLE direction("
   +"recipe_id INT,dir_no INT,"
   +"detail VARCHAR(400), PRIMARY KEY (recipe_id , dir_no),"
   +"FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id) ON DELETE CASCADE)";


 image_table_query = "CREATE TABLE image ("
   +"meal_id INT,img_id INT,"
   +"title VARCHAR(30),description VARCHAR(100),"
   +"date_taken DATE, PRIMARY KEY (meal_id , img_id),"
   +"FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE)";


 own_table_query = "CREATE TABLE own("
   +"person_id INT ,inventory_id INT,"
   +"PRIMARY KEY (person_id, inventory_id),"
   +"FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id))";


 itemize_table_query = "CREATE TABLE itemize ("
    +"inventory_id INT,ingred_id  INT,"
    +"quantity INT,inStock VARCHAR(1),"
    +"expiration_date DATE,"
    +"PRIMARY KEY (inventory_id , ingred_id),"
    +"FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id),"
    +"FOREIGN KEY (ingred_id) REFERENCES ingredient(ingred_id))";



 make_table_query = "CREATE TABLE make ("
   +"person_id INT,recipe_id INT,"
   +"creation_date DATE,"
   +"PRIMARY KEY (person_id,recipe_id),"
   +"FOREIGN KEY (person_id) REFERENCES person(person_id),"
   +"FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id))";



 contains_table_query = "CREATE TABLE contain ("
   +"recipe_id INT,ingred_id INT,"
   +"base_unit VARCHAR(30),numeric_measure DECIMAL(10,2),"
   +"PRIMARY KEY (recipe_id , ingred_id, base_unit),"
   +"FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),"
   +"FOREIGN KEY (ingred_id) REFERENCES ingredient(ingred_id),"
   +"FOREIGN KEY (base_unit) REFERENCES measurement(base_unit))";



 host_table_query = "CREATE TABLE host("
   +"person_id  INT,allergy_id INT,"
   +"PRIMARY KEY (person_id, allergy_id),"
   +"FOREIGN KEY (person_id) REFERENCES person(person_id),"
   +"FOREIGN KEY (allergy_id) REFERENCES allergy(allergy_id))";



 schedule_table_query = "CREATE TABLE schedule("
   +"person_id INT, meal_id INT,"
   +"type_no INT, meal_date DATE,"
   +"auto_gen VARCHAR(1),"
   +"PRIMARY KEY (person_id , meal_id, type_no),"
   +"FOREIGN KEY (person_id) REFERENCES person(person_id),"
   +"FOREIGN KEY (meal_id) REFERENCES meal(meal_id),"
   +"FOREIGN KEY (type_no) REFERENCES type(type_no))";



 prepare_table_query = "CREATE TABLE prepare("
   +"recipe_id INT,meal_id INT,"
   +"PRIMARY KEY (recipe_id, meal_id),"
   +"FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),"
   +"FOREIGN KEY (meal_id) REFERENCES meal(meal_id))";



 reacts_table_query = "CREATE TABLE reacts ("
   +"allergy_id INT,ingred_id INT,"
   +"PRIMARY KEY (allergy_id, ingred_id),"
   +"FOREIGN KEY (allergy_id) REFERENCES allergy(allergy_id),"
   +"FOREIGN KEY (ingred_id) REFERENCES ingredient(ingred_id))";


  int_sql += "DROP DATABASE IF EXISTS mealSystemDBS;\n";
  int_sql += "CREATE DATABASE mealSystemDBS;\n";
  int_sql += "USE mealSystemDBS;\n";

  int_sql += person_table_query + ';\n';

  int_sql += inventory_table_query + ';\n';

  int_sql += ingredient_table_query + ';\n';

  int_sql += measurement_table_query + ';\n';

  int_sql += meal_table_query + ';\n';

  int_sql += type_table_query + ';\n';

  int_sql += allergy_table_query+ ';\n';

  int_sql += nutrition_table_query+ ';\n';

  int_sql += recipe_table_query+ ';\n';

  int_sql += direction_table_query+ ';\n';

  int_sql += image_table_query+ ';\n';

  int_sql += own_table_query+ ';\n';

  int_sql += itemize_table_query + ';\n';

  int_sql += make_table_query + ';\n';

  int_sql += contains_table_query + ';\n';

  int_sql += host_table_query + ';\n';

  int_sql += schedule_table_query + ';\n';

  int_sql += prepare_table_query + ';\n';


  int_sql += reacts_table_query + ';\n';

  initialize_database();


function populate_person_own_inventory( )
{
  faker.seed(300);
  p_inserts += "INSERT INTO person VALUES ";
  inventory_inserts += "INSERT INTO inventory (name) VALUES ";
  own_inserts += "INSERT INTO own VALUES ";

  for( i = 0 ; i < 20000 ; i++)
  {
      age = Math.floor(Math.random() * 70) + 18
      height = (Math.floor(Math.random() * 180) + 100) / 100 // measured in meters
      weight =(Math.floor(Math.random() * 10000) + 4500) / 100 // kg
      first_name = faker.name.firstName();

      count_p += 1;
      if ( ! ( (count_p % 20000) == 1 )  )
      {

        p_inserts += ',(' + count_p.toString() +',"'+first_name+'"'+','+
        '"'+faker.name.lastName()+'"'+','+'"'+age.toString()+'"'+','+'"'+height+'"'+','+
        '"'+ weight +'","'+ sha1(faker.internet.password())+'")';
        inventory_inserts += ',("'+ first_name +' Kitchen Inventory")';
        own_inserts += ',("'+ count_p.toString() +'","'+ count_p.toString() +'")';
      }
      else
      {
        p_inserts += '(' + count_p.toString() +',"'+first_name+'"'+','+
        '"'+faker.name.lastName()+'"'+','+'"'+age.toString()+'"'+','+'"'+height+'"'+','+
        '"'+ weight +'","'+ sha1(faker.internet.password())+'")';

        inventory_inserts += '("'+ first_name +' Kitchen Inventory")';
        own_inserts += '("'+ count_p.toString() +'","'+ count_p.toString() +'")';
      }


    }

    p_inserts += ";\n";
    inventory_inserts += ";\n";
    own_inserts += ";\n";
}

/*  populating recipe, nutrition & directions table  below */

function recipe_nutrition_instructions ()
{
  faker.seed(300);

  nutrition_inserts += "INSERT INTO nutrition (calories, total_fat , sugar , sodium , protein, saturated_fat) VALUES ";
  recipe_inserts += "INSERT INTO recipe( name , serving , nutrition_no) VALUES ";
  direction_inserts += "INSERT INTO direction ( recipe_id , dir_no , detail ) VALUES ";

  food_suffix = [' Soup',' Stew', ' Roast' , ' Dried', ' Bake',' Jerk']

  for ( i = 0 ;  i < 30000 ; i++){

    //nutrition table
    nutrition_data = [0,0,0,0,0,0];
    nutrition_data[0] = Math.random()* 2000;
    nutrition_data[1] = Math.random()* 100 ;
    nutrition_data[2]  = Math.random()* 100;
    nutrition_data[3] = Math.random()* 100 ;
    nutrition_data[4] = Math.random()* 100 ;
    nutrition_data[5] = Math.random()* 100;

    count_n = count_n + 1;

    if(  !( (count_n % 30000) == 1) )
    {
      nutrition_inserts += ",(" + nutrition_data[0]+ "," + nutrition_data[1] + "," + nutrition_data[2] + "," + nutrition_data[3]
      + "," + nutrition_data[4] + "," + nutrition_data[5] + ")";
    }
    else
    {
      nutrition_inserts += "(" + nutrition_data[0]+ "," + nutrition_data[1] + "," + nutrition_data[2] + "," + nutrition_data[3]
      + "," + nutrition_data[4] + "," + nutrition_data[5] + ")";
    }

    //recipe table name , serving , nutr_no
    n = Math.floor(Math.random() * 5)
    recipe_name = "";
    switch (n)
    {
      case 0 :
      recipe_name = faker.animal.fish() + " "+ food_suffix[n];
      break;
      case 1 :
      recipe_name = faker.animal.cow() + " "+ food_suffix[n];
      break;
      case 2 :
      recipe_name = faker.animal.bird() + " "+ food_suffix[n];
      break;
      case 3 :
      recipe_name = faker.animal.bear() + " "+ food_suffix[n];
      break;
      case 4 :
      recipe_name = faker.animal.crocodilia() + " "+ food_suffix[n];
      break;
    }

    count_r = count_r + 1 ;

    if (  ! ( (count_r % 30000) == 1) )
    {
      recipe_inserts += ',("'+recipe_name + '",' + (n + 1).toString() + "," + (count_n).toString() + ")";
    }
    else
    {
      recipe_inserts += '("'+recipe_name + '",' + (n + 1).toString() + "," + (count_n).toString() + ")";
    }

    stored_recipe_name.push(recipe_name);


    dir_no =  1 ;
    if (  ! ( (count_r % 30000) == 1) )
    {
      direction_inserts += ",(" + (count_r).toString() + "," + dir_no.toString() + ",'" + faker.lorem.sentence() + "')";
    }
    else
    {
      direction_inserts += "(" + (count_r).toString() + "," + dir_no.toString() + ",'" + faker.lorem.sentence() + "')";
    }
  }
  nutrition_inserts += ";\n";
  recipe_inserts += ";\n";
  direction_inserts += ";\n";

}

async function  populate_meals ()
{
   let promise = new Promise ( (resolve , reject ) => {

           for ( i = 1 ; i < 601 ; i++)
           {
              if (i != 1 )
              {
                meal_inserts += ',( "'+ stored_recipe_name[i] +'")';
              }
              else
              {
                meal_inserts += '( "'+ stored_recipe_name[i] +'")';
              }
            }
          resolve();
        });

        let msg = await promise;
        populate_schedule_meals();
        populate_prepare ();
        populate_image();
}

function populate_meal_type ()
{
  let no_loops_need = 1400

  // 200,000 people each have 1 meal plan for a week
  // breakfast, lunch and dinner, since  week = 7 days
  // 200k * 7 = 1400000 or 4.2 million records

  for (i = 1 ; i < (no_loops_need + 1) ; i ++)
  {
        //create meal_type
        if(i == 1 )
        {
          meal_type_inserts += "( 'BREAKFAST' )";
        }
        meal_type_inserts += ",( 'BREAKFAST' )";
        meal_type_inserts += ",( 'LUNCH' )";
        meal_type_inserts += ",( 'DINNER' )";
  }
}

function populate_schedule_meals () {


  var breakfast = 1 ; lunch  = 2 ; dinner = 3;
  var date = "2021-03-";
  var queries = [];
  var random_meal = [];
  var random_day = [];

  var marker = false ;
  for ( i = 0 ; i < 200 ; i ++)
  {
    random_meal.push( Math.floor((Math.random() * 500) + 1));
    random_day.push(Math.floor((Math.random() * 24) + 1));
  }

   for (i = 0 ; i < 200 ; i ++)
   {

     for( j = 0 ; j <  7 ; j++ )
     {
       if ( marker )
       {
         queries.push (',( "'+ (i+1).toString() +'","'
         + (random_meal[i]++ ).toString() + '","' + breakfast.toString() +
         '","' + date + (random_day[i] + j).toString() + '",'+ '"N")');

         queries.push( ',( "'+ (i+1).toString() +'","'
          + (random_meal[i]++ ).toString() + '","' + lunch.toString() +
         '","' + date + (random_day[i] + j).toString() + '",'+ '"N")');

         queries.push (',( "' + (i+1).toString()+ '","'
         + (random_meal[i]++ ).toString() + '","' + dinner.toString() +
         '","' + date + (random_day[i] + j).toString() + '",' + '"N")');
       }
       else
       {
         queries.push ('( "'+ (i+1).toString() +'","'
         + (random_meal[i]++ ).toString() + '","' + breakfast.toString() +
         '","' + date + (random_day[i] + j).toString() + '",'+ '"N")');

         queries.push( ',( "'+ (i+1).toString() +'","'
          + (random_meal[i]++ ).toString() + '","' + lunch.toString() +
         '","' + date + (random_day[i] + j).toString() + '",'+ '"N")');

         queries.push (',( "' + (i+1).toString()+ '","'
         + (random_meal[i]++ ).toString() + '","' + dinner.toString() +
         '","' + date + (random_day[i] + j).toString() + '",' + '"N")');
         marker = true;
       }

        breakfast = breakfast + 3 ; lunch = lunch + 3 ; dnner = dinner + 3 ;
     }
   }

   queries.forEach( (query) => {
     schedule_inserts +=  query ;
    //setTimeout( function () {console.log(query) }, 3000);
   });

}
function populate_ingredients (){

  let vegetable = [
  "Acorn Squash" ,"Amaranth" ,"Anaheim Chile",
  "Arrowroot","Artichoke", "Arugula",
  "Asparagus","Baby Candy Cane Beets","Baby Oyster Mushrooms",
  "Banana Squash","Beets","Belgian Endive",
  "Bell Peppers","Bitter Melons","Black Radish",
  "Black Salsify","Bok Choy","Boniato",
  "Broccoflower","Carrot","Chanterelle Mushroom",
  "Chayote Squash","Cherry Tomato","Chinese Eggplant",
  "Dandelion Greens","Delicata Squash","Garlic",
  "Ginger Root","Green Onion","Shallots",
  "Shiitake Mushrooms","Snow Peas", "Sorrel",
  "Spinach" , "Sugar Snap Peas", "Tomato","Yam"];

  //milk
  for ( i = 0 ; i < 50 ; i++){
    product = faker.animal.cow() + " Milk";
    calories = Math.floor( (Math.random()* 50) + 40 );

    if (i != 0 )
    {
      ingredient_inserts += ',( " ' + product + '",'
       +' "DAIRY" '+ ',' +calories.toString() + ')';
    }
    else
    {
      ingredient_inserts += '( "' + product + '"'+
      ","+'"DAIRY"'+ ',' +calories.toString() + ')';
    }
  }

  //eggs
  for ( i = 0 ; i < 50 ; i++){
    product = faker.animal.bird() + " Egg";
    calories = Math.floor( (Math.random()* 50) + 40 );
    ingredient_inserts += ',( "' + product + '"'+ ","+'"PROTEIN"'+ ',' +calories.toString() + ')';
  }

  //meat
  for ( i = 0 ; i < 50 ; i++){

    n = Math.floor( (Math.random() * 5)  + 1);
    product ="";
    switch (n)
    {
      case 1 :
      product = faker.animal.cow() + " Meat";
      break;
      case 2 :
      product = faker.animal.bird() + " Meat";
      break;
      case 3 :
      product = faker.animal.bear() + " Meat";
      break;
      case 4 :
      product = faker.animal.crocodilia() + " Meat";
      break;
    }
    calories = Math.floor( (Math.random()* 50) + 40 );
    ingredient_inserts += ',( "' + product + '"'+
    ","+'"MEAT"'+ ',' +calories.toString() + ')';
  }
  //Seafood
  for( i = 0 ; i < 50 ; i++)
  {
    product = faker.animal.fish() ;
    calories = Math.floor( (Math.random()* 50) + 40 );

    ingredient_inserts += ',( "' + product + '"'+
    ","+'"SEAFOOD"'+ ',' +calories.toString() + ')';
  }
  //Vegetables

  for ( i = 0 ; i < vegetable.length; i ++){

    calories = Math.floor( (Math.random()* 50) + 40 );
    ingredient_inserts += ',( "' + vegetable[i] + '"'+
    ","+'"VEGETABLE"'+ ',' +calories.toString() + ')';
  }
}

function populate_measuremnt() {

  base = [ "", "Tablespoon" , "tsp" , "Ounce","Oz", "Cup","c",
  "Quart","qt","Gallon","gal","Pound","lb","Units","Units"];

  for( i = 1 ; i < 8 ; i++)
  {
     pos_1 = 2 * i  - 1;
     pos_2 = 2 * i;

    if (i != 1 )
    {
      measurement_inserts += ',("'+ base[pos_1] + '","' + base[pos_2] + '" )';

    }
    else
    {
      measurement_inserts += '("'+ base[pos_1] + '","' + base[pos_2] + '" )';
    }
  }

}

function populate_itemize (){

  for (i = 1 ; i < 201 ; i++){

    no_items = Math.floor(Math.random()*50) + 50;
    ingred_id = Math.floor(Math.random()* 100) + 1;

    for( j = 0 ; j < no_items ; j++)
    {
       qty = Math.floor(Math.random()* 20) + 1;
       inStock  = ["","Y","N"] ;
       gamble = Math.floor(Math.random() * 2) + 1;
       ex_date = "2021-"+ (Math.floor(Math.random()*8) + 4 ).toString() + "-" +
       (Math.floor( (Math.random()*29) + 1)).toString();

       if ( !(j == 0 && i == 1) )
       {
         itemize_inserts += ',(' + i.toString() + ',' + (ingred_id + j).toString()
         + ',' + qty.toString() + ',"' + inStock[gamble] + '","'+ ex_date + '")';
       }
       else
       {
         itemize_inserts += '(' + i.toString() + ',' + (ingred_id + j).toString()
         + ',' + qty.toString() + ',"' + inStock[gamble] + '","'+ ex_date + '")';

       }

    }

  }

}

function populate_make (){

      let r_1 = 1 ;
      let r_2 = 2 ;
      let r_3 = 3 ;

      // each person gets 3 recipes assigned to them
      //
      for( i = 1 ; i < 201 ; i ++)
      {
        _date = "2020-"+ (Math.floor(Math.random()*12) + 1 ).toString() + "-" +
        (Math.floor( (Math.random()*29) + 1)).toString();

        if( i != 1 )
        {
          make_inserts += ',(' + i.toString() + ',' + r_1.toString()
          + ',"' + _date +'")';
        }
        else
        {
          make_inserts += '(' + i.toString() + ',' + r_1.toString()
          + ',"' + _date +'")';
        }


        make_inserts += ',('+ i.toString() + ',' + r_2.toString()
        + ',"' + _date +'")';


        make_inserts += ',('+ i.toString() + ',' + r_3.toString()
        + ',"' + _date +'")';

        r_1 = r_1 + 3 ;
        r_2 = r_2 + 3 ;
        r_2 = r_3 + 3 ;
    }

  }

function contain (){

  base = ["Tablespoon" ,"Ounce", "Cup", "Quart","Gallon","Pound","Units"];

  // each recipe has associated measurements

  for ( i = 1 ; i < 601 ; i++)
  {
     no_ingredients = Math.floor( Math.random() * 5 ) + 3 ;
     ingred_id = Math.floor( Math.random() * 230 ) + 1;

     for ( j = 0 ; j < no_ingredients ; j ++){

          unit = Math.floor( Math.random() * 7 );
          numeric_measure = Math.floor( Math.random() * 8 ) + 1 ;

          if ( !(i == 1 && j== 0 ) )
          {
            contain_inserts += ',(' + i.toString() +','+ (ingred_id + j).toString()
            +  ',"' + base[unit] + '",' + numeric_measure.toString() + ')';
          }
          else
          {
            contain_inserts += '(' + i.toString() +','+ (ingred_id + j).toString()
            +  ',"' + base[unit] + '",' + numeric_measure.toString() + ')';
          }

     }
  }

}

function populate_prepare (){

  for( i = 1 ; i < 601 ; i++ )
  {
    if( i != 1)
    {
      prepare_inserts += ',(' + i.toString() + ',' + i.toString() + ')';
    }
    else
    {
      prepare_inserts += '(' + i.toString() + ',' + i.toString() + ')';

    }
  }

}

function populate_allergy()
{

  allergy = ["Fish Allergy", "Egg Allergy" , "Milk Allergy"];

  for (i = 0; i < allergy.length; i++)
  {
    if( i != 0 )
    {
      allergy_inserts += ',("' + allergy[i] +'")';

    }
    else
    {
      allergy_inserts += '("' + allergy[i] +'")';
    }
  }
}
function populate_host(){

  // person id , allergy id
  for(i = 1 ; i < 51 ; i++)
  {

      n = Math.floor( Math.random()*3) + 1;

      if ( i != 1 )
      {
        host_inserts += ',(' + i.toString() + ',' + n.toString() +')';
      }
      else
      {
        host_inserts += '(' + i.toString() + ',' + n.toString() +')';
      }
  }

}

function populate_reacts(){

  marked = false ;

  //seafood category
  for ( i = 151 ; i < 201 ; i++ )
  {
    if(marked)
    {
      reacts_inserts += ',( 1'+ ',' + i.toString() + ')';
    }
    else
    {
      reacts_inserts += '( 1'+ ',' + i.toString() + ')';
      marked = true ;
    }
  }

  //protein
  for( i = 51 ; i < 101 ; i ++ ){
    reacts_inserts += ',( 2' + ',' + i.toString() + ')';
  }

  // dairy
  for ( i = 1 ; i < 51 ; i++)
  {
    reacts_inserts += ',( 3'+ ',' + i.toString() + ')';
  }

}

function populate_image(){

// change
  img_inserts = "INSERT INTO image VALUES ";

  for( i = 1; i < 10 ; i++){

    title = "img_"+i.toString();
    description = faker.lorem.word();
    date = '2020-' + (Math.floor(Math.random()*12) + 1).toString() +
    '-' + (Math.floor(Math.random()*28) + 1).toString();


    if( i != 1 )
    {
      img_inserts += ',(' + i.toString() + ',' + i.toString() + ','
      + '"'+ title + '","' + description + '","' + date + '")';
    }
    else
    {
      img_inserts += '(' + i.toString() + ',' + i.toString() + ','
      + '"'+ title + '","' + description + '","' + date + '")';
    }
  }

  sql_output +=  img_inserts  + ';\n';


}

async function initialize_database () {

  let promise = new Promise((resolve, reject) => {


    for ( x = 0 ; x < 10 ; x++)
    {
      populate_person_own_inventory ();
    }


    for ( x = 0 ; x < 20 ; x ++)
    {
      recipe_nutrition_instructions ();
    }

    populate_meal_type ();
    populate_meals();
    populate_ingredients ();
    populate_measuremnt();
    populate_itemize ();
    populate_make ();
    contain();
    populate_allergy();
    populate_host();
    populate_reacts();
    resolve();
  });

  await promise;
  create_stored_procedures();

  output_sql_file (int_sql + "\n" + p_inserts + ";\n" + inventory_inserts + ";\n" + own_inserts + ";\n"+ nutrition_inserts
  + ";\n" + recipe_inserts + ";\n"+ direction_inserts + ";\n" + meal_type_inserts + ";\n" + meal_inserts +  ";\n"
   + schedule_inserts + ";\n"  + ingredient_inserts + ";\n"+ prepare_inserts + ";\n" + measurement_inserts + ";\n" + itemize_inserts + ";\n"
   + make_inserts + ";\n" + contain_inserts + ";\n"+ allergy_inserts + ";\n" + host_inserts + ";\n"
   + reacts_inserts + ";\n" +sql_output );

}

function create_stored_procedures(){
  sql_output += "DELIMITER //\n"
  +"CREATE PROCEDURE add_recipe( IN cal DECIMAL(10,2),\n"
  +"IN tot DECIMAL(10,2), IN sug DECIMAL(10,2) , IN sod DECIMAL(10,2), IN pro DECIMAL(10,2),\n"
  +"IN sat_fat DECIMAL(10,2), IN nam VARCHAR(150), IN ser DECIMAL(10,2))\n"
  +"BEGIN\n"
  +"DECLARE nut INT DEFAULT 0 ;\n"
  +"INSERT INTO nutrition (calories, total_fat, sugar ,\n"
  +"sodium , protein , saturated_fat) VALUES (cal , tot,sug , sod , pro, sat_fat );\n"
  +"SELECT count(*) INTO nut FROM nutrition;\n"
  +"INSERT INTO recipe (name , serving , nutrition_no) VALUES (nam , ser , nut);\n"
  +"END//\n"
  +"DELIMITER ;\n"

  +"DELIMITER //\n"
  +"CREATE PROCEDURE recipe_date( IN p_id INT , IN r_id INT )\n"
  +"BEGIN\n"
  +"SELECT * FROM make WHERE person_id = p_id AND recipe_id = r_id;\n"
  +"END //\n"
  +"DELIMITER ;\n"
  +"DELIMITER //\n"
  +"CREATE PROCEDURE generate_shopping_list( IN p_id INT , IN week_start_date DATE,\n"
  +"IN week_end_date DATE )\n"
  +"BEGIN\n"

  +"create view recipes_ingredients as select ingredient.ingred_id as ingred_id,\n"
  +"ingredient.name  as ingred_name, contain.recipe_id as recipe_id from ingredient\n"
  +"inner join contain on contain.ingred_id = ingredient.ingred_id;\n"
  +"select distinct t_2.ingred_name as Ingredient_Name from\n"
      +"(select ingred_id from itemize where inventory_id in\n"
      +"(select inventory_id from own where person_id = p_id) and inStock='N') as t_1 inner join\n"
      +"(select ingred_name, ingred_id from recipes_ingredients where recipe_id in\n"
      +"(select recipe_id from prepare where meal_id in (\n"
      +"select meal_id from schedule where person_id = p_id and (meal_date between\n"
      +"week_start_date and week_end_date)))) as t_2  on t_1.ingred_id = t_2.ingred_id;\n"
  +"drop view recipes_ingredients; \n"
  +"END //\n"
  +"DELIMITER ;\n"

  +"DELIMITER //\n"
  +"CREATE PROCEDURE total_items( IN p_id INT )\n"
  +"BEGIN\n"

  +"select count(ingred_id) as total_items from itemize where inventory_id in\n"
  +"(select inventory_id from inventory where inventory_id in\n"
  +"(select inventory_id from own where person_id = p_id));\n"
  +"END //\n"
  +"DELIMITER ;\n"

  +"DELIMITER //\n"

  +"CREATE PROCEDURE View_Meal_Plan( IN p_id INT , IN week_start_date DATE , week_end_date DATE)\n"
  +"BEGIN\n"

  +"select meal.name as meal_name , t_2.meal_type as meal_type , t_2.meal_date as meal_date from\n"
  +"(select t_1.meal_id as meal_id , type.meal_type as meal_type, t_1.meal_date as meal_date from\n"
  +"(select meal_id , type_no , meal_date from schedule\n"
  +"where person_id = p_id and meal_date between week_start_date and week_end_date )\n"
  +"as t_1 inner join type on type.type_no = t_1.type_no) as t_2 inner join  meal\n"
  +"on meal.meal_id = t_2.meal_id;\n"
  +"END //\n"
  +"DELIMITER ;\n"

  +"DELIMITER //\n"
  +"CREATE PROCEDURE schedule_calorie_count( IN p_id INT , IN week_start_date DATE , IN week_end_date DATE)\n"
  +"BEGIN\n"

  +"select SUM(calories) as Total_Calories from nutrition\n"
              +"where nutrition_no in ( select nutrition_no from recipe where\n"
              +"recipe_id in (select recipe_id from prepare where meal_id in\n"
              +"(select meal_id from schedule where person_id = p_id and\n"
              +"meal_date between week_start_date and week_end_date)));\n"

  +"END //\n"
  +"DELIMITER ;\n";
}
function output_sql_file ( file ){

 let writeStream = fs.createWriteStream('meal_system.sql');
  writeStream.on('finish', () => {
    console.log('wrote all data to file');
  });
  writeStream.write(file);
  // close the stream
   writeStream.end();
}
