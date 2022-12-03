-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-12-03 19:08:17.301

-- tables
-- Table: Customers
CREATE TABLE Customers (
    customer_id int  NOT NULL,
    loyalty_pts int  NOT NULL,
    CONSTRAINT Customers_pk PRIMARY KEY (customer_id)
);

-- Table: Reservations
CREATE TABLE Reservations (
    date date  NOT NULL,
    time time  NOT NULL,
    seats int  NOT NULL,
    additional_requests text  NOT NULL,
    customer_id int  NOT NULL,
    restaurant_id int  NOT NULL,
    CONSTRAINT Reservations_pk PRIMARY KEY (customer_id,restaurant_id,date)
);

-- Table: Restaurants
CREATE TABLE Restaurants (
    restaurant_id int  NOT NULL,
    location text  NOT NULL,
    menu text  NOT NULL,
    open_hour time  NOT NULL,
    close_hour time  NOT NULL,
    CONSTRAINT Restaurants_pk PRIMARY KEY (restaurant_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    name text  NOT NULL,
    email text  NOT NULL,
    phone bigint  NOT NULL,
    CONSTRAINT user_id PRIMARY KEY (user_id)
);

-- foreign keys
-- Reference: Customers_Users (table: Customers)
ALTER TABLE Customers ADD CONSTRAINT Customers_Users
    FOREIGN KEY (customer_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Reservations_Customers (table: Reservations)
ALTER TABLE Reservations ADD CONSTRAINT Reservations_Customers
    FOREIGN KEY (customer_id)
    REFERENCES Customers (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Reservations_Restaurants (table: Reservations)
ALTER TABLE Reservations ADD CONSTRAINT Reservations_Restaurants
    FOREIGN KEY (restaurant_id)
    REFERENCES Restaurants (restaurant_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Restaurants_Users (table: Restaurants)
ALTER TABLE Restaurants ADD CONSTRAINT Restaurants_Users
    FOREIGN KEY (restaurant_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

