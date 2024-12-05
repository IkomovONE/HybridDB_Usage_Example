from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pymongo import MongoClient           #Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy
import json



app = Flask(__name__)    #Using Flask to initialize frontend server


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asia.db'   ##Connecting to SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False          

db = SQLAlchemy(app)   ## Using SQLAlchemy for managing SQL database


##Next 4 classes represent typical DB entry in each of the 4 SQL DB tables

class User(db.Model):     
    __tablename__ = 'Users'   ## Table "Users"

    id = db.Column(db.Integer, primary_key=True)   ## id column

    name = db.Column(db.String(100), nullable=False)  ## name column

    email = db.Column(db.String(100), unique=True, nullable=False)  ## email column

    location = db.Column(db.String(100), nullable=False)  ## location column

    created_at = db.Column(db.Date, nullable=False)  ## date column

class Seller(db.Model):
    __tablename__ = 'Sellers'    ## Table "Sellers"

    id = db.Column(db.Integer, primary_key=True)   ## id column

    name = db.Column(db.String(100), nullable=False)   ## name column

    store_name = db.Column(db.String(100), nullable=False)  ## store name column

    email = db.Column(db.String(100), unique=True, nullable=False)  ## email column

    sales_region = db.Column(db.String(100), nullable=False)  ## sales region column

    created_at = db.Column(db.Date, nullable=False)  ## date column

class Product(db.Model):
    __tablename__ = 'Products'   ## Table "Products"

    id = db.Column(db.Integer, primary_key=True)    ## id column

    name = db.Column(db.String(100), nullable=False)   ## name column

    price = db.Column(db.Float, nullable=False)    ## price column

    stock = db.Column(db.Integer, nullable=False)    ## stock column

    category = db.Column(db.String(100), nullable=False)    ## category column


class Order(db.Model):
    __tablename__ = 'Orders'     ## Table "Orders"

    id = db.Column(db.Integer, primary_key=True)   ## id column

    userID = db.Column(db.String(100), nullable=False)    ## userID column

    sellerName = db.Column(db.String(100), nullable=False)   ## seller name column

    productNames = db.Column(db.String(1000), nullable=False)  ## products names column

    Quantity = db.Column(db.Integer, nullable=False)   ## quantity column

    orderDate = db.Column(db.String(100), nullable=False)  ## date column



##Initializing mongoDB


client = MongoClient("localhost:27017")     #Setting up mongoDB to connect to database

europe_db = client["Europe"]     #Establishing "europe" database



users_eu = europe_db["Users"]     #users
sellers_eu = europe_db["Sellers"]   #sellers
products_eu = europe_db["Products"]   #products
orders_eu = europe_db["Orders"]   #orders



#### Main route (main page)

