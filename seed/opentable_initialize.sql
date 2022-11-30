\c postgres
DROP DATABASE IF EXISTS opentable;

CREATE database opentable;
\c opentable

\i opentable_create.SQL

\copy Users(user_id, name, email, phone) FROM csv/users.csv csv header;

\copy Customers(customer_id, loyalty_pts) FROM csv/customers.csv csv header;

\copy Restaurants(restaurant_id, location, menu, hours) FROM csv/restaurants.csv csv header;
