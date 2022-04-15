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

def verify_function(on_board_charger_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT on_board_charger FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.on_board_charger IN (SELECT id FROM on_board_chargers WHERE on_board_charger_id= %s )
                    """
            cur.execute(dbquery,(on_board_charger_id,))
            on_board_charger_available=cur.fetchall()
            print(on_board_charger_available)
            if on_board_charger_available!=[]:
                return [False,"on_board_charger is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT on_board_charger_id FROM on_board_chargers WHERE on_board_charger_id=%s
                      """
            cur.execute(dbquery_2,(on_board_charger_id, ))
            registered_on_board_charger=cur.fetchall()
            if registered_on_board_charger==[]:
                return [False,"There is no on_board_charger with such id"]
            return [True]

