from src.repos.GetStatePointId import getStatePointId
from src.config.config import load_config
import oracledb
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# load the config.json
database_config = load_config()


#this function takes input as start time, end time, state name and returns DayAHead forecast demand
def getDayAHeadData(fromDate, toDate, stateName):
    pointId = getStatePointId(stateName)  # get point ID
    if pointId is None:
        return {}
    try:
        # connect to database
        with oracledb.connect(database_config["DATABASE_URL"]) as connection: #database connection
            with connection.cursor() as cursor:
                sql = "select FORECASTED_DEMAND_VALUE, TIME_STAMP from DAYAHEAD_DEMAND_FORECAST where ENTITY_TAG = '{0}' and TIME_STAMP between to_timestamp('{1}', 'YYYY-MM-DD HH24:MI:SS.FF3') and  to_timestamp('{2}', 'YYYY-MM-DD HH24:MI:SS.FF3') ORDER BY TIME_STAMP ASC".format(
                    pointId, fromDate, toDate)
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [list(i) for i in rows] #return data as list

    except Exception as E:
        print("error", E)

# getDayAHeadData('2020-09-10 00:00:00.000', '2020-09-12 00:00:00.000', "GOA")
