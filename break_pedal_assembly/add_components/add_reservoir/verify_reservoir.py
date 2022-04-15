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

def verify_function(reservoir_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT reservoir FROM break_pedal_assemblies 
                        WHERE break_pedal_assemblies.reservoir IN 
                        (SELECT id FROM reservoirs WHERE reservoir_id= %s )
                    """
            cur.execute(dbquery,(reservoir_id,))
            reservoir_available=cur.fetchall()
            print(reservoir_available)
            if reservoir_available!=[]:
                return [False,"reservoir is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT reservoir_id FROM reservoirs WHERE reservoir_id=%s
                      """
            cur.execute(dbquery_2,(reservoir_id, ))
            registered_reservoir=cur.fetchall()
            if registered_reservoir==[]:
                return [False,"There is no reservoir with such id"]
            return [True]

