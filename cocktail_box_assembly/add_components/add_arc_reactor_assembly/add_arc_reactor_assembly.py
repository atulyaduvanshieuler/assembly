import json
import psycopg2
from psycopg2 import sql
from verify_arc_reactor_assembly import verify_function

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
    arc_reactor_assembly_id = body["arc_reactor_assembly_id"]

    verification=verify_function(arc_reactor_assembly_id)
    if verification[0]:
        with psycopg2.connect(**database_config) as conn: 
            with conn.cursor() as cur:

                dbquery = """
                            UPDATE cocktail_box_assemblies SET arc_reactor_assembly=(sub_query_2.id) FROM 
                            ( SELECT cocktail_box_assembly FROM vehicles WHERE emch=%s ) AS sub_query_1,
                            (SELECT id FROM arc_reactor_assemblies WHERE arc_reactor_assembly_id= %s ) AS sub_query_2
                            WHERE cocktail_box_assemblies.id= sub_query_1.cocktail_box_assembly
                                
                            """
                cur.execute(dbquery, (emch_number,arc_reactor_assembly_id))
                conn.commit()

        msg = {
            "message": "arc_reactor_assembly with arc_reactor_assembly id: %s added successfully in vehicle with following EMCH number: %s"
            % (arc_reactor_assembly_id, emch_number)
        }
    else:
        msg={
            "message":verification[1]
        }

    return {"statusCode": 200, "body": json.dumps(msg)}
