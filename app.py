import time

import redis
import mysql.connector
from flask import Flask

import os

# Set environment variables 
# REDIS
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
# MYSQL
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']

app = Flask(__name__)
cache = redis.Redis(host=REDIS_HOST, port=6379, password=REDIS_PASSWORD)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    message = 'Hello Keepcoding! I have been seen {} times.\n'.format(count)
    #with open("log.txt","a+") as fo:
    #    fo.write(message)
    
    return message

@app.route('/insert')
def insert_hits():
    #Obtaining clicks number
    count = get_hit_count()
    # Open database connection
    db = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database='TESTDB')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Inserting click numbers in DB
    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO counter(hits) VALUES ('%d' )" % (count)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        return "Insertion OK"
    except:
        # Rollback in case there is any error
        db.rollback()
        return "Oh oh, we have a problem with the insertion"

    # disconnect from server
    db.close()

@app.route('/read')
def read_hits():
    # Open database connection
    db = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database='TESTDB')

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM counter"
    try:
    # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            n_hits = row[0]
            # Now print fetched result
            message_number_hits = 'Hello all! I have been seen {} times.\n'.format(n_hits)
    except:
        message_number_hits = 'Error: unable to fetch data'

    # disconnect from server
    db.close()
    return message_number_hits

@app.route('/create_db')
def create_db():
    # Open database connection
    db = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS TESTDB")
        db.close()
        return "BD creada OK"
    except mysql.connector.Error as err:
        db.close()
        return("Failed creating database: {}".format(err))
        exit(1)


@app.route('/create_table')
def create_table():
    # Open database connection
    db = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database='TESTDB')

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS counter ( hits INT)")
        db.close()
        return "COUNTER creada OK"
    except mysql.connector.Error as err:
        db.close()
        return("Failed creating table: {}".format(err))
        exit(1)

@app.route('/health/live')
def health_live():
    return "Ok"

@app.route('/health/ready')
def health_ready():
    return "Ok"

