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

def verify_function(rim_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT rim FROM front_wheel_assemblies WHERE front_wheel_assemblies.rim IN (SELECT id FROM rims WHERE rim_id= %s )
                    """
            cur.execute(dbquery,(rim_id,))
            rim_available=cur.fetchall()
            print(rim_available)
            if rim_available!=[]:
                return [False,"rim is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT rim_id FROM rims WHERE rim_id=%s
                      """
            cur.execute(dbquery_2,(rim_id, ))
            registered_rim=cur.fetchall()
            if registered_rim==[]:
                return [False,"There is no rim with such id"]
            return [True]

