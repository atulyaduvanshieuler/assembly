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

def verify_function(upper_and_lower_cone_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT upper_and_lower_cone FROM fork_and_suspension_assemblies WHERE fork_and_suspension_assemblies.upper_and_lower_cone IN (SELECT id FROM upper_and_lower_cones WHERE upper_and_lower_cone_id= %s )
                    """
            cur.execute(dbquery,(upper_and_lower_cone_id,))
            upper_and_lower_cone_available=cur.fetchall()
            print(upper_and_lower_cone_available)
            if upper_and_lower_cone_available!=[]:
                return [False,"upper_and_lower_cone is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT upper_and_lower_cone_id FROM upper_and_lower_cones WHERE upper_and_lower_cone_id=%s
                      """
            cur.execute(dbquery_2,(upper_and_lower_cone_id, ))
            registered_upper_and_lower_cone=cur.fetchall()
            if registered_upper_and_lower_cone==[]:
                return [False,"There is no upper_and_lower_cone with such id"]
            return [True]

