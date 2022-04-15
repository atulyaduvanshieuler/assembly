import json
import psycopg2
from psycopg2 import sql

database_config = {
    "user": 'postgres',
    "password": '9812376024',
    "host": '172.19.0.2',
    "port": 5432,
    "dbname": 'postgres'
}

def verify_function(bms_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT bms FROM battery_assemblies WHERE battery_assemblies.bms IN (SELECT id FROM bmses WHERE bms_id= %s )
                    """
            cur.execute(dbquery,(bms_id,))
            bms_available=cur.fetchall()
            print(bms_available)
            if bms_available!=[]:
                return [False,"bms is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT bms_id FROM bmses WHERE bms_id=%s
                      """
            cur.execute(dbquery_2,(bms_id, ))
            registered_bms=cur.fetchall()
            if registered_bms==[]:
                return [False,"There is no bms with such id"]
            return [True]