@app.route("/", methods=["GET", "POST"])    ## Establishing route
def home():

    #Establishing default queries for showing all databases even if the choice for displaying specific thing hasn't been made

    users = list(users_eu.find({}))           ## find all user entries
    sellers = list(sellers_eu.find({}))      ## find all sellers entries
    products = list(products_eu.find({}))    ## find all products entries
    orders = list(orders_eu.find({}))       ## find all orders entries



    users_SQL = [    ## creating SQL query for user
        {
            "_id": user.id,
            "name": user.name,
            "email": user.email,
            "location": user.location,
            "created_at": user.created_at.strftime('%Y-%m-%d'),
        }
        for user in User.query.all()
    ]

    sellers_SQL = [      ## creating SQL query for sellers
        {
            "_id": seller.id,
            "s_name": seller.name,
            "store_name": seller.store_name,
            "email": seller.email,
            "sales_region": seller.sales_region,
            "created_at": seller.created_at.strftime('%Y-%m-%d'),
        }
        for seller in Seller.query.all()
    ]

    products_SQL = [     ## creating SQL query for products
        {
            "_id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "category": product.category,
        }
        for product in Product.query.all()
    ]

    orders_SQL = [      ## creating SQL query for orders
        {
            "_id": order.id,
            "user_id": order.userID,
            "seller_name": order.sellerName,
            "products_names": order.productNames,
            "quantity": order.Quantity,
            "order_date": order.orderDate,
        }
        for order in Order.query.all()
    ]

    for i in users_SQL:     #adding SQL entries together with noSQL
        users.append(i)

    for i in sellers_SQL:
        sellers.append(i)

    for i in orders_SQL:
        orders.append(i)

    for i in products_SQL:
        products.append(i)

    db_choice= "All databases"    #default choice

    render_template("index.html", users=users, sellers=sellers, products=products, orders=orders, db_choice=db_choice) #rendering index page



    



    if request.method == "POST":  #using POST method

        

        db_choice = request.form["db_choice"]   #getting info from request HTML form

        
        if db_choice == "Europe(noSQL)":   #noSQL query
            
            users = list(users_eu.find({}))  
            sellers = list(sellers_eu.find({}))      
            products = list(products_eu.find({}))
            orders = list(orders_eu.find({}))

        elif db_choice == "Asia(SQL)":
        
            users = [        ## creating SQL query for users
                {
                    "_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "location": user.location,
                    "created_at": user.created_at.strftime('%Y-%m-%d'),
                }
                for user in User.query.all()
            ]

            sellers = [         ## creating SQL query for sellers
                {
                    "_id": seller.id,
                    "s_name": seller.name,
                    "store_name": seller.store_name,
                    "email": seller.email,
                    "sales_region": seller.sales_region,
                    "created_at": seller.created_at.strftime('%Y-%m-%d'),
                }
                for seller in Seller.query.all()
            ]

            products = [         ## creating SQL query for products
                {
                    "_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "stock": product.stock,
                    "category": product.category,
                }
                for product in Product.query.all()
            ]

            orders = [        ## creating SQL query for orders
                {
                    "_id": order.id,
                    "user_id": order.userID,
                    "seller_name": order.sellerName,
                    "products_names": order.productNames,
                    "quantity": order.Quantity,
                    "order_date": order.orderDate,
                }
                for order in Order.query.all()
            ]

        elif db_choice == "All databases":    ##All databases query, both SQL and noSQL
            
            users = list(users_eu.find({}))  
            sellers = list(sellers_eu.find({}))      
            products = list(products_eu.find({}))
            orders = list(orders_eu.find({}))



            users_SQL = [
                {
                    "_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "location": user.location,
                    "created_at": user.created_at.strftime('%Y-%m-%d'),
                }
                for user in User.query.all()
            ]

            sellers_SQL = [
                {
                    "_id": seller.id,
                    "s_name": seller.name,
                    "store_name": seller.store_name,
                    "email": seller.email,
                    "sales_region": seller.sales_region,
                    "created_at": seller.created_at.strftime('%Y-%m-%d'),
                }
                for seller in Seller.query.all()
            ]

            products_SQL = [
                {
                    "_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "stock": product.stock,
                    "category": product.category,
                }
                for product in Product.query.all()
            ]

            orders_SQL = [
                {
                    "_id": order.id,
                    "user_id": order.userID,
                    "seller_name": order.sellerName,
                    "products_names": order.productNames,
                    "quantity": order.Quantity,
                    "order_date": order.orderDate,
                }
                for order in Order.query.all()
            ]

            for i in users_SQL:    ##Adding SQL rows to noSQL
                users.append(i)

            for i in sellers_SQL:
                sellers.append(i)

            for i in orders_SQL:
                orders.append(i)

            for i in products_SQL:
                products.append(i)


             

    return render_template("index.html", users=users, sellers=sellers, products=products, orders=orders, db_choice=db_choice)  ##Rendering index page






#### Create route (making new entries)


@app.route("/create", methods=["GET", "POST"])   ##This route is for inserting rows

def create():

    status= ""   ##Implementing status variable as a simple indication of either success or error

    if request.method == "POST":   ##using POST method

        db_choice = request.form["db_choice"]   ##Getting choices information about db choice, table choice and new entry string

        table_choice = request.form["table_choice"]

        json_lines= request.form["json_lines"]

        

        


        try:
            
            data_list = json.loads(json_lines)   #Trying to convert list string to JSON



            if db_choice == "Europe(noSQL)":   

                

                if table_choice== "Users":
                    
                    users_eu.insert_many(data_list)   ##Inserting the data to noSQL

                elif table_choice== "Sellers":
                    
                    sellers_eu.insert_many(data_list)

                elif table_choice== "Orders":
                    
                    orders_eu.insert_many(data_list)

                elif table_choice== "Products":
                    
                    products_eu.insert_many(data_list)



            if db_choice == "Asia(SQL)":

                

                if table_choice== "Users":
                    
                    for row in data_list:
                        created_at_date = datetime.strptime(row["created_at"], "%Y-%m-%d").date()  ##Parsing date into specific format

                        new_user = User(
                            id=row.get("_id"),  # Inserting to SQL DB using new object initialization through earlier made class
                            name=row["name"],
                            email=row["email"],
                            location=row["location"],
                            created_at=created_at_date
                        )
                        db.session.add(new_user)

                elif table_choice== "Sellers":
                    
                    for entry in data_list:

                        created_at_date = datetime.strptime(entry["created_at"], "%Y-%m-%d").date()
                        new_seller = Seller(
                            id=entry.get("_id"),
                            name=entry["name"],
                            store_name=entry["store_name"],
                            email=entry["email"],
                            sales_region=entry["sales_region"],
                            created_at=created_at_date
                        )
                        db.session.add(new_seller)

                elif table_choice== "Orders":
                    
                    for entry in data_list:

                        created_at_date = datetime.strptime(entry["created_at"], "%Y-%m-%d").date()
                        new_order = Product(
                            id=entry.get("_id"),
                            name=entry["name"],
                            price=entry["price"],
                            stock=entry["stock"],
                            category=created_at_date
                        )
                        db.session.add(new_order)

                elif table_choice== "Products":
                    
                    for entry in data_list:

                        created_at_date = datetime.strptime(entry["created_at"], "%Y-%m-%d").date()
                        new_product = Order(
                            id=entry.get("_id"),
                            user_id=entry["user_id"],
                            seller_name=entry["seller_name"],
                            product_names=entry["product_names"],
                            quantity=entry["quantity"],
                            order_date=created_at_date
                        )
                        db.session.add(new_product)

                    

                
                db.session.commit()  ##Commiting changes to SQL database
                status= "true"

        except json.JSONDecodeError as e:   #Simple error handling
            print(e)
            status = "false"




        pass
    return render_template("create.html", success=status)   ##Rendering row insertion html page 







