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

def verify_function(biw_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            #Checking whether that vehicle harness is already present in anotther vehicle or not
            dbquery=""" 
                        SELECT id FROM vehicles WHERE biw IN
                        (SELECT id FROM biws WHERE biw_id = %s )
                    """
            cur.execute(dbquery,(biw_id,))
            biw_available=cur.fetchall()
            print(biw_available)
            if biw_available!=[]:
                return [False,"biw is present in another vehicle"]
            
            #check whether that vehicle harness was a part of inventory or not
            
            dbquery_2="""
                          SELECT id FROM biws WHERE biw_id=%s
                      """
            cur.execute(dbquery_2,(biw_id, ))
            registered_biw=cur.fetchall()
            if registered_biw==[]:
                return [False,"There is no biw with such id"]
            return [True]

