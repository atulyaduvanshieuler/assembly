import json
import psycopg2
from psycopg2 import sql
from verify_brake_switch import verify_function

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
    brake_switch_id = body["brake_switch_id"]

    verification=verify_function(brake_switch_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE break_pedal_assemblies SET brake_switch=(sub_query_2.id) FROM 
                            ( SELECT break_pedal_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM brake_switches WHERE brake_switch_id= %s ) AS sub_query_2
                            WHERE break_pedal_assemblies.id= sub_query_1.break_pedal_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,brake_switch_id))
                conn.commit()

        msg = {
            "message": "brake_switch with brake_switch id: %s added successfully in vehicle with following EMCH number: %s"
            % (brake_switch_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
