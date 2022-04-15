import json
import psycopg2
from psycopg2 import sql
from verify_crown_nut import verify_function

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
    crown_nut_id = body["crown_nut_id"]

    verification=verify_function(crown_nut_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE driveshaft_assemblies SET crown_nut=(sub_query_2.id) FROM 
                            ( SELECT driveshaft_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM crown_nuts WHERE crown_nut_id= %s ) AS sub_query_2
                            WHERE driveshaft_assemblies.id= sub_query_1.driveshaft_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,crown_nut_id))
                conn.commit()

        msg = {
            "message": "crown_nut with crown_nut id: %s added successfully in vehicle with following EMCH number: %s"
            % (crown_nut_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
