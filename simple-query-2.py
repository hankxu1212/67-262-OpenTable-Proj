import psycopg2
import sys

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

def cancel_reservation(cust_id, rest_id, date) :
    tmpl = '''
    DELETE FROM Reservations
           WHERE customer_id = %s AND restaurant_id = %s AND date = %s
    '''
    cmd = cur.mogrify(tmpl, (cust_id, rest_id, date))
    print_cmd(cmd)
    cur.execute(cmd)

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
        cust_id = 9
        rest_id = 19
        date = '2023-1-12'
        make_reservation('2023-1-12', '18:00', 2, "Birthday", cust_id, rest_id)
        print('Showing table: Reservations ----------------- Before: ---------------------------')
        show_all_reservations()
        print("Canceling Sam's reservation at Primanti Bros on 2023-1-12")
        cancel_reservation(cust_id, rest_id, date)
        print('Showing table: Reservations ----------------- After: ----------------------------')
        show_all_reservations()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))