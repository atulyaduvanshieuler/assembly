import json
import psycopg2
from psycopg2 import sql
from verify_brake_plate import verify_function

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
    brake_plate_id = body["brake_plate_id"]
    print(emch_number, brake_plate_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(brake_plate_id)
            if verification[0]:

                dbquery="""
                            UPDATE semi_sprung_asssemblies 
                            SET brake_plate=sub_query_1.id FROM
                            (SELECT id FROM brake_plates WHERE brake_plate_id=%s) AS sub_query_1,
                            (SELECT semi_sprung_assebly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE semi_sprung_assembly.id=sub_query_2.semi_sprung_assembly
                        """

                cur.execute(dbquery,(brake_plate_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "brake_plate with brake_plate id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (brake_plate_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
