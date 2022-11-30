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

def new_reservation_menu():
    heading("new_reservation")
    date = input('Date: ')
    time = input('Time: ')
    seats = input('Seats: ')
    info = input('Additional Information: ')
    cust_id = input('Customer_Id (1-10): ')
    rest_id = input('Restaurant_id (11-20): ')
    make_reservation(date=date, time=time, seats=seats, info=info, cust_id=cust_id, rest_id=rest_id)
    show_all_reservations()

def make_reservation(date, time, seats, info, cust_id, rest_id) :
    tmpl = '''
        INSERT INTO Reservations(date, time, seats, additional_requests, customer_id, restaurant_id)
            VALUES(%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (date, time, seats, info, cust_id, rest_id))
    print_cmd(cmd)
    cur.execute(cmd)

def show_all_reservations() :
    tmpl = '''
        SELECT c.name, t.name, r.date, r.time
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
        new_reservation_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))