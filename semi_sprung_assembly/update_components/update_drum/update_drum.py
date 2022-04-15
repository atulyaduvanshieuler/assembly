import json
import psycopg2
from psycopg2 import sql
from verify_drum import verify_function

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
    drum_id = body["drum_id"]
    print(emch_number, drum_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(drum_id)
            if verification[0]:

                dbquery="""
                            UPDATE semi_sprung_assemblies 
                            SET drum=sub_query_1.id FROM
                            (SELECT id FROM drums WHERE drum_id=%s) AS sub_query_1,
                            (SELECT semi_sprung_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE semi_sprung_assemblies.id=sub_query_2.semi_sprung_assembly
                        """

                cur.execute(dbquery,(drum_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "drum with drum id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (drum_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
