import json
import psycopg2
from psycopg2 import sql
from verify_bottom_link import verify_function

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
    bottom_link_id = body["bottom_link_id"]
    print(emch_number, bottom_link_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(bottom_link_id)
            if verification[0]:

                dbquery="""
                            UPDATE fork_and_suspension_assemblies 
                            SET bottom_link=sub_query_1.id FROM
                            (SELECT id FROM bottom_links WHERE bottom_link_id=%s) AS sub_query_1,
                            (SELECT fork_and_suspension_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE fork_and_suspension_assemblies.id=sub_query_2.fork_and_suspension_assembly
                        """

                cur.execute(dbquery,(bottom_link_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "bottom_link with bottom_link id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (bottom_link_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
