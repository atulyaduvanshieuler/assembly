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

def verify_function(telematics_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            #Checking whether that vehicle harness is already present in anotther vehicle or not
            dbquery=""" 
                        SELECT id FROM vehicles WHERE telematics IN
                        (SELECT id FROM telematics WHERE telematics_id = %s )
                    """
            cur.execute(dbquery,(telematics_id,))
            telematics_available=cur.fetchall()
            print(telematics_available)
            if telematics_available!=[]:
                return [False,"telematics is present in another vehicle"]
            
            #check whether that vehicle harness was a part of inventory or not
            
            dbquery_2="""
                          SELECT id FROM telematics WHERE telematics_id=%s
                      """
            cur.execute(dbquery_2,(telematics_id, ))
            registered_telematics=cur.fetchall()
            if registered_telematics==[]:
                return [False,"There is no telematics with such id"]
            return [True]