#### Edit route (for updating existing row)

##There are 2 routes used for editing: the one below is for searching for the specific table row, next one is for editing it. 



@app.route("/edit", methods=["GET", "POST"])
def edit():
    

    if request.method == "POST":

        db_choice = request.form["db_choice"]   ##Getting form information

        table_choice = request.form["table_choice"]

        row_ID = request.form["row_ID"]

        try:
            
            if db_choice == "Europe(noSQL)":   ##Finding the row in mongoDB
                if table_choice == "Users":
                    record = users_eu.find_one({"_id": row_ID}) 
                elif table_choice == "Sellers":
                    record = sellers_eu.find_one({"_id": row_ID}) 
                elif table_choice == "Orders":
                    record = orders_eu.find_one({"_id": row_ID}) 
                elif table_choice == "Products":
                    record = products_eu.find_one({"_id": row_ID})  

            elif db_choice == "Asia(SQL)":
                if table_choice == "Users":
                    record = User.query.get(row_ID)  ## Finding the row in SQL database
                    record = {     ##Initializing simple structure for fetching
                        "id": record.id,
                        "name": record.name,
                        "email": record.email,
                        "location": record.location,
                        "created_at": record.created_at.strftime("%Y-%m-%d")
                    }

                if table_choice == "Sellers":
                    record = Seller.query.get(row_ID)  
                    record = {

                        "id": record.id,
                        "name": record.name,
                        "store_name": record.store_name,
                        "email": record.email,
                        "sales_region": record.sales_region,
                        "created_at": record.created_at.strftime('%Y-%m-%d'),
     
                    }

                if table_choice == "Orders":
                    record = Order.query.get(row_ID)  
                    record = {
                        "id": record.id,
                        "userId": record.userID,
                        "sellerName": record.sellerName,
                        "ProductNames": record.productNames,
                        "Quantity": record.Quantity,
                        "Order_Date": record.orderDate,
                    }

                if table_choice == "Products":
                    record = Product.query.get(row_ID)  
                    record = {

                        "id": record.id,
                        "name": record.name,
                        "price": record.price,
                        "stock": record.stock,
                        "category": record.category,
                    }

            if record:
                return render_template("update-form.html", record=record, db_choice=db_choice, table_choice=table_choice)  ##Rendering update form page
            else:
                return "Record not found", 404   ##Showing that the record is not found

        except Exception as e:
            return f"Error: {e}", 500  ##Showing error in case of an exception

    return render_template("edit.html") ##Rendering initial edit search page



#### Update route (for updating existing row)

