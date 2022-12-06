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
    CREATE or REPLACE function check_reservations (p_rest_id integer, p_date date, p_time time)
    RETURNS void
    language plpgsql as
    $$
    DECLARE check_time time = p_time - interval '2 hours';
    DECLARE end_time time = check_time + interval '4.5 hours';
    BEGIN

    DROP Table IF EXISTS Available_Times;
    DROP Table IF EXISTS Unavailable_Times;

    CREATE Table Available_Times AS
        (SELECT time
           FROM Reservations
          WHERE restaurant_id = p_rest_id AND date = p_date
          GROUP BY time, date
         HAVING count(customer_id) < 2);

    CREATE Table Unavailable_Times AS
        (SELECT time
           FROM Reservations
          WHERE restaurant_id = p_rest_id AND date = p_date
          GROUP BY time, date
         HAVING count(customer_id) >= 2);

    LOOP 
    EXIT WHEN check_time = end_time;
        IF check_time NOT IN (SELECT time
                                From Available_Times) AND
           check_time NOT IN (SELECT time
                                FROM Unavailable_Times)
            THEN INSERT INTO Available_Times(time)
                    VALUES(check_time);
        END IF;
        check_time = check_time + interval '.5 hours';
    END LOOP;
    END;
    $$;
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
        print('Showing Available Reservations within 2 hours')
        check_available_reservations(18, '2023-1-1', '18:00')


    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))