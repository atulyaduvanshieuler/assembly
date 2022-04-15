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

def verify_function(rotor_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT rotor FROM disc_brake_assemblies WHERE disc_brake_assemblies.rotor IN (SELECT id FROM rotors WHERE rotor_id= %s )
                    """
            cur.execute(dbquery,(rotor_id,))
            rotor_available=cur.fetchall()
            print(rotor_available)
            if rotor_available!=[]:
                return [False,"rotor is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT rotor_id FROM rotors WHERE rotor_id=%s
                      """
            cur.execute(dbquery_2,(rotor_id, ))
            registered_rotor=cur.fetchall()
            if registered_rotor==[]:
                return [False,"There is no rotor with such id"]
            return [True]

