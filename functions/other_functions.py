def show_menu():
    menu = '''
--------------------------------------------------
--- customer functions
1. make reservation
2. cancel reservation
3. check available hours
4. filter restaurants by cuisines or reviews

--- restaurant functions
5. notify customers for waitlist
6. check when available for next duration
7. seasonal recommendations

--- other user functions
8. change basic info

--- admin functions
9. recommend loyal customers
10. find restaurants with highest 1 star percentage reviews
11. what cuisine gets most reservations

Choose (1-11, 0 to quit): '''

    try:
        choice = int(input( menu ))
    except ValueError:
        print("\n\n* Invalid choice. Choose again.")
        show_menu()
    else:
        if choice == 0:
            print('Done.')
            cur.close()
            conn.close()
        elif choice in range(1,1+7):
            print()
            actions[choice]()
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close()

def update_user_info(user_id, edits) :
    pass