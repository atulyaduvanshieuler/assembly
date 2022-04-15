import json
import psycopg2
from psycopg2 import sql

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
    battery_id = body["battery_id"]

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:

            dbquery = """
                        SELECT battery_id FROM batteries
                            WHERE batteries.id IN(
                                SELECT battery FROM battery_assemblies
                                    WHERE battery_assemblies.id IN (
                                    SELECT battery_assembly FROM vehicles
                                    WHERE emch= %s
                                )
                            );
                            
                        """
            cur.execute(dbquery, (emch_number,))
            present_array=cur.fetchall()
            if battery_id in present_array:
                msg = {
                            "message": True
                        }
            else:
                msg = {
                            "message": False
                        }

    return {"statusCode": 200, "body": json.dumps(msg)}
