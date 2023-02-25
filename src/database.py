# 2023 Copyright Ash Amin
# Functions are from and modified from the guide here:
# https://www.postgresqltutorial.com/postgresql-python/connect/
# Big thank you for the clear and coherent tutorial.

import psycopg2
from configparser import ConfigParser
import bcrypt

from shoprToken import tokenNew, tokenDecrypt

# Function is from: https://www.postgresqltutorial.com/postgresql-python/connect/
def databaseConfig(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


# Initialise Database.
def databaseInit():
    """ create tables in the PostgreSQL database"""
    commands = [
        ("""
        CREATE TABLE users (
            userID SERIAL PRIMARY KEY,
            userName VARCHAR(255) NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            password VARCHAR NOT NULL
        )
        """),]
    conn = None
    try:
        # read the connection parameters
        params = databaseConfig()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # Store bank balance.
        cur.execute("""INSERT INTO bank (balance) VALUES(%s)""", ("0",))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()