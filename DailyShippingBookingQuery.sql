DECLARE @sYYear char(4), @sYMonth char(2), @sYDay char(2)
DECLARE @dDate as smalldatetime, @sDate char(10), @mDate Char(10), @sDateFM char(10), @sDateTO char(10)

SET @sDateFM = CONVERT(CHAR(10), GETDATE(), 101)
SET @sDateTO = CONVERT(CHAR(10), GETDATE() + 90, 101)
SET @dDate = CONVERT(SMALLDATETIME, GETDATE() )

SET @sYYear = DATEPART(year,@dDate)
SET @sYMonth = DATEPART(month,@dDate)
SET @sYDay = DATEPART(day,@dDate)

SELECT  TOP 32 CONVERT(CHAR(10), CAST(YYYYMMDD AS SMALLDATETIME), 101) AS SBDATE, 
                                       SHDAILY, SHACCU, 
                                       BKDAILY, BKACCU, 
                                       DAYOFWEEK, 
                                       ISNULL(SHdailyUSNPI, 0)      AS SHdailyUSNPI,    ISNULL(SHAccuUSNPI, 0)   AS SHAccuUSNPI, 
                                       ISNULL(SHdailyUSEMS, 0)    AS SHdailyUSEMS,   ISNULL(SHAccuUSEMS, 0) AS SHAccuUSEMS, 
                                       ISNULL(SHdailyKR, 0)            AS SHdailyKR,          ISNULL(SHAccuKR, 0)         AS SHAccuKR, 
                                       ISNULL(SHdailyChina, 0)        AS SHdailyChina,      ISNULL(SHAccuChina, 0)     AS SHAccuChina, 
                                       ISNULL(SHDailyOther, 0)        AS SHDailyOther,     ISNULL(SHAccuOther, 0)      AS SHAccuOther, 
                                       ISNULL(SHDailyIntSales, 0)    AS SHDailyIntSales, ISNULL(SHAccuIntSales, 0)  AS SHAccuIntSales, 
                                       ISNULL(BKDailyUS, 0)            AS BKDailyUS,         ISNULL(BKAccuUS, 0)          AS BKAccuUS,
                                       ISNULL(BKDailyKR, 0)            AS BKDailyKR,         ISNULL(BKAccuKR, 0)          AS BKAccuKR,
                                       ISNULL(PASTDUE, 0)            AS PASTDUE,            
                                       ISNULL(NPIPAST,   0)            AS NPIPAST,            
                                       ISNULL(RMAPAST, 0)            AS RMAPAST,            
                                       ISNULL(BOOKWITHIN90, 0)  AS BOOK90,            ISNULL(TOTALBOOK, 0)       AS TOTALBOOK
					   FROM  TE6050_HISTORY
					WHERE  LEFT(YYYYMMDD, 6) =   @sYYear + @sYMonth
					ORDER  BY SBDATE DESC
