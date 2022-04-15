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

def verify_function(load_body_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            #Checking whether that vehicle harness is already present in anotther vehicle or not
            dbquery=""" 
                        SELECT id FROM vehicles WHERE load_body IN
                        (SELECT id FROM load_bodies WHERE load_body_id = %s )
                    """
            cur.execute(dbquery,(load_body_id,))
            load_body_available=cur.fetchall()
            print(load_body_available)
            if load_body_available!=[]:
                return [False,"load_body is present in another vehicle"]
            
            #check whether that vehicle harness was a part of inventory or not
            
            dbquery_2="""
                          SELECT id FROM load_bodies WHERE load_body_id=%s
                      """
            cur.execute(dbquery_2,(load_body_id, ))
            registered_load_body=cur.fetchall()
            if registered_load_body==[]:
                return [False,"There is no load_body with such id"]
            return [True]

