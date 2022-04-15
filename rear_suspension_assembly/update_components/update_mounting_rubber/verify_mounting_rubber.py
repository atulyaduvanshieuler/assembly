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

def verify_function(mounting_rubber_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT mounting_rubber FROM rear_suspension_assemblies WHERE rear_suspension_assemblies.mounting_rubber IN (SELECT id FROM mounting_rubbers WHERE mounting_rubber_id= %s )
                    """
            cur.execute(dbquery,(mounting_rubber_id,))
            mounting_rubber_available=cur.fetchall()
            print(mounting_rubber_available)
            if mounting_rubber_available!=[]:
                return [False,"mounting_rubber is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT mounting_rubber_id FROM mounting_rubbers WHERE mounting_rubber_id=%s
                      """
            cur.execute(dbquery_2,(mounting_rubber_id, ))
            registered_mounting_rubber=cur.fetchall()
            if registered_mounting_rubber==[]:
                return [False,"There is no mounting_rubber with such id"]
            return [True]

