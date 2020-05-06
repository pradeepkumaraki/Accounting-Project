#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def show_credits(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Credits WHERE priority=?")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
def credit_transaction(conn, values):
 	conn.execute("INSERT INTO Debits (Name, Amount, Balance, Description, Certified_name,Date,Transact) VALUES ({},{},{},{},{},{},{})".format(values))
 	conn.commit()

def debit_transaction(conn, values):
 	conn.execute("INSERT INTO Debits (Name, Amount, Balance, Description, Certified_name,Date,Transact) VALUES ({},{},{},{},{},{},{})".format(values))
 	conn.commit()


 
def sql_connect():
    database = "/home/aki/accounting_project/sample.db"

    # create a database connection
    conn = create_connection(database)

    conn.execute('''CREATE TABLE IF NOT EXISTS Credits 
            (Name STRING(50) NOT NULL, 
             Amount DECIMAL NOT NULL,
             Balance DECIMAL NOT NULL,
            Description STRING(50) NOT NULL,
            Certified_name STRING(50) NOT NULL,
            Date DATETIME NOT NULL, 
            Transact INTEGER PRIMARY KEY NOT NULL)''')


    conn.execute('''CREATE TABLE IF NOT EXISTS Debits 
            (Name STRING(50) NOT NULL,
             Amount DECIMAL NOT NULL, 
            Description STRING(50) NOT NULL,
            Certified_name STRING(50) NOT NULL,
            Date DATETIME NOT NULL,
            Credit_Transact INTEGER 	 NOT NULL, 
            Debit_Transact INTEGER PRIMARY KEY NOT NULL,
            FOREIGN KEY (Credit_Transact) REFERENCES Credits (Transact) 
  ON UPDATE CASCADE
  ON DELETE CASCADE)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS logs 
            (Name STRING(50) NOT NULL,
             Amount DECIMAL NOT NULL, 
            Description STRING(50) NOT NULL,
            Certified_name STRING(50) NOT NULL,
            Date DATETIME NOT NULL, 
            Transact INTEGER  NOT NULL,
            Action STRING(50) NOT NULL)''')

    return conn