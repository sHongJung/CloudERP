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

sql_statement = "DECLARE @sYYear char(4), @sYMonth char(2), @sYDay char(2) " \
                "DECLARE @dDate as smalldatetime, @sDate char(10), @mDate Char(10), @sDateFM char(10), @sDateTO char(10)" \
                "SET @sDateFM = CONVERT(CHAR(10), GETDATE(), 101)" \
                "SET @sDateTO = CONVERT(CHAR(10), GETDATE() + 90, 101)" \
                "SET @dDate = CONVERT(SMALLDATETIME, GETDATE() )" \
                "SET @sYYear = DATEPART(year,@dDate) SET @sYMonth = DATEPART(month,@dDate)" \
                "SET @sYDay = DATEPART(day,@dDate)" \
                "SELECT TOP 32 CONVERT(CHAR(10), CAST(YYYYMMDD AS SMALLDATETIME), 101) AS SBDATE, SHDAILY, SHACCU, BKDAILY, BKACCU, DAYOFWEEK, ISNULL(SHdailyUSNPI, 0) AS SHdailyUSNPI, ISNULL(SHAccuUSNPI, 0) AS SHAccuUSNPI, ISNULL(SHdailyUSEMS, 0) AS SHdailyUSEMS, ISNULL(SHAccuUSEMS, 0) AS SHAccuUSEMS, ISNULL(SHdailyKR, 0) AS SHdailyKR, ISNULL(SHAccuKR, 0) AS SHAccuKR, ISNULL(SHdailyChina, 0) AS SHdailyChina, ISNULL(SHAccuChina, 0) AS SHAccuChina,  ISNULL(SHDailyOther, 0) AS SHDailyOther, ISNULL(SHAccuOther, 0) AS SHAccuOther, ISNULL(SHDailyIntSales, 0) AS SHDailyIntSales, ISNULL(SHAccuIntSales, 0) AS SHAccuIntSales, ISNULL(BKDailyUS, 0) AS BKDailyUS, ISNULL(BKAccuUS, 0) AS BKAccuUS, ISNULL(BKDailyKR, 0) AS BKDailyKR, ISNULL(BKAccuKR, 0) AS BKAccuKR, ISNULL(PASTDUE, 0) AS PASTDUE, ISNULL(NPIPAST,   0) AS NPIPAST, ISNULL(RMAPAST, 0) AS RMAPAST, ISNULL(BOOKWITHIN90, 0)  AS BOOK90, ISNULL(TOTALBOOK, 0) AS TOTALBOOK  FROM  TE6050_HISTORY WHERE  LEFT(YYYYMMDD, 6) =   @sYYear + @sYMonth ORDER  BY SBDATE DESC"

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server_name+';PORT=1433;DATABASE='+db_name+';UID='+uid+';PWD='+ pwd)

pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '$ {:,.2f}'.format)
df = pd.read_sql(sql_statement, cnxn)
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
msg['Subject'] = 'US Daily Shipping/Booking Status'
msg['From'] = mailFrom
msg['To'] = mailTo1

html = df.to_html()
html2 = html.replace('<tr>', '<tr align="right">')
text = "<br>This is an automatically generated email. Thank you."
html3 = html2 + text

part = MIMEText(html3, 'html')

msg.attach(part) 

smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
 
smtp.quit()
print("e-mail send successfully")