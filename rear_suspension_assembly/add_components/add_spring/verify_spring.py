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

def verify_function(spring_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT spring FROM rear_suspension_assemblies 
                        WHERE rear_suspension_assemblies.spring IN 
                        (SELECT id FROM springs WHERE spring_id= %s )
                    """
            cur.execute(dbquery,(spring_id,))
            spring_available=cur.fetchall()
            print(spring_available)
            if spring_available!=[]:
                return [False,"spring is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT spring_id FROM springs WHERE spring_id=%s
                      """
            cur.execute(dbquery_2,(spring_id, ))
            registered_spring=cur.fetchall()
            if registered_spring==[]:
                return [False,"There is no spring with such id"]
            return [True]

