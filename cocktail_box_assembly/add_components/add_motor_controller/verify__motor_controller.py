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

def verify_function(motor_controller_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT motor_controller FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.motor_controller IN (SELECT id FROM motor_controllers WHERE motor_controller_id= %s )
                    """
            cur.execute(dbquery,(motor_controller_id,))
            motor_controller_available=cur.fetchall()
            print(motor_controller_available)
            if motor_controller_available!=[]:
                return [False,"motor_controller is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT motor_controller_id FROM motor_controllers WHERE motor_controller_id=%s
                      """
            cur.execute(dbquery_2,(motor_controller_id, ))
            registered_motor_controller=cur.fetchall()
            if registered_motor_controller==[]:
                return [False,"There is no motor_controller with such id"]
            return [True]

