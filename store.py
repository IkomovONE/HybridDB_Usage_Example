from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient           #Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy



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
    users, sellers, products, orders = None, None, None, None



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
                    "s_id": seller.id,
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
                    "s_id": seller.id,
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


            





            

    
            
        

    return render_template("index.html", users=users, sellers=sellers, products=products, orders=orders)  #rendering using index.html


@app.route('/sql/users', methods=['GET'])
def get_sql_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'location': user.location,
        'created_at': user.created_at.strftime('%Y-%m-%d')
    } for user in users])

if __name__ == "__main__":
    app.run(debug=True)    #running the app




#RUN USING flask --app store run


