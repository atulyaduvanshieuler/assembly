import json
import psycopg2
from psycopg2 import sql
from verify_brake_plate import verify_function

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
    brake_plate_id = body["brake_plate_id"]

    verification=verify_function(brake_plate_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE semi_sprung_assemblies SET brake_plates=(sub_query_2.id) FROM 
                            ( SELECT semi_sprung_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM brake_plates WHERE brake_plate_id= %s ) AS sub_query_2
                            WHERE semi_sprung_assemblies.id= sub_query_1.semi_sprung_assembly                                
                            """
                cur.execute(dbquery, (emch_number,brake_plate_id))
                conn.commit()

        msg = {
            "message": "brake_plate with brake_plate id: %s added successfully in vehicle with following EMCH number: %s"
            % (brake_plate_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
