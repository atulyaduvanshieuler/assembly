import json
import psycopg2
from psycopg2 import sql
from verify_drum import verify_function

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
    drum_id = body["drum_id"]

    verification=verify_function(drum_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE semi_sprung_assemblies SET drum=(sub_query_2.id) FROM 
                            ( SELECT semi_sprung_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM drums WHERE drum_id= %s ) AS sub_query_2
                            WHERE semi_sprung_assemblies.id= sub_query_1.semi_sprung_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,drum_id))
                conn.commit()

        msg = {
            "message": "drum with drum id: %s added successfully in vehicle with following EMCH number: %s"
            % (drum_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
