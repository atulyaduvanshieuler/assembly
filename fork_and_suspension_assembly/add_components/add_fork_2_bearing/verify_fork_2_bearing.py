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

def verify_function(fork_2_bearing_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT fork_2_bearing FROM fork_and_suspension_assemblies WHERE fork_and_suspension_assemblies.fork_2_bearing IN (SELECT id FROM fork_2_bearings WHERE fork_2_bearing_id= %s )
                    """
            cur.execute(dbquery,(fork_2_bearing_id,))
            fork_2_bearing_available=cur.fetchall()
            print(fork_2_bearing_available)
            if fork_2_bearing_available!=[]:
                return [False,"fork_2_bearing is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT fork_2_bearing_id FROM fork_2_bearings WHERE fork_2_bearing_id=%s
                      """
            cur.execute(dbquery_2,(fork_2_bearing_id, ))
            registered_fork_2_bearing=cur.fetchall()
            if registered_fork_2_bearing==[]:
                return [False,"There is no fork_2_bearing with such id"]
            return [True]

