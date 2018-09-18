import pyodbc
import db_config as cf
import pandas as pd


server_name = cf.DATABASE_CONFIG['server_name']
db_name = cf.DATABASE_CONFIG['db_name']
uid = cf.DATABASE_CONFIG['user']
pwd = cf.DATABASE_CONFIG['password']
driver = '{ODBC Driver 13 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server_name+';PORT=1433;DATABASE='+db_name+';UID='+uid+';PWD='+ pwd)

cursor = cnxn.cursor()
cursor.execute("SELECT * FROM ExecutiveReport")
row = cursor.fetchone()
while row:
    print (str(row[0]) + "  " + str(row[1])+ "  " +  str(row[2]) + "  "+  str(row[3]) + "  "+  str(row[4]) )
    row = cursor.fetchone()

'''
df = pd.read_sql_query('select * from ExecutiveReport', cnxn)
df.head()
'''