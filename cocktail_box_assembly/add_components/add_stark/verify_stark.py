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

def verify_function(stark_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT stark FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.stark IN (SELECT id FROM starks WHERE stark_id= %s )
                    """
            cur.execute(dbquery,(stark_id,))
            stark_available=cur.fetchall()
            print(stark_available)
            if stark_available!=[]:
                return [False,"stark is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT stark_id FROM starks WHERE stark_id=%s
                      """
            cur.execute(dbquery_2,(stark_id, ))
            registered_stark=cur.fetchall()
            if registered_stark==[]:
                return [False,"There is no stark with such id"]
            return [True]

