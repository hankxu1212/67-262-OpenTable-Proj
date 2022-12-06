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

# REQUIRES: a valid customer_id
# ENSURES: UPDATES customer.recommendations -> the highest rated restaurant with customer's favorate cuisine
def recommend_customers(cust_id) :
    tmpl = '''
    CREATE VIEW tmp_reservations AS
        SELECT restaurant_id
          FROM reservations
         WHERE customer_id = %s;

    CREATE VIEW cuisines_rank AS
        SELECT c.cuisine_name, count(r.restaurant_id) as cnt
          FROM cuisines AS c
               JOIN labels AS l ON l.cuisine_name = c.cuisine_name
               JOIN tmp_reservations as r ON l.restaurant_id = r.restaurant_id
      GROUP BY c.cuisine_name
      ORDER BY cnt DESC;
    
    CREATE VIEW ratings AS
        SELECT l.restaurant_id, avg(r.rating) as avg
          FROM reviews AS r
               JOIN labels AS l ON r.posted_to = l.restaurant_id
               JOIN cuisines_rank as c ON l.cuisine_name = (SELECT c2.cuisine_name 
                                                              FROM cuisines_rank as c2
                                                             LIMIT 1)
      GROUP BY l.restaurant_id
      ORDER BY avg DESC;

    UPDATE customers
       SET recommendations = (SELECT r.restaurant_id
                                FROM ratings as r
                               LIMIT 1)
     WHERE customer_id = %s;
    '''
    cmd = cur.mogrify(tmpl, (cust_id, cust_id))
    print_cmd(cmd)
    cur.execute(cmd)

def show() :
    tmpl = '''
        SELECT *
          FROM customers
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

        print('Showing table: Customers ----------------- Before: ---------------------------')
        show()
        recommend_customers(5)
        print('Showing table: Customers ----------------- After: ----------------------------')
        show()
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))