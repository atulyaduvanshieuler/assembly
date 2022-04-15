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

def verify_function(tmc_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT tmc FROM break_pedal_assemblies WHERE break_pedal_assemblies.tmc IN (SELECT id FROM tmcs WHERE tmc_id= %s )
                    """
            cur.execute(dbquery,(tmc_id,))
            tmc_available=cur.fetchall()
            print(tmc_available)
            if tmc_available!=[]:
                return [False,"tmc is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT tmc_id FROM tmcs WHERE tmc_id=%s
                      """
            cur.execute(dbquery_2,(tmc_id, ))
            registered_tmc=cur.fetchall()
            if registered_tmc==[]:
                return [False,"There is no tmc with such id"]
            return [True]

