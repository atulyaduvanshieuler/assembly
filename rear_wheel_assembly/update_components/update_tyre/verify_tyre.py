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

def verify_function(tyre_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT tyre FROM rear_wheel_assemblies WHERE rear_wheel_assemblies.tyre IN (SELECT id FROM tyres WHERE tyre_id= %s )
                    """
            cur.execute(dbquery,(tyre_id,))
            tyre_available=cur.fetchall()
            print(tyre_available)
            if tyre_available!=[]:
                return [False,"tyre is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT tyre_id FROM tyres WHERE tyre_id=%s
                      """
            cur.execute(dbquery_2,(tyre_id, ))
            registered_tyre=cur.fetchall()
            if registered_tyre==[]:
                return [False,"There is no tyre with such id"]
            return [True]

