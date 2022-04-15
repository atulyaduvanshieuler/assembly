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

def verify_function(strut_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT strut FROM fork_and_suspension_assemblies WHERE fork_and_suspension_assemblies.strut IN (SELECT id FROM struts WHERE strut_id= %s )
                    """
            cur.execute(dbquery,(strut_id,))
            strut_available=cur.fetchall()
            print(strut_available)
            if strut_available!=[]:
                return [False,"strut is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT strut_id FROM struts WHERE strut_id=%s
                      """
            cur.execute(dbquery_2,(strut_id, ))
            registered_strut=cur.fetchall()
            if registered_strut==[]:
                return [False,"There is no strut with such id"]
            return [True]

