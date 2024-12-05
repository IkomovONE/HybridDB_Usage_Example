# HybridDB_Usage_Example


**Author**: Daniil Komov

## Project Overview
This repository serves as a usage example of hybrid system of 2 databases. The repository contains dummy data for each database and a frontend program which accesses MongoDB and SQL to display data and allows user to insert, delete or edit the data. The program serves as a browser program for imaginary e-commerce store with database locations in Europe and Asia. MongoDB(Europe) has been used as noSQL database, while SQLite has been used to create SQL database(Asia). This mini-project serves as a good example of how both noSQL and SQL databases can be utilized for one purpose and in one application.

## Usage
### Running

To run the program, you will need to install Python, venv and have mongoDB connection, on port 27017. 

**MongoDB:** you will need to manually create a connection(port mentioned above) using, for example, mongoDB Compass app, then create a database "Europe", create 4 tables (Users, Sellers, Orders, Products) and paste the dummy data using, for example, JSON templates found in "EU_NoSQL(MongoDB)" folder.

In case the connection port for the MongoDB is different, change it in store.py code file: find a line where connection to mongoDB is being established, and write your own port number.

**SQLite database:** the database is already in the "instance" folder, however, source code for creating tables using SQL is in the "Asia_SQL" folder. Also there's dummy data in JSON files.

Set virtual environment, install needed libraries (e.g. Flask, pymongo) and then run this command:

```bash
flask --app store run
```
Then go to browser and enter URL given in terminal. 

### Locations

The page is showing all databases by default. You can change the location using the selector on the top of the page. Then by pressing submit the data will change, as it will be gathered from another database.

### Inserting data

You can insert data by clicking "Insert data", then choosing database, table, and inserting/writing the list of entries in the field, then submitting. **Important:** for successful insertion the format of the template and strinct column names have to be followed, the insertion string has to be in format [{}, {}, {}] and have relevant JSON data inside. Also the _id (or id, refer to the specific database) value has to be unique. After submitting the status will then be displayed. If you want to come back to the home page you can click the big button.

### Editing data

To edit specific row, click "edit data", then choose your database and table. Then enter ID of the row to update. Click submit. If the entry is found, you will see next page where you will be able to update the JSON line of the entry. **Important:** don't change the JSON structure, rather just the values of the relations. Click submit. The status will then be displayed. If you want to come back to the home page you can click the big button.

### Deleting data

Deleting a specific table row is very simple: click "delete data", in the next page select the database, table, and write the ID of the table entry to be deleted. Press "submit". The status will then be displayed. If you want to come back to the home page you can click the big button.

### Demonstration video

You can access a demo video using this link:

https://youtu.be/KZCXM9M_Fw8


