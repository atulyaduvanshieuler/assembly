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

def verify_function(mark_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            #Checking whether that vehicle harness is already present in anotther vehicle or not
            dbquery=""" 
                        SELECT id FROM vehicles WHERE mark IN
                        (SELECT id FROM marks WHERE mark_id = %s )
                    """
            cur.execute(dbquery,(mark_id,))
            mark_available=cur.fetchall()
            print(mark_available)
            if mark_available!=[]:
                return [False,"mark is present in another vehicle"]
            
            #check whether that vehicle harness was a part of inventory or not
            
            dbquery_2="""
                          SELECT id FROM marks WHERE mark_id=%s
                      """
            cur.execute(dbquery_2,(mark_id, ))
            registered_mark=cur.fetchall()
            if registered_mark==[]:
                return [False,"There is no mark with such id"]
            return [True]

