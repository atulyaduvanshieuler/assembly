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

def verify_function(battery_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT battery FROM battery_assemblies WHERE battery_assemblies.battery IN (SELECT id FROM batteries WHERE battery_id= %s )
                    """
            cur.execute(dbquery,(battery_id,))
            battery_available=cur.fetchall()
            print(battery_available)
            if battery_available!=[]:
                return [False,"battery is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT battery_id FROM batteries WHERE battery_id=%s
                      """
            cur.execute(dbquery_2,(battery_id, ))
            registered_battery=cur.fetchall()
            if registered_battery==[]:
                return [False,"There is no battery with such id"]
            return [True]

