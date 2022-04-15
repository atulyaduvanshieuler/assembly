import json
import psycopg2
from psycopg2 import sql
from verify_battery_box import verify_function

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
    battery_box_id = body["battery_box_id"]

    verification=verify_function(battery_box_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE battery_assemblies SET battery_box=(sub_query_2.id) FROM 
                            ( SELECT battery_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM battery_boxes WHERE battery_box_id= %s ) AS sub_query_2
                            WHERE battery_assemblies.id= sub_query_1.battery_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,battery_box_id))
                conn.commit()

        msg = {
            "message": "battery_box with battery_box id: %s added successfully in vehicle with following EMCH number: %s"
            % (battery_box_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
