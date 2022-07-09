'''importing database in order for our interactive app to run'''
import database

DISPLAY_MESSAGE = """\nWelcome to the SQLITE CRUD App !
1] Add user data
2] Add child data
3] Delete user data
4] Update user data
5] View all user data
6] Exit

Selection: """


def add_user_data():
    '''Takes input details from user and sends them to database'''
    user = {
        'first_name': input("enter first name: "),
        'last_name': input("enter last name: "),
        'country': input("enter country name: ")
        }
    
    database.user_add_to_table(user)


def view_parents_data(all_user=False):
    '''Fetch and thus show parents data from database'''
    if all_user:
        all_data = database.get_all_user_data()
        for element in all_data:
            
            print(element)
    else:
        parent_data = database.get_current_parents_data()
        # print(parent_data)
        print("Parents id's with names")
        print('------------------------')

        for _id, f_n, l_n,c in parent_data:
            print(f"id: {_id} Name: {f_n} {l_n} Country: {c}")

        print('\n')


def add_child_data():
    '''helps add child data in interactive mode'''
    database.child_add_to_table(
        input("enter child's name: "),
        input("enter parent id: "))


def delete_data():
    '''helps delete parents data in interactive mode'''
    database.delete_user_data(int(input("enter id: ")))


def update_user_data():
    '''helps update parents data in interactive mode'''
    col_name = input("Please enter the column name: ").lower()
    new_value = input("Enter the value: ")
    id_val = input(
        "Please enter the parent id to which you would like to change the value: ")
    database.update_table(col_name, new_value, id_val)  ## Implement Validation logic if necessary


# the following operator: walrus operator , was introduced in python 3.8
# and works in later versions
while(user_input := input(DISPLAY_MESSAGE)) != '6':
    if user_input == '1':
        add_user_data()
    elif user_input == '2':
        view_parents_data()
        add_child_data()
    elif user_input == '3':

        view_parents_data()
        delete_data()

    elif user_input == '4':
        view_parents_data()
        update_user_data()
    elif user_input == '5':
        view_parents_data(True)
