'''importing standard library sqlite3'''
import sqlite3


CREATE_PARENT_TABLE = """CREATE TABLE IF NOT EXISTS p_table (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    country TEXT


);"""

CREATE_CHILD_TABLE = """CREATE TABLE IF NOT EXISTS c_table (
    child_name TEXT PRIMARY KEY,
    parent_id INTEGER,
    FOREIGN KEY(parent_id) REFERENCES p_table(id)


);"""

INSERT_PARENTS_INFO = """INSERT INTO p_table (first_name, last_name, country)
VALUES (?,?,?);"""
INSERT_CHILD_INFO = "INSERT INTO c_table (child_name, parent_id) VALUES (?,?);"
SHOW_EXISTING_PARENTS = "SELECT id,first_name,last_name,country FROM p_table;"
SHOW_USER_DETAILS = """SELECT * FROM p_table
LEFT JOIN c_table
ON p_table.id = c_table.parent_id;"""
SHOW_EXISTING_IDS = "SELECT id FROM p_table;"
DELETE_PARENTS_DATA = "DELETE FROM p_table where id = ?;"
DELETE_CHILD_DATA = "DELETE FROM c_table where parent_id = ?;"


connection = sqlite3.connect("data.db")
with connection:
    connection.execute(CREATE_PARENT_TABLE)
    connection.execute(CREATE_CHILD_TABLE)


def query_builder(column_name, new_val):
    '''this method takes two arguments and build a query suitable for update_table method'''
    if column_name in [
        'first_name',
        'last_name',
        'country']:
        query_built = f"UPDATE p_table SET {column_name} = '{new_val}' WHERE id = ?;"
    return query_built


def update_table(column_name, new_val, parent_id):
    '''this method is used for updating data as per column
    name provided user delivered new value and parent id'''
    parent_id_list = get_current_parents_data(True)
    query = query_builder(column_name, new_val)

    # The below part looks for an integer value and if it sees that the User
    # passed a column name like Human or Place name and a value that contains only integer
    # it do not permit value change
    # It also checks if the user provided a valid parents id

    try:
        int(new_val)
    except ValueError:
        if int(parent_id) in parent_id_list:
            with connection:
                connection.execute(query, (parent_id,))
            return True 
    return False


def user_add_to_table(user):
    '''this method adds parent user to table'''
    with connection:
        connection.execute(
            INSERT_PARENTS_INFO,
            (user['first_name'],
             user['last_name'],
             user['country']))


def get_current_parents_data(_id=False):
    '''this method is responsible for returning datas from database'''
    with connection:
        cursor = connection.cursor()

        if _id:
            cursor.execute(SHOW_EXISTING_IDS)
            result = [elem[0] for elem in cursor.fetchall()]
        else:
            cursor.execute(SHOW_EXISTING_PARENTS)
            result = cursor.fetchall()

    return result


def prepare_data(fetched_data):
    '''data manipulation for get_all_user_data() method  '''
    data = fetched_data
    # print(fetched_data)
    ready_data = []
    for index in data:
        data_man = ''
        for component in index[:5]:   # Please print fetched_data to understand the motive
            data_man = data_man + ' ' + str(component)
        ready_data.append(data_man)
    return ready_data


def child_add_to_table(child_name, corresponding_parent_id):
    '''Adds child information to child table'''
    with connection:
        connection.execute(
            INSERT_CHILD_INFO,
            (child_name,
             corresponding_parent_id))


def delete_user_data(_id):
    '''Deletes parent user along with child as per provided parentID '''
    if _id in get_current_parents_data(True):

        with connection:
            connection.execute(DELETE_CHILD_DATA, (_id,))
            connection.execute(DELETE_PARENTS_DATA, (_id,))
        return True

    return False


def get_all_user_data():
    '''gets data and manipulates them to show to the user'''
    with connection:
        cursor = connection.cursor()
        cursor.execute(SHOW_USER_DETAILS)
    return prepare_data(cursor.fetchall())
