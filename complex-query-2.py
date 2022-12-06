import psycopg2
import sys

def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')    

SHOW_CMD = True

def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

def show_all_reservations() :
    tmpl = '''
        SELECT c.name, t.name, r.date, r.time, r.seats, r.additional_requests
          FROM Users as c 
               JOIN Reservations as r ON c.user_id = r.customer_id
               JOIN Users as t ON r.restaurant_id = t.user_id
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

def cancel_reservation(cust_id, rest_id, date) :
    tmpl = '''
    DELETE FROM Reservations
           WHERE customer_id = %s AND restaurant_id = %s AND date = %s
    '''
    cmd = cur.mogrify(tmpl, (cust_id, rest_id, date))
    print_cmd(cmd)
    cur.execute(cmd)

def remove_from_waitlist() :
    tmpl = '''
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
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)

def show_waitlist() :
    tmpl = '''
    SELECT * 
      FROM Waitlists
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()


if __name__ == '__main__':
    try:
        db, user = 'opentable', 'isdb'
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        print('User Story #4')
        print('''This user story automatically implements a reservation from the
                 waitlist when a relevant cancellation has occurred.''')
        remove_from_waitlist()
        print('Showing table: Waitlists ----------------- Before: ---------------------------')
        show_waitlist()
        print('Showing table: Reservations ----------------- Before: ---------------------------')
        show_all_reservations()
        print("Canceling Fred's reservation at Red Lobster on 2023-1-5")
        cancel_reservation(6, 15, '2023-1-5')
        print("Adding Sam's reservation from the waitlist")
        print('Showing table: Waitlists ----------------- After: ---------------------------')
        show_waitlist()
        print('Showing table: Reservations ----------------- After: ---------------------------')
        show_all_reservations()
 
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))