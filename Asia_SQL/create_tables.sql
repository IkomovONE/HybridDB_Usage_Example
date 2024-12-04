CREATE TABLE "Orders" (
	"id"	INTEGER,
	"UserID"	TEXT,
	"SellerName"	TEXT,
	"ProductNames"	TEXT,
	"Quantity"	INTEGER,
	"OrderDate"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "Products" (
	"id"	INT,
	"name"	VARCHAR(100) NOT NULL,
	"price"	DECIMAL(10, 2) NOT NULL,
	"stock"	INT NOT NULL,
	"category"	VARCHAR(100) NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "Sellers" (
	"id"	INT,
	"name"	VARCHAR(100) NOT NULL,
	"store_name"	VARCHAR(100) NOT NULL,
	"email"	VARCHAR(100) NOT NULL UNIQUE,
	"sales_region"	VARCHAR(100) NOT NULL,
	"created_at"	DATE NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "Users" (
	"id"	INT,
	"name"	VARCHAR(100) NOT NULL,
	"email"	VARCHAR(100) NOT NULL UNIQUE,
	"location"	VARCHAR(100) NOT NULL,
	"created_at"	DATE NOT NULL,
	PRIMARY KEY("id")
);