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

def verify_function(arc_reactor_assembly_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT arc_reactor_assembly FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.arc_reactor_assembly IN (SELECT id FROM arc_reactor_assemblies WHERE arc_reactor_assembly_id= %s )
                    """
            cur.execute(dbquery,(arc_reactor_assembly_id,))
            arc_reactor_assembly_available=cur.fetchall()
            print(arc_reactor_assembly_available)
            if arc_reactor_assembly_available!=[]:
                return [False,"arc_reactor_assembly is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT arc_reactor_assembly_id FROM arc_reactor_assemblies WHERE arc_reactor_assembly_id=%s
                      """
            cur.execute(dbquery_2,(arc_reactor_assembly_id, ))
            registered_arc_reactor_assembly=cur.fetchall()
            if registered_arc_reactor_assembly==[]:
                return [False,"There is no arc_reactor_assembly with such id"]
            return [True]

