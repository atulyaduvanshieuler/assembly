import json
import psycopg2
from psycopg2 import sql
from verify_reservoir import verify_function

database_config = {
    "user": 'postgres',
    "password": '9812376024',
    "host": '172.19.0.2',
    "port": 5432,
    "dbname": 'postgres'
}
# will take emch and gearbox_id as input
# issue i am facing is ki jaisi hi request dobara bhejta hu ik or row create ho jati h with sam e values
#the solution is ki m jo subassembly me pehle components aaenge unko m unique kr du 


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    emch_number = body["emch"]
    reservoir_id = body["reservoir_id"]
    print(emch_number, reservoir_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(reservoir_id)
            if verification[0]:

                dbquery="""
                            UPDATE break_pedal_assemblies 
                            SET reservoir=sub_query_1.id FROM
                            (SELECT id FROM reservoirs WHERE reservoir_id=%s) AS sub_query_1,
                            (SELECT break_pedal_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE break_pedal_assemblies.id=sub_query_2.break_pedal_assembly
                        """

                cur.execute(dbquery,(reservoir_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "reservoir with reservoir id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (reservoir_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
