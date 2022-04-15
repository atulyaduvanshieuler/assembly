import json
import psycopg2
from psycopg2 import sql
from verify_signal_connector import verify_function

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
    signal_connector_id = body["signal_connector_id"]

    verification=verify_function(signal_connector_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE battery_assemblies SET signal_connector=(sub_query_2.id) FROM 
                            ( SELECT battery_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM signal_connectors WHERE signal_connector_id= %s ) AS sub_query_2
                            WHERE battery_assemblies.id= sub_query_1.battery_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,signal_connector_id))
                conn.commit()

        msg = {
            "message": "signal_connector with signal_connector id: %s added successfully in vehicle with following EMCH number: %s"
            % (signal_connector_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
