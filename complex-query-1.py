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

def check_available_reservations(rest_id, date, time) :
    tmpl = '''
    SELECT check_reservations(%s, %s, %s);
    SELECT time
      FROM Available_Times
     ORDER BY time ASC;
    '''
    cmd = cur.mogrify(tmpl, (rest_id, date, time))
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
        print('User Story #3')
        print('''This user story finds the available reservations within two 
                 hours of the specified time at the specified restaurant on the
                 specified date, assuming that a restaurant can only have two
                 reservations every half an hour.''')
        print('Showing Available Reservations within 2 hours of 18:00:')
        print('Note: Since 17:30 is booked, it is not in the list.')
        check_available_reservations(18, '2023-1-1', '18:00')

    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))