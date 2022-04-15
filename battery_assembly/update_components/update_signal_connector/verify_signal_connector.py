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

def verify_function(signal_connector_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT {component_key_in_subassembly_table} FROM battery_assemblies WHERE battery_assemblies.{component_key_in_subassembly_table} IN (SELECT id FROM {component_table_name} WHERE signal_connector_id= %s )
                    """
            cur.execute(dbquery,(signal_connector_id,))
            signal_connector_available=cur.fetchall()
            print(signal_connector_available)
            if signal_connector_available!=[]:
                return [False,"signal_connector is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT signal_connector_id FROM {component_table_name} WHERE signal_connector_id=%s
                      """
            cur.execute(dbquery_2,(signal_connector_id, ))
            registered_signal_connector=cur.fetchall()
            if registered_signal_connector==[]:
                return [False,"There is no signal_connector with such id"]
            return [True]

