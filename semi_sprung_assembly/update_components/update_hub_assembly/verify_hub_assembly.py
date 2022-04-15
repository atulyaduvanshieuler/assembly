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

def verify_function({component_name}_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT {component_key_in_subassembly_table} FROM {subassembly_table_name} WHERE {subassembly_table_name}.{component_key_in_subassembly_table} IN (SELECT id FROM {component_table_name} WHERE {component_name}_id= %s )
                    """
            cur.execute(dbquery,({component_name}_id,))
            {component_name}_available=cur.fetchall()
            print({component_name}_available)
            if {component_name}_available!=[]:
                return [False,"{component_name} is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT {component_name}_id FROM {component_table_name} WHERE {component_name}_id=%s
                      """
            cur.execute(dbquery_2,({component_name}_id, ))
            registered_{component_name}=cur.fetchall()
            if registered_{component_name}==[]:
                return [False,"There is no {component_name} with such id"]
            return [True]

