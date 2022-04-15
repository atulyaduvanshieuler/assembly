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

def verify_function(hub_assembly_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT hub_assembly FROM semi_sprung_assemblies WHERE semi_sprung_assemblies.hub_assembly IN (SELECT id FROM hub_assemblies WHERE hub_assembly_id= %s )
                    """
            cur.execute(dbquery,(hub_assembly_id,))
            hub_assembly_available=cur.fetchall()
            print(hub_assembly_available)
            if hub_assembly_available!=[]:
                return [False,"hub_assembly is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT hub_assembly_id FROM hub_assemblies WHERE hub_assembly_id=%s
                      """
            cur.execute(dbquery_2,(hub_assembly_id, ))
            registered_hub_assembly=cur.fetchall()
            if registered_hub_assembly==[]:
                return [False,"There is no hub_assembly with such id"]
            return [True]

