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

def rank_restaurants() :
    tmpl = '''
        CREATE VIEW one_star AS
            SELECT posted_to, count(review_id) as cnt
              FROM reviews
             WHERE rating = 1
             GROUP BY posted_to;

        CREATE VIEW total_reviews AS 
            SELECT posted_to, count(review_id) as cnt
              FROM reviews
             GROUP BY posted_to;

        SELECT u.user_id, u.name, 1.0*o.cnt/t.cnt AS percentage
          FROM one_star as o
               JOIN total_reviews as t ON o.posted_to = t.posted_to
               JOIN users as u ON u.user_id = t.posted_to
         ORDER BY percentage DESC
         LIMIT 10;
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

        rank_restaurants()
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))