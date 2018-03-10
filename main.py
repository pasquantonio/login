"""
A login system built with python3 and sqlite3

Joe Pasquantonio
"""
import sqlite3
import bcrypt
import os.path
from datetime import datetime
from argparse import ArgumentParser
from getpass import getpass


DATABASE = 'test.db'


def connect_db():
    """Connect to database"""
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv


def init_db(filename):
    """
    Initalize the database.

    Read schema from specified file and create database
    """
    db = connect_db()
    with open(filename, mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Database initialized.')


def add_user():
    """
    Adds a new user to the database
    ensure username does not already exist

    store username in lowercase
    """
    username, password = get_credentials()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    db = connect_db()
    cursor = db.execute('select username from users where username = (?)',
                        (username,))
    if cursor.fetchone():
        print('That user name already exists.')
        return
    dt = datetime.now()
    db.execute('insert into users'
               '(username, password, created) values (?, ?, ?)',
               [username, password, dt])
    db.commit()
    print('User successfully created')


def fetch_all_users():
    """Return list of users in database"""
    db = connect_db()
    cursor = db.execute('select id, username, created from users order by id')
    users = cursor.fetchall()
    return users


def display_users():
    """Fetch all usernames in database and display in terminal"""
    users = fetch_all_users()
    print('\nUSERS')
    print('-'*35)
    for user in users:
        print(format_user(user))
        print('-'*35)
    print('END\n')


def format_user(user):
    """Return formatted string of user data"""
    return 'ID: {}\nUsername: {}\nCreated: {}'.format(user[0],
                                                      user[1],
                                                      user[2])


def check_credentials(u, p):
    """Check password entered against database hash"""
    db = connect_db()
    try:
        cursor = \
            db.execute(
                'select username, password from users where username = (?)',
                (u,)
            )
        user = cursor.fetchone()
        if bcrypt.checkpw(p, user[1]):
            return True
        return False
    except Exception as e:
        print('Incorrect credentials or user does not exist')
        return


def login():
    """Return boolean if credentials are correct or not"""
    username, password = get_credentials()
    return check_credentials(username, password)


def get_credentials():
    """
    Prompt user for username and password

    return: username as string
    return: password as 'bytes' object
    """
    username = input('Username: ')
    username = username.lower()
    password = str.encode(getpass('Password: '))
    return username, password


if __name__ == "__main__":
    parser = ArgumentParser(description='Terminal Login System')
    parser.add_argument('--init',
                        help='initialize the database',
                        action='store_true')
    parser.add_argument('--create',
                        help='create a new user',
                        action='store_true')
    parser.add_argument('--users',
                        help='display all usernames',
                        action='store_true')
    args = parser.parse_args()

    if args.init:
        if os.path.isfile(DATABASE):
            print('A database already exists!')
        else:
            init_db('schema.sql')

    if args.create:
        add_user()

    if args.users:
        display_users()

    if login():
        print('Sucessfully Logged in.')
    else:
        print('Incorrect credentials, try again.')
