import json
import psycopg2
from psycopg2 import sql
from verify_on_board_charger import verify_function

database_config = {
    "user": 'postgres',
    "password": '9812376024',
    "host": '172.19.0.2',
    "port": 5432,
    "dbname": 'postgres'
}
#input will be motor_id and emch
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    emch_number = body["emch"]
    on_board_charger_id = body["on_board_charger_id"]

    verification=verify_function(on_board_charger_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE cocktail_box_assemblies SET on_board_charger=(sub_query_2.id) FROM 
                            ( SELECT cocktail_box_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM on_board_chargers WHERE on_board_charger_id= %s ) AS sub_query_2
                            WHERE cocktail_box_assemblies.id= sub_query_1.cocktail_box_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,on_board_charger_id))
                conn.commit()

        msg = {
            "message": "on_board_charger with on_board_charger id: %s added successfully in vehicle with following EMCH number: %s"
            % (on_board_charger_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
