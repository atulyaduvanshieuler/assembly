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

def verify_function(bottom_link_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT bottom_link FROM fork_and_suspension_assemblies WHERE fork_and_suspension_assemblies.bottom_link IN (SELECT id FROM bottom_links WHERE bottom_link_id= %s )
                    """
            cur.execute(dbquery,(bottom_link_id,))
            bottom_link_available=cur.fetchall()
            print(bottom_link_available)
            if bottom_link_available!=[]:
                return [False,"bottom_link is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT bottom_link_id FROM bottom_links WHERE bottom_link_id=%s
                      """
            cur.execute(dbquery_2,(bottom_link_id, ))
            registered_bottom_link=cur.fetchall()
            if registered_bottom_link==[]:
                return [False,"There is no bottom_link with such id"]
            return [True]

