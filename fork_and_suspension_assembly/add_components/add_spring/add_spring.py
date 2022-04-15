import json
import psycopg2
from psycopg2 import sql
from verify_spring import verify_function

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
    spring_id = body["spring_id"]

    verification=verify_function(spring_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE fork_and_suspension_assemblies SET spring=(sub_query_2.id) FROM 
                            ( SELECT fork_and_suspension_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM springs WHERE spring_id= %s ) AS sub_query_2
                            WHERE fork_and_suspension_assemblies.id= sub_query_1.fork_and_suspension_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,spring_id))
                conn.commit()

        msg = {
            "message": "spring with spring id: %s added successfully in vehicle with following EMCH number: %s"
            % (spring_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
