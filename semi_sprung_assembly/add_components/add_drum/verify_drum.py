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

def verify_function(drum_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT drum FROM semi_sprung_assemblies 
                        WHERE semi_sprung_assemblies.drum IN 
                        (SELECT id FROM drums WHERE drum_id= %s )
                    """
            cur.execute(dbquery,(drum_id,))
            drum_available=cur.fetchall()
            print(drum_available)
            if drum_available!=[]:
                return [False,"drum is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT drum_id FROM drums WHERE drum_id=%s
                      """
            cur.execute(dbquery_2,(drum_id, ))
            registered_drum=cur.fetchall()
            if registered_drum==[]:
                return [False,"There is no drum with such id"]
            return [True]

