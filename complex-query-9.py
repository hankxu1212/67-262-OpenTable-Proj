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

# REQUIRES: filter_type is either "rating" or "cuisine".
# -- IF filter_type = rating, arg1 is the lowerbound for the 
# -- restaurant's average rating, and arg2 is the upperbound
# ----- ENSURES: returns all restaurants with rating arg1 <= r <= arg2
# -- IF filter_type = cuisine, arg1 and arg2 are both cuisine names
# ----- ENSURES: return all restaurants labeled either arg1 OR arg2
def filter_restaurants(filter_type, arg1, arg2) :
    tmpl = ''
    if(filter_type == 'rating') :
        tmpl = '''
            SELECT u.user_id, u.name, avg(r.rating) as avg
              FROM reviews as r
                   JOIN users as u ON r.posted_to = u.user_id
             GROUP BY u.user_id, u.name
            HAVING avg(r.rating) >= %s AND avg(r.rating) <= %s;
        '''
    elif(filter_type == 'cuisine') :
        tmpl = '''
            SELECT u.user_id, u.name
              FROM users as u
                   JOIN labels as l ON u.user_id = l.restaurant_id
             WHERE l.cuisine_name = %s OR l.cuisine_name = %s
        '''
    else :
        raise Exception('Not a Valid filter type. Please enter : rating/cuisine, followed by value')
    cmd = cur.mogrify(tmpl, (arg1, arg2))
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

        filter_restaurants('rating', '4', '10')
        filter_restaurants('rating', '1', '1')
        filter_restaurants('cuisine', 'Japanese', 'Chinese')
        # filter_restaurants('garbage', '??', 'rand(2)')
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))