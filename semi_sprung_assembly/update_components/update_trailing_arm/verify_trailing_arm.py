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

def verify_function(trailing_arm_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT trailing_arm FROM semi_sprung_assemblies 
                        WHERE semi_sprung_assemblies.trailing_arm IN 
                        (SELECT id FROM trailing_arms WHERE trailing_arm_id= %s )
                    """
            cur.execute(dbquery,(trailing_arm_id,))
            trailing_arm_available=cur.fetchall()
            print(trailing_arm_available)
            if trailing_arm_available!=[]:
                return [False,"trailing_arm is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT trailing_arm_id FROM trailing_arms WHERE trailing_arm_id=%s
                      """
            cur.execute(dbquery_2,(trailing_arm_id, ))
            registered_trailing_arm=cur.fetchall()
            if registered_trailing_arm==[]:
                return [False,"There is no trailing_arm with such id"]
            return [True]

