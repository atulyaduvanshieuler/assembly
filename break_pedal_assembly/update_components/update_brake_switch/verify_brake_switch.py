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

def verify_function(brake_switch_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT brake_switch FROM break_pedal_assemblies WHERE break_pedal_assemblies.brake_switch IN (SELECT id FROM brake_switches WHERE brake_switch_id= %s )
                    """
            cur.execute(dbquery,(brake_switch_id,))
            brake_switch_available=cur.fetchall()
            print(brake_switch_available)
            if brake_switch_available!=[]:
                return [False,"brake_switch is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT brake_switch_id FROM brake_switches WHERE brake_switch_id=%s
                      """
            cur.execute(dbquery_2,(brake_switch_id, ))
            registered_brake_switch=cur.fetchall()
            if registered_brake_switch==[]:
                return [False,"There is no brake_switch with such id"]
            return [True]

