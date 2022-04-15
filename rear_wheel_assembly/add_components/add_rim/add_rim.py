import json
import psycopg2
from psycopg2 import sql
from verify_rim import verify_function

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
    rim_id = body["rim_id"]

    verification=verify_function(rim_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE rear_wheel_assemblies SET rim=(sub_query_2.id) FROM 
                            ( SELECT rear_wheel_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM rims WHERE rim_id= %s ) AS sub_query_2
                            WHERE rear_wheel_assemblies.id= sub_query_1.rear_wheel_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,rim_id))
                conn.commit()

        msg = {
            "message": "rim with rim id: %s added successfully in vehicle with following EMCH number: %s"
            % (rim_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
