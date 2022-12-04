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

def recommend_customers(cust_id) :
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

        print('Showing table: Reservations ----------------- Before: ---------------------------')
        recommend_customers(1)
        print('Showing table: Reservations ----------------- After: ----------------------------')
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))