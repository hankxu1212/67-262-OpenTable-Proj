-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-12-04 19:39:36.338

-- tables
-- Table: Customers
CREATE TABLE Customers (
    customer_id int  NOT NULL,
    loyalty_pts int  NOT NULL,
    recommendations int  NULL,
    CONSTRAINT Customers_pk PRIMARY KEY (customer_id)
);

-- Table: Reservations
CREATE TABLE Reservations (
    date date  NOT NULL,
    time time  NOT NULL,
    seats int  NOT NULL,
    additional_requests text  NULL,
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

-- Table: Reviews
CREATE TABLE Reviews (
    review_id int  NOT NULL,
    comment text  NOT NULL,
    rating int  NOT NULL,
    post_time timestamp  NOT NULL DEFAULT LOCALTIMESTAMP(0),
    posted_by int  NOT NULL,
    posted_to int  NOT NULL,
    CONSTRAINT Reviews_pk PRIMARY KEY (review_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    name text  NOT NULL,
    email text  NOT NULL,
    phone bigint  NOT NULL,
    CONSTRAINT user_id PRIMARY KEY (user_id)
);

-- Table: cuisines
CREATE TABLE cuisines (
    cuisine_name text  NOT NULL,
    CONSTRAINT cuisines_pk PRIMARY KEY (cuisine_name)
);

-- Table: labels
CREATE TABLE labels (
    restaurant_id int  NOT NULL,
    cuisine_name text  NOT NULL,
    CONSTRAINT labels_pk PRIMARY KEY (restaurant_id,cuisine_name)
);

-- Table: waitlists
CREATE TABLE waitlists (
    customer_id int  NOT NULL,
    restaurant_id int  NOT NULL,
    date date  NOT NULL,
    time time  NOT NULL,
    seats int  NOT NULL,
    entry_time timestamp  NOT NULL DEFAULT LOCALTIMESTAMP(0),
    CONSTRAINT waitlists_pk PRIMARY KEY (customer_id,restaurant_id)
);

-- foreign keys
-- Reference: Customers_Reviews (table: Reviews)
ALTER TABLE Reviews ADD CONSTRAINT Customers_Reviews
    FOREIGN KEY (posted_by)
    REFERENCES Customers (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

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

-- Reference: Restaurants_Customers (table: Customers)
ALTER TABLE Customers ADD CONSTRAINT Restaurants_Customers
    FOREIGN KEY (recommendations)
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

-- Reference: Reviews_Restaurants (table: Reviews)
ALTER TABLE Reviews ADD CONSTRAINT Reviews_Restaurants
    FOREIGN KEY (posted_to)
    REFERENCES Restaurants (restaurant_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: labels_Restaurants (table: labels)
ALTER TABLE labels ADD CONSTRAINT labels_Restaurants
    FOREIGN KEY (restaurant_id)
    REFERENCES Restaurants (restaurant_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: labels_cuisines (table: labels)
ALTER TABLE labels ADD CONSTRAINT labels_cuisines
    FOREIGN KEY (cuisine_name)
    REFERENCES cuisines (cuisine_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: waitlists_Customers (table: waitlists)
ALTER TABLE waitlists ADD CONSTRAINT waitlists_Customers
    FOREIGN KEY (customer_id)
    REFERENCES Customers (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: waitlists_Restaurants (table: waitlists)
ALTER TABLE waitlists ADD CONSTRAINT waitlists_Restaurants
    FOREIGN KEY (restaurant_id)
    REFERENCES Restaurants (restaurant_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

