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

def verify_function(dc_dc_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT dc_dc FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.dc_dc IN (SELECT id FROM dc_dcs WHERE dc_dc_id= %s )
                    """
            cur.execute(dbquery,(dc_dc_id,))
            dc_dc_available=cur.fetchall()
            print(dc_dc_available)
            if dc_dc_available!=[]:
                return [False,"dc_dc is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT dc_dc_id FROM dc_dcs WHERE dc_dc_id=%s
                      """
            cur.execute(dbquery_2,(dc_dc_id, ))
            registered_dc_dc=cur.fetchall()
            if registered_dc_dc==[]:
                return [False,"There is no dc_dc with such id"]
            return [True]

