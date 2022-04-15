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

def verify_function(brake_plate_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT brake_plate FROM semi_sprung_assemblies WHERE semi_sprung_assemblies.brake_plate IN (SELECT id FROM brake_plates WHERE brake_plate_id= %s )
                    """
            cur.execute(dbquery,(brake_plate_id,))
            brake_plate_available=cur.fetchall()
            print(brake_plate_available)
            if brake_plate_available!=[]:
                return [False,"brake_plate is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT brake_plate_id FROM brake_plates WHERE brake_plate_id=%s
                      """
            cur.execute(dbquery_2,(brake_plate_id, ))
            registered_brake_plate=cur.fetchall()
            if registered_brake_plate==[]:
                return [False,"There is no brake_plate with such id"]
            return [True]

