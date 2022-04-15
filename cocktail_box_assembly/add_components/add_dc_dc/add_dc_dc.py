import json
import psycopg2
from psycopg2 import sql
from verify_dc_dc import verify_function

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
    dc_dc_id = body["dc_dc_id"]

    verification=verify_function(dc_dc_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE cocktail_box_assemblies SET dc_dc=(sub_query_2.id) FROM 
                            ( SELECT cocktail_box_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM dc_dcs WHERE dc_dc_id= %s ) AS sub_query_2
                            WHERE cocktail_box_assemblies.id= sub_query_1.cocktail_box_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,dc_dc_id))
                conn.commit()

        msg = {
            "message": "dc_dc with dc_dc id: %s added successfully in vehicle with following EMCH number: %s"
            % (dc_dc_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
