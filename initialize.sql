\c postgres
DROP DATABASE IF EXISTS opentable;

CREATE database opentable;
\c opentable

\i create.SQL

\copy Users(user_id, name, email, phone) FROM csv/users.csv csv header;

\copy Customers(customer_id, loyalty_pts) FROM csv/customers.csv csv header;

\copy Restaurants(restaurant_id, location, menu, open_hour, close_hour) FROM csv/restaurants.csv csv header;

\copy Cuisines(cuisine_name) FROM csv/cuisines.csv csv header;

\copy Reservations(date, time, seats, additional_requests, customer_id, restaurant_id) FROM csv/reservations.csv csv header;

\copy Reviews(review_id, comment, rating, posted_by, posted_to) FROM csv/reviews.csv csv header;

\copy Labels(restaurant_id, cuisine_name) FROM csv/labels.csv csv header;

\copy Waitlists(customer_id, restaurant_id, date, time, seats, entry_time) FROM csv/waitlists.csv csv header;