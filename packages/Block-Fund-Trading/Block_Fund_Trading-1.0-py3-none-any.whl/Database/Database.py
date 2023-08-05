import pymysql
import os
import pandas as pd
from pandas.io import sql







class Database:
         


    def __init__(self):
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'Eaststreet1'
        self.port = '3306'
        self.database = 'Block_Traders'

    def MySQl_connection(host, username, password, port, database):

        conn = pymysql.connect( host= host, user= username, passwd= password, db= database )

        return conn



    def df_to_sql(self, dataframe, conn, tablename):
        dataframe.to_sql( name = tablename, con = conn, if_exists = 'replace', index = False)
                
        


    
    @staticmethod
    def write(data):
        '''    
        Save order
        data = orderid,symbol,amount,price,side,quantity,profit
        Create a database connection
        '''
        cur = conn.cursor()
        cur.execute('''INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
    
    @staticmethod
    def read(orderid):
        '''
        Query order info by id
        :param orderid: the buy/sell order id
        :return:
        '''
        cur = conn.cursor()
        cur.execute('SELECT * FROM orders WHERE orderid = ?', (orderid,))
        return cur.fetchone()

    def close_MySQL_conn(conn):
        conn.close()


