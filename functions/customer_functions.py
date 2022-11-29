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

def new_reservation():
    heading("new_reservation")
    date = input('Date: ')
    time = input('Time: ')
    seats = input('Seats: ')
    cust_id = input('Customer_Id (1-10): ')
    rest_id = input('Restaurant_id (11-20): ')
    make_reservation(date=date, time=time, seats=seats, cust_id=cust_id, rest_id=rest_id)

def make_reservation(date, time, seats, info, cust_id, rest_id) :
    tmpl = '''
        INSERT INTO Reservations(date, time, seats, additional_requests, customer_id, restaurant_id)
            VALUES(%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (date, time, seats, info, cust_id, rest_id))
    print_cmd(cmd)
    cur.execute(cmd)

def cancel_reservation(p_customer_id, p_restaurant_id):
    pass

def check_available_hours(p_restaurant_id) :
    pass

def filter_restaurants(filter_type, filter_value, order, limit) :
    pass

def join_waitlist(p_customer_id, p_restaurant_id, p_date, p_time, p_seats) :
    pass

if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'opentable', 'isdb'
        # you may have to adjust the user 
        # python a4-socnet-sraja.py a4_socnet postgres
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        # by assigning to conn and cur here they become
        # global variables.  Hence they are not passed
        # into the various SQL interface functions
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        new_reservation()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))