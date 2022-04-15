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

def verify_function(gearbox_id):
    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery=""" 
                        SELECT cocktail_box FROM cocktail_box_assemblies 
                        WHERE cocktail_box_assemblies.cocktail_box IN 
                        (SELECT id FROM cocktail_boxes WHERE cocktail_box_id= %s )
                    """
            cur.execute(dbquery,(cocktail_box_id,))
            cocktail_box_available=cur.fetchall()
            print(cocktail_box_available)
            if cocktail_box_available!=[]:
                return [False,"cocktail_box is present in another vehicle"]
            
            
            
            dbquery_2="""
                          SELECT cocktail_box_id FROM cocktail_boxes WHERE cocktail_box_id=%s
                      """
            cur.execute(dbquery_2,(cocktail_box_id, ))
            registered_cocktail_box=cur.fetchall()
            if registered_cocktail_box==[]:
                return [False,"There is no cocktail_box with such id"]
            return [True]

