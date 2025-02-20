import oracledb
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config.config import load_config
from src.repos.GetStatePointId import getStatePointId

#read config.json
database_config = load_config()


#this function takes input as start time, endtime and statename and returns IntraDayAHead forecast demand by quering from FORECAST_REVISION_STORE table 
def getForecastRevision(fromDate, toDate, stateName, revisonNo='R0A'):
    pointId = getStatePointId(stateName) #get state point ID
    if pointId is None: 
        return []
    try:
        with oracledb.connect(database_config["DATABASE_URL"]) as connection: #connect to database 
            with connection.cursor() as cursor:
                sql = "select FORECASTED_DEMAND_VALUE, TIME_STAMP from FORECAST_REVISION_STORE where ENTITY_TAG = '{0}' and TIME_STAMP between to_timestamp('{1}', 'YYYY-MM-DD HH24:MI:SS.FF3')  and  to_timestamp('{2}', 'YYYY-MM-DD HH24:MI:SS.FF3')  and  REVISION_NO = '{3}' ORDER BY TIME_STAMP ASC".format(pointId, fromDate, toDate, revisonNo)
                #print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [list(i) for i in rows] #return data as list 

    except Exception as E:
        print("error", E)

       
#getForecastRevision('2024-09-10 00:00:00.000', '2024-09-12 00:00:00.000', "GOA", 'R0A')