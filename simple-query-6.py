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

# REQUIRES: void
# ENSURES: a list of cuisines, ordered by the number of reservations corresponding 
# to that cuisine in descending order
def rank_cuisines() :
    tmpl = '''
        SELECT c.cuisine_name, count(r.customer_id)
          FROM cuisines as c
               JOIN labels as l ON l.cuisine_name = c.cuisine_name
               JOIN reservations as r ON r.restaurant_id = l.restaurant_id
         GROUP BY c.cuisine_name
         ORDER BY count(r.customer_id) DESC
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
        print('''User story 10:
                 REQUIRES: void
                 ENSURES: a list of cuisines, ordered by the number of reservations corresponding 
                          to that cuisine in descending order''')
        rank_cuisines()
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))