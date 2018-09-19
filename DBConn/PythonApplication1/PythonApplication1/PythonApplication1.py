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
   print ('{:10}'.format(str(row[0])) + '{:>8}'.format(str(row[1])) +  '{:>13}'.format(str(row[2])) +  '{:>14}'.format(str(row[3])) +  '{:>13}'.format(str(row[4])) +  '{:>13}'.format(str(row[5])) + '{:>13}'.format(str(row[6])) )
   row = cursor.fetchone()



'''     
df = pd.read_sql_table('select * from ExecutiveReport', cnxn)
df.head()
'''