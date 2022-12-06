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
# ENSURES: a list of months ordered by the number of reservations made in that month in descending order
def rank_months() :
    tmpl = '''
        SELECT EXTRACT(MONTH FROM date) AS month, COUNT(customer_id) AS TotalCount
          FROM reservations
         GROUP BY EXTRACT(MONTH FROM date)
         ORDER BY TotalCount DESC
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

        rank_months()
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))