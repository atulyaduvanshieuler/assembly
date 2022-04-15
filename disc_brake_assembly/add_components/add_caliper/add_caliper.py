import json
import psycopg2
from psycopg2 import sql
from verify_caliper import verify_function

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
    caliper_id = body["caliper_id"]

    verification=verify_function(caliper_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE disc_brake_assemblies SET caliper=(sub_query_2.id) FROM 
                            ( SELECT disc_brake_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM calipers WHERE caliper_id= %s ) AS sub_query_2
                            WHERE disc_brake_assemblies.id= sub_query_1.disc_brake_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,caliper_id))
                conn.commit()

        msg = {
            "message": "caliper with caliper id: %s added successfully in vehicle with following EMCH number: %s"
            % (caliper_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
