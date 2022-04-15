import json
import psycopg2
from psycopg2 import sql
from verify_hub_assembly import verify_function

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
    hub_assembly_id = body["hub_assembly_id"]

    verification=verify_function(hub_assembly_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE semi_sprung_assemblies SET hub_assembly=(sub_query_2.id) FROM 
                            ( SELECT semi_sprung_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM hub_assemblies WHERE hub_assembly_id= %s ) AS sub_query_2
                            WHERE semi_sprung_assemblies.id= sub_query_1.semi_sprung_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,hub_assembly_id))
                conn.commit()

        msg = {
            "message": "hub_assembly with hub_assembly id: %s added successfully in vehicle with following EMCH number: %s"
            % (hub_assembly_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
