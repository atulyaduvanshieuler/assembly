import json
import psycopg2
from psycopg2 import sql
from verify_gearbox import verify_function

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
    signal_connector_id = body["signal_connector_id"]
    print(emch_number, signal_connector_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(signal_connector_id)
            if verification[0]:

                dbquery="""
                            UPDATE battery_assemblies 
                            SET signal_connector=sub_query_1.id FROM
                            (SELECT id FROM signal_connectors WHERE signal_connector_id=%s) AS sub_query_1,
                            (SELECT battery_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE battery_assemblies.id=sub_query_2.battery_assembly
                        """

                cur.execute(dbquery,(signal_connector_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "signal_connector with signal_connector id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (signal_connector_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
