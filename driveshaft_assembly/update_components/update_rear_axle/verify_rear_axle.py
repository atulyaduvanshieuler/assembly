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

def verify_function(rear_axle_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT rear_axle FROM driveshaft_assemblies WHERE driveshaft_assemblies.rear_axle IN (SELECT id FROM rear_axles WHERE rear_axle_id= %s )
                    """
            cur.execute(dbquery,(rear_axle_id,))
            rear_axle_available=cur.fetchall()
            print(rear_axle_available)
            if rear_axle_available!=[]:
                return [False,"rear_axle is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT rear_axle_id FROM rear_axles WHERE rear_axle_id=%s
                      """
            cur.execute(dbquery_2,(rear_axle_id, ))
            registered_rear_axle=cur.fetchall()
            if registered_rear_axle==[]:
                return [False,"There is no rear_axle with such id"]
            return [True]

