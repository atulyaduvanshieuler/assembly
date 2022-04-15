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

def verify_function(caliper_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT caliper FROM disc_brake_assemblies WHERE disc_brake_assemblies.caliper IN (SELECT id FROM calipers WHERE caliper_id= %s )
                    """
            cur.execute(dbquery,(caliper_id,))
            caliper_available=cur.fetchall()
            print(caliper_available)
            if caliper_available!=[]:
                return [False,"caliper is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT caliper_id FROM calipers WHERE caliper_id=%s
                      """
            cur.execute(dbquery_2,(caliper_id, ))
            registered_caliper=cur.fetchall()
            if registered_caliper==[]:
                return [False,"There is no caliper with such id"]
            return [True]

