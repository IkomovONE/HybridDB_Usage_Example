from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pymongo import MongoClient           #Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy
import json



app = Flask(__name__)    #Using Flask to initialize frontend server


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

class Seller(db.Model):
    __tablename__ = 'Sellers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    sales_region = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(100), nullable=False)  # Assuming TEXT maps to String
    sellerName = db.Column(db.String(100), nullable=False)
    productNames = db.Column(db.String(1000), nullable=False)  # To store multiple product names as a comma-separated string
    Quantity = db.Column(db.Integer, nullable=False)
    orderDate = db.Column(db.String(100), nullable=False)

client = MongoClient("localhost:27017")     #Setting up mongoDB to connect to databases

europe_db = client["Europe"]     #Establishing 3 databases, 3 continents



users_eu = europe_db["Users"]     #users
sellers_eu = europe_db["Sellers"]   #sellers
products_eu = europe_db["Products"]   #products
orders_eu = europe_db["Orders"]   #orders



@app.route("/", methods=["GET", "POST"])    #creating a route
def home():

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

    for i in users_SQL:
        users.append(i)

    for i in sellers_SQL:
        sellers.append(i)

    for i in orders_SQL:
        orders.append(i)

    for i in products_SQL:
        products.append(i)

    db_choice= "All databases"

    render_template("index.html", users=users, sellers=sellers, products=products, orders=orders, db_choice=db_choice) 



    



    if request.method == "POST":

        

        db_choice = request.form["db_choice"]   #Using POST method

        
        if db_choice == "Europe(noSQL)":
            
            users = list(users_eu.find({}))  
            sellers = list(sellers_eu.find({}))      
            products = list(products_eu.find({}))
            orders = list(orders_eu.find({}))

        elif db_choice == "Asia(SQL)":
        # Fetch data from SQL tables using SQLAlchemy
            users = [
                {
                    "_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "location": user.location,
                    "created_at": user.created_at.strftime('%Y-%m-%d'),
                }
                for user in User.query.all()
            ]

            sellers = [
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

            products = [
                {
                    "_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "stock": product.stock,
                    "category": product.category,
                }
                for product in Product.query.all()
            ]

            orders = [
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

        elif db_choice == "All databases":
            
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

            for i in users_SQL:
                users.append(i)

            for i in sellers_SQL:
                sellers.append(i)

            for i in orders_SQL:
                orders.append(i)

            for i in products_SQL:
                products.append(i)


             

    return render_template("index.html", users=users, sellers=sellers, products=products, orders=orders, db_choice=db_choice)  









@app.route("/create", methods=["GET", "POST"])

def create():

    status= ""

    if request.method == "POST":

        db_choice = request.form["db_choice"]

        table_choice = request.form["table_choice"]

        json_lines= request.form["json_lines"]

        

        


        try:
            # Convert JSON string to a Python list
            data_list = json.loads(json_lines)



            if db_choice == "Europe(noSQL)":

                

                if table_choice== "Users":
                    
                    users_eu.insert_many(data_list)

                elif table_choice== "Sellers":
                    
                    sellers_eu.insert_many(data_list)

                elif table_choice== "Orders":
                    
                    orders_eu.insert_many(data_list)

                elif table_choice== "Products":
                    
                    products_eu.insert_many(data_list)



            if db_choice == "Asia(SQL)":

                

                if table_choice== "Users":
                    
                    for row in data_list:
                        created_at_date = datetime.strptime(row["created_at"], "%Y-%m-%d").date()

                        new_user = User(
                            id=row.get("_id"),  # Use .get() to avoid KeyErrors
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
                        new_product = Product(
                            id=entry.get("_id"),
                            name=entry["name"],
                            price=entry["price"],
                            stock=entry["stock"],
                            category=created_at_date
                        )
                        db.session.add(new_product)

                elif table_choice== "Products":
                    
                    for entry in data_list:

                        created_at_date = datetime.strptime(entry["created_at"], "%Y-%m-%d").date()
                        new_order = Order(
                            id=entry.get("_id"),
                            user_id=entry["user_id"],
                            seller_name=entry["seller_name"],
                            product_names=entry["product_names"],
                            quantity=entry["quantity"],
                            order_date=created_at_date
                        )
                        db.session.add(new_order)

                    

                
                db.session.commit()
                status= "true"

        except json.JSONDecodeError as e:
            print(e)
            status = "false"




        pass
    return render_template("create.html", success=status)











@app.route("/edit", methods=["GET", "POST"])
def edit():
    

    if request.method == "POST":

        db_choice = request.form["db_choice"]

        table_choice = request.form["table_choice"]

        row_ID = request.form["row_ID"]

        try:
            # Fetch data based on database and table choice
            if db_choice == "Europe(noSQL)":
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
                    record = User.query.get(row_ID)  # Fetch SQLAlchemy row
                    record = {
                        "id": record.id,
                        "name": record.name,
                        "email": record.email,
                        "location": record.location,
                        "created_at": record.created_at.strftime("%Y-%m-%d")
                    }

                if table_choice == "Sellers":
                    record = Seller.query.get(row_ID)  # Fetch SQLAlchemy row
                    record = {

                        "id": record.id,
                        "name": record.name,
                        "store_name": record.store_name,
                        "email": record.email,
                        "sales_region": record.sales_region,
                        "created_at": record.created_at.strftime('%Y-%m-%d'),
     
                    }

                if table_choice == "Orders":
                    record = Order.query.get(row_ID)  # Fetch SQLAlchemy row
                    record = {
                        "id": record.id,
                        "userId": record.userID,
                        "sellerName": record.sellerName,
                        "ProductNames": record.productNames,
                        "Quantity": record.Quantity,
                        "Order_Date": record.orderDate,
                    }

                if table_choice == "Products":
                    record = Product.query.get(row_ID)  # Fetch SQLAlchemy row
                    record = {

                        "id": record.id,
                        "name": record.name,
                        "price": record.price,
                        "stock": record.stock,
                        "category": record.category,
                    }

            if record:
                return render_template("update-form.html", record=record, db_choice=db_choice, table_choice=table_choice)
            else:
                return "Record not found", 404

        except Exception as e:
            return f"Error: {e}", 500

    return render_template("edit.html") 



@app.route("/update", methods=["POST"])
def update():
    db_choice = request.form["db_choice"]
    table_choice = request.form["table_choice"]
    json_data = request.form["json_data"]
    status= ""

    try:
        # Parse JSON input
        updated_data = json.loads(json_data)

        if db_choice == "Europe(noSQL)":
            if table_choice == "Users":
                result = users_eu.update_one(
                    {"_id": updated_data["_id"]},  # Match by ID
                    {"$set": updated_data}         # Update fields
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

            if table_choice == "Sellers":
                result = sellers_eu.update_one(
                    {"_id": updated_data["_id"]},  # Match by ID
                    {"$set": updated_data}         # Update fields
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

            if table_choice == "Orders":
                result = orders_eu.update_one(
                    {"_id": updated_data["_id"]},  # Match by ID
                    {"$set": updated_data}         # Update fields
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

            if table_choice == "Products":
                result = products_eu.update_one(
                    {"_id": updated_data["_id"]},  # Match by ID
                    {"$set": updated_data}         # Update fields
                )
                if result.matched_count > 0:
                    status= "true" 
                else:
                    status= "false"

        elif db_choice == "Asia(SQL)":

            if table_choice == "Users":
                record = User.query.get(updated_data["id"])  # Match by ID
                if record:
                    record.name = updated_data["name"]
                    record.email = updated_data["email"]
                    record.location = updated_data["location"]
                    record.created_at = datetime.strptime(updated_data["created_at"], "%Y-%m-%d").date()
                    db.session.commit()
                    status= "true"  
                else:
                    status= "false"  

            if table_choice == "Sellers":
                record = Seller.query.get(updated_data["id"])  # Match by ID
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
                record = Order.query.get(updated_data["id"])  # Match by ID
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
                record = Product.query.get(updated_data["id"])  # Match by ID
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
        return f"Invalid JSON: {e}", 400
    except Exception as e:
        return f"Error: {e}", 500
    

    return render_template("update-form.html", status= status, record= "success") 







@app.route("/delete", methods=["GET", "POST"])

def delete():

    status= ""

    if request.method == "POST":

        db_choice = request.form["db_choice"]

        table_choice = request.form["table_choice"]

        row_ID = request.form["row_ID"]
        
        
        if db_choice == "Europe(noSQL)":

            if table_choice== "Users":
                    
                del_status = users_eu.delete_one({"_id": row_ID})

                if del_status.deleted_count > 0:
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
                row = User.query.get(row_ID)  # Find by primary key
                if row:

                    db.session.delete(row)

                    db.session.commit()

                    status= "true"
                else:
                    status= "false"
            
            elif table_choice== "Sellers":

                row = Seller.query.get(row_ID)  # Find by primary key
                if row:

                    db.session.delete(row)

                    db.session.commit()
                    status= "true"
                else:
                    status= "false"

                
                 

            elif table_choice== "Orders":

                row = Order.query.get(row_ID)  # Find by primary key
                if row:

                    db.session.delete(row)

                    db.session.commit()
                    status= "true"
                else:
                    status= "false"
                    
                    

            elif table_choice== "Products":

                row = Product.query.get(row_ID)  # Find by primary key
                if row:

                    db.session.delete(row)

                    db.session.commit()
                    status= "true"
                else:
                    status= "false"
                    
                    



        pass
    return render_template("delete.html", success=status)




if __name__ == "__main__":
    app.run(debug=True)    #running the app






#RUN USING flask --app store run


