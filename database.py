#!/usr/bin/env python3

import mysql.connector
from config_db import ConfigDb

class Database:
    """
    Handle mySQL database connections.
    Requires a ConfigDB instance.
    """

    def __init__(self, config):

        self._connection = mysql.connector.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            database=config.database)
        
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

def main():

    try:
        c = ConfigDb('config_db.ini')

        with Database(c) as db:
            prices = db.query('select symbol, contract, expires from prices where symbol in (%s, %s)', ('HEN', 'HIS',))
            for (symbol, contract, price) in prices:
                print('{}|{} = {}'.format(symbol, contract, price))

    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
    
