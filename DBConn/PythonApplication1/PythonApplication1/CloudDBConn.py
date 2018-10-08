import pyodbc
import db_config as cf
import pandas as pd
from IPython.display import display, HTML
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server_name = cf.DATABASE_CONFIG['server_name']
db_name = cf.DATABASE_CONFIG['db_name']
uid = cf.DATABASE_CONFIG['user']
pwd = cf.DATABASE_CONFIG['password']
driver = '{ODBC Driver 13 for SQL Server}'
mailto = cf.MAIL_CONFIG['mail_id']
mailpw = cf.MAIL_CONFIG['mail_pw']

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server_name+';PORT=1433;DATABASE='+db_name+';UID='+uid+';PWD='+ pwd)
'''
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM ExecutiveReport")
row = cursor.fetchone()

while row:
    print ('{:10}'.format(str(row[0])) + '{:>8}'.format(str(row[1])) +  '{:>13}'.format(str(row[2])) +  '{:>14}'.format(str(row[3])) +  '{:>13}'.format(str(row[4])) +  '{:>13}'.format(str(row[5])) + '{:>13}'.format(str(row[6])) )
    row = cursor.fetchone()
'''
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '$ {:,.2f}'.format)
df = pd.read_sql('select * from ExecutiveReport', cnxn)
df.style.set_properties(**{'text-align' :'right'})

display(df)

mailFrom = 'aqsreport@aqs-inc.com'
mailTo1 = 'kenneth.jung@aqs-inc.com'
mailTo2 = 'kenneth.jung@aqs-inc.com,scottk@aqs-inc.com'
#,sungshikkim@aqs-inc.com'

smtp = smtplib.SMTP_SSL('smtp.gmail.com')
#smtp.ehlo()      # say Hello
#smtp.starttls()  # TLS 사용시 필요
smtp.login(mailto, mailpw)
 
msg = MIMEMultipart('alternative')
msg['Subject'] = 'Daily Executive Report'
msg['From'] = mailFrom
msg['To'] = mailTo2

html = df.to_html()
html2 = html.replace('<tr>', '<tr align="right">')
text = "<br>This is an automatically generated email. Thank you."
html3 = html2 + text

part = MIMEText(html3, 'html')

msg.attach(part) 

smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
 
smtp.quit()
print("e-mail send successfully")