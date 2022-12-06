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

# REQUIRES: valid inputs with correct types
# ENSURES: updated restaurant table with the new information
def update_info(rest_id, p_location, p_menu, p_open_hour, p_close_hour) :
    tmpl = '''
        UPDATE restaurants
           SET location = %s,
               menu = %s,
               open_hour = %s,
               close_hour = %s
         WHERE restaurant_id = %s;
    '''
    cmd = cur.mogrify(tmpl, (p_location, p_menu, p_open_hour, p_close_hour, rest_id))
    print_cmd(cmd)
    cur.execute(cmd)

def show() :
    tmpl = '''
        SELECT *
          FROM restaurants
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

        print('Showing table: Restaurants ----------------- Before: ---------------------------')
        show()
        print('''User story 7
                 REQUIRES: valid inputs with correct types
                 ENSURES: updated restaurant table with the new information''')
        update_info(13, 'Pacific', 'Gross', '12:00', '13:00')
        print('Showing table: Restaurants ----------------- After: ----------------------------')
        show()
        
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))