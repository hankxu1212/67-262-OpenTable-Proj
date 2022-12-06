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
    heading("New_Reservation")
    date = input('Date (e.g. 2023-02-12): ')
    time = input('Time (e.g. 14:00): ')
    seats = input('Seats (e.g. 3): ')
    info = input('Additional Information: (e.g. Anniversary)')
    cust_id = input('Customer_Id (e.g. 4): ')
    rest_id = input('Restaurant_id (e.g. 12): ')
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
        print('Showing table: Reservations ----------------- Before: ---------------------------')
        show_all_reservations()
        print('Inserting a reservation for Jill at Red Robin')
        make_reservation('2023-1-1', '14:00', 3, "Anniversary", 4, 13)
        print('Showing table: Reservations ----------------- After: ----------------------------')
        show_all_reservations()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))