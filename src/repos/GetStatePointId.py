import oracledb
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config.config import load_config


#load the config.json 
database_config = load_config()

#this function takes input as statename and return point ID of that particular state by quering the ENTITY_MAPPING_TABLE
def getStatePointId(stateName):
    try:
        with oracledb.connect(database_config["DATABASE_URL"]) as connection: #connect to database
            with connection.cursor() as cursor:
                sql = "select ENTITY_TAG from ENTITY_MAPPING_TABLE where ENTITY_FULL_NAME = '{0}'".format(stateName) #SQL query to read point ID
                cursor.execute(sql)
                rows = cursor.fetchall()
                if len(rows) == 0:
                    return None
                return rows[0][0] #return first element from the list


    except Exception as E:
        print("error", E)


print(getStatePointId('GOAS'))