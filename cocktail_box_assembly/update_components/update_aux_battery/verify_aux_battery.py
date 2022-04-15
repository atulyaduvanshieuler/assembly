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

def verify_function(aux_battery_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT aux_battery FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.aux_battery IN (SELECT id FROM aux_batteries WHERE aux_battery_id= %s )
                    """
            cur.execute(dbquery,(aux_battery_id,))
            aux_battery_available=cur.fetchall()
            print(aux_battery_available)
            if aux_battery_available!=[]:
                return [False,"aux_battery is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT aux_battery_id FROM aux_batteries WHERE aux_battery_id=%s
                      """
            cur.execute(dbquery_2,(aux_battery_id, ))
            registered_aux_battery=cur.fetchall()
            if registered_aux_battery==[]:
                return [False,"There is no aux_battery with such id"]
            return [True]

