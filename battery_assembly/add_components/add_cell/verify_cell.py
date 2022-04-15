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

def verify_function(cell_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT cell FROM battery_assemblies 
                        WHERE battery_assemblies.cell IN 
                        (SELECT id FROM cells WHERE cell_id= %s )
                    """
            cur.execute(dbquery,(cell_id,))
            cell_available=cur.fetchall()
            print(cell_available)
            if cell_available!=[]:
                return [False,"cell is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT cell_id FROM cells WHERE cell_id=%s
                      """
            cur.execute(dbquery_2,(cell_id, ))
            registered_cell=cur.fetchall()
            if registered_cell==[]:
                return [False,"There is no cell with such id"]
            return [True]