@app.route("/update", methods=["POST"])   ##this route is for updating the entry that has been found
def update():
    db_choice = request.form["db_choice"]
    table_choice = request.form["table_choice"]
    json_data = request.form["json_data"]
    status= ""   #status for either success or error

    try:
        
        updated_data = json.loads(json_data)   #trying to parse the edited string to JSON

        if db_choice == "Europe(noSQL)":    ##Again, using if condition for doing either SQL or noSQL work

            if table_choice == "Users":    

                result = users_eu.update_one(    ##Updating the existing entry using _id
                    {"_id": updated_data["_id"]},  
                    {"$set": updated_data}         
                )
                if result.matched_count > 0:   ##Determining status based on the result
                    status= "true" 
                else:
                    status= "false"

            if table_choice == "Sellers":
                result = sellers_eu.update_one(
                    {"_id": updated_data["_id"]},  
                    {"$set": updated_data}         
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

            if table_choice == "Orders":
                result = orders_eu.update_one(
                    {"_id": updated_data["_id"]},  
                    {"$set": updated_data}         
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

            if table_choice == "Products":
                result = products_eu.update_one(
                    {"_id": updated_data["_id"]},  
                    {"$set": updated_data}         
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

        elif db_choice == "Asia(SQL)":

            if table_choice == "Users":

                record = User.query.get(updated_data["id"])  ##Getting user record using id

                if record:   ##If record is found set new values
                    record.name = updated_data["name"]
                    record.email = updated_data["email"]
                    record.location = updated_data["location"]
                    record.created_at = datetime.strptime(updated_data["created_at"], "%Y-%m-%d").date()
                    db.session.commit()  ##Commiting the update
                    status= "true"  
                else:
                    status= "false"  

            if table_choice == "Sellers":
                record = Seller.query.get(updated_data["id"])  
                if record:
                    record.id = updated_data["id"]
                    record.name = updated_data["name"]
                    record.store_name = updated_data["store_name"]
                    record.email = updated_data["email"]
                    record.sales_region = updated_data["sales_region"]
                    record.created_at = datetime.strptime(updated_data["created_at"], "%Y-%m-%d").date()
                    db.session.commit()
                    status= "true"  
                else:
                    status= "false"  

            if table_choice == "Orders":
                record = Order.query.get(updated_data["id"])  
                if record:
                    record.id = updated_data["id"]
                    record.userID = updated_data["userID"]
                    record.sellerName = updated_data["sellerName"]
                    record.Quantity = updated_data["Quantity"]
                    record.order_date = datetime.strptime(updated_data["orderDate"], "%Y-%m-%d").date()
                    db.session.commit()
                    status= "true"  
                else:
                    status= "false"  

            if table_choice == "Products":
                record = Product.query.get(updated_data["id"])  
                if record:
                    record.id = updated_data["id"]
                    record.name = updated_data["name"]
                    record.price = updated_data["price"]
                    record.stock = updated_data["stock"]
                    record.category = updated_data["category"]
                    db.session.commit()
                    status= "true"  
                else:
                    status= "false"  

    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}", 400   ##Showing error if JSON is invalid
    except Exception as e:
        return f"Error: {e}", 500   ##Showing error in case of other exception error
    

    return render_template("update-form.html", status= status, record= "success")  ##Rendering update-form page









#### Delete route


@app.route("/delete", methods=["GET", "POST"])   ##Route used to delete rows based on ID

def delete():   

    status= ""

    if request.method == "POST":

        db_choice = request.form["db_choice"]

        table_choice = request.form["table_choice"]

        row_ID = request.form["row_ID"]   ##Getting ID of the row to be deleted
        
        
        if db_choice == "Europe(noSQL)":

            if table_choice== "Users":
                    
                del_status = users_eu.delete_one({"_id": row_ID})  ##Deleting the row based on the given ID

                if del_status.deleted_count > 0:   ##Determining status based on deletion status
                    status= "true"
                else:
                    status= "false"

            elif table_choice== "Sellers":
                    
                del_status = sellers_eu.delete_one({"_id": row_ID})

                if del_status.deleted_count > 0:
                    status= "true"
                else:
                    status= "false"

            elif table_choice== "Orders":
                    
                del_status = orders_eu.delete_one({"_id": row_ID})
                if del_status.deleted_count > 0:
                    status= "true"
                else:
                    status= "false"

            elif table_choice== "Products":
                    
                del_status = products_eu.delete_one({"_id": row_ID})
                if del_status.deleted_count > 0:
                    status= "true"
                else:
                    status= "false"

                

        if db_choice == "Asia(SQL)":
            
            if table_choice== "Users":
                row = User.query.get(row_ID)  ##Getting the row with ID
                if row:

                    db.session.delete(row)  ##Deleting the row

                    db.session.commit()  ##Commiting changes

                    status= "true"
                else:
                    status= "false"
            
            elif table_choice== "Sellers":

                row = Seller.query.get(row_ID)  
                if row:

                    db.session.delete(row)

                    db.session.commit()
                    status= "true"
                else:
                    status= "false"

                
                 

            elif table_choice== "Orders":

                row = Order.query.get(row_ID)  
                if row:

                    db.session.delete(row)

                    db.session.commit()
                    status= "true"
                else:
                    status= "false"
                    
                    

            elif table_choice== "Products":

                row = Product.query.get(row_ID)  
                if row:

                    db.session.delete(row)

                    db.session.commit()
                    status= "true"
                else:
                    status= "false"
                    
                    



        pass
    return render_template("delete.html", success=status)  ##Rendering the delete form page




if __name__ == "__main__":
    app.run(debug=True)    #running the app






#RUN USING flask --app store run


