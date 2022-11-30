import psycopg2
import sys
import functions.customer_functions as cf
import functions.restaurant_functions as rf
import functions.other_functions as of
import functions.admin_functions as af

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
5. join waitlists

--- restaurant functions
6. seasonal recommendations

--- other user functions
7. change basic info

--- admin functions
8. recommend loyal customers
9. find restaurants with highest 1 star percentage reviews
10. what cuisine gets most reservations

Choose (1-11, 0 to quit): '''

def show_menu():
    of.show_menu()
    
def make_reservation(p_customer_id, p_restaurant_id, p_date, p_time, p_seats, p_info) :
    cf.make_reservation(p_customer_id, p_restaurant_id, p_date, p_time, p_seats, p_info)

def cancel_reservation(p_customer_id, p_restaurant_id) :
    cf.cancel_reservation(p_customer_id, p_restaurant_id)

def check_available_hours(p_restaurant_id, p_date, p_time) :
    cf.check_available_hours(p_restaurant_id, p_date, p_time)

def filter_restaurants(filter_type, filter_value, order, limit) :
    cf.filter_restaurants(filter_type, filter_value, order, limit)

def join_waitlist(p_customer_id, p_restaurant_id, p_date, p_time, p_seats) :
    cf.join_waitlist(p_customer_id, p_restaurant_id, p_date, p_time, p_seats)

def rank_seasons(p_restaurant_id) :
    rf.rank_seasons(p_restaurant_id)

def update_user_info(user_id, edits) :
    of.update_user_info(user_id, edits)

def recommend_customers(user_id) :
    af.recommend_customers(user_id)

def rank_restaurants() :
    af.rank_restaurants()

def rank_cuisines() :
    af.rank_cuisines()

actions = {
1: show_menu,
2: make_reservation,
3: cancel_reservation,
4: check_available_hours,
5: filter_restaurants,
6: join_waitlist,
7: rank_seasons,
8: update_user_info,
9: recommend_customers,
10: rank_restaurants,
11: rank_cuisines}


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
