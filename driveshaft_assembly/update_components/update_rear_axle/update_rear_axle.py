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
    rear_axle_id = body["rear_axle_id"]
    print(emch_number, rear_axle_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(rear_axle_id)
            if verification[0]:

                dbquery="""
                            UPDATE driveshaft_assemblies 
                            SET rear_axle=sub_query_1.id FROM
                            (SELECT id FROM rear_axles WHERE rear_axle_id=%s) AS sub_query_1,
                            (SELECT driveshaft_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE driveshaft_assemblies.id=sub_query_2.driveshaft_assembly
                        """

                cur.execute(dbquery,(rear_axle_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "rear_axle with rear_axle id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (rear_axle_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
