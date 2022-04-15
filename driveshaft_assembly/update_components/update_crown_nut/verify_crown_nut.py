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

def verify_function(crown_nut_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT crown_nut FROM driveshaft_assemblies WHERE driveshaft_assemblies.crown_nut IN (SELECT id FROM crown_nuts WHERE crown_nut_id= %s )
                    """
            cur.execute(dbquery,(crown_nut_id,))
            crown_nut_available=cur.fetchall()
            print(crown_nut_available)
            if crown_nut_available!=[]:
                return [False,"crown_nut is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT crown_nut_id FROM crown_nuts WHERE crown_nut_id=%s
                      """
            cur.execute(dbquery_2,(crown_nut_id, ))
            registered_crown_nut=cur.fetchall()
            if registered_crown_nut==[]:
                return [False,"There is no crown_nut with such id"]
            return [True]

