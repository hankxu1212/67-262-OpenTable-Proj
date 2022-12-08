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

\copy Waitlists(customer_id, restaurant_id, date, time, seats, entry_time, add_requests) FROM csv/waitlists.csv csv header;

CREATE OR REPLACE FUNCTION fn_remove_from_waitlist()
    RETURNS trigger
    LANGUAGE plpgsql AS
    $$
    DECLARE waitlist_cust integer;
    DECLARE num_seats integer;
    DECLARE add_info text;
    BEGIN
    waitlist_cust = (SELECT customer_id
                       FROM Waitlists
                      WHERE restaurant_id = old.restaurant_id AND
                            date = old.date AND 
                            time = old.time
                      ORDER BY entry_time ASC
                      LIMIT 1);
    IF waitlist_cust IS NOT NULL
        THEN num_seats = (SELECT seats
                            FROM Waitlists
                           WHERE restaurant_id = old.restaurant_id AND
                                 date = old.date AND 
                                 customer_id = waitlist_cust);
             add_info = (SELECT add_requests
                           FROM Waitlists
                          WHERE restaurant_id = old.restaurant_id AND
                                date = old.date AND 
                                customer_id = waitlist_cust);
             INSERT INTO Reservations(date, time, seats, customer_id, restaurant_id)
                         VALUES(old.date, old.time, num_seats, waitlist_cust, old.restaurant_id);
             DELETE FROM Waitlists
                    WHERE customer_id = waitlist_cust AND 
                          date = old.date AND
                          restaurant_id = old.restaurant_id;
    END IF;
    RETURN null;
    END;
    $$;

    CREATE OR REPLACE TRIGGER tr_remove_from_waitlist
    AFTER DELETE OR UPDATE ON Reservations
    FOR EACH ROW
    EXECUTE FUNCTION fn_remove_from_waitlist();