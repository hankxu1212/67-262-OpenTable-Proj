import psycopg2
import sys
import customer_functions as cf
import restaurant_functions as rf
import other_functions as of
import admin_functions as af

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

'''
--------------------------------------------------
--- customer functions
1. make reservation
2. cancel reservation
3. check available hours
4. filter restaurants by cuisines or reviews

--- restaurant functions
5. notify customers for waitlist
6. check when available for next duration
7. seasonal recommendations

--- other user functions
8. change basic info

--- admin functions
9. recommend loyal customers
10. find restaurants with highest 1 star percentage reviews
11. what cuisine gets most reservations

Choose (1-11, 0 to quit): '''

def show_menu():
    of.show_menu()
    
def make_reservation(p_customer_id, p_restaurant_id, p_date, p_time, p_seats, p_info) :
    cf.make_reservation(p_customer_id, p_restaurant_id, p_date, p_time, p_seats, p_info)

def cancel_reservation(p_customer_id, p_restaurant_id) :
    cf.cancel_reservation(p_customer_id, p_restaurant_id)

def check_available_hours() :
    pass

def filter_restaurants() :
    pass

def add_to_waitlist() :
    pass

def check_special_occasion() :
    pass

def recommend_seasonals() :
    pass

def update_user_info() :
    pass

def recommend_loyal_customers() :
    pass

def rank_restaurants() :
    pass

def rank_cuisines() :
    pass

actions = {
1: show_menu,
2: make_reservation,
3: cancel_reservation,
4: check_available_hours,
5: filter_restaurants,
6: add_to_waitlist,
7: check_special_occasion,
8: recommend_seasonals,
9: update_user_info,
10:recommend_loyal_customers,
11: rank_restaurants,
12: rank_cuisines}


if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'opentable', 'isdb'
        # you may have to adjust the user 
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
        show_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))
