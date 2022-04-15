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

def verify_function(battery_box_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT battery_box FROM battery_assemblies WHERE battery_assemblies.battery_box IN (SELECT id FROM battery_boxes WHERE battery_box_id= %s )
                    """
            cur.execute(dbquery,(battery_box_id,))
            battery_box_available=cur.fetchall()
            print(battery_box_available)
            if battery_box_available!=[]:
                return [False,"battery_box is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT battery_box_id FROM battery_boxes WHERE battery_box_id=%s
                      """
            cur.execute(dbquery_2,(battery_box_id, ))
            registered_battery_box=cur.fetchall()
            if registered_battery_box==[]:
                return [False,"There is no battery_box with such id"]
            return [True]

