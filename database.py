import sqlite3
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    print('Good')
    try:
        conn = sqlite3.connect(db_file)
        print('Good')
    except Error as e:
        print(e)
 
    return conn