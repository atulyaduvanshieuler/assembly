import json
import psycopg2
from psycopg2 import sql
from verify_trailng_arm import verify_function

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
    trailng_arm_id = body["trailng_arm_id"]
    print(emch_number, trailng_arm_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(trailing_arm_id)
            if verification[0]:

                dbquery_1 = """INSERT INTO semi_sprung_assemblies(trailng_arm) SELECT id FROM trailing_arms WHERE trailing_arm_id = (%s)"""
                cur.execute(dbquery_1, (trailing_arm__id,))
                conn.commit()

                dbquery_2="""UPDATE vehicles SET semi_sprung_assembly = sub_query_1.id FROM
                (SELECT id FROM semi_sprung_assemblies WHERE semi_sprung_assemblies.trailing_arm IN
                (SELECT id FROM trailing_arms WHERE trailing_arms.trailing_arm_id = %s)) AS sub_query_1     
                WHERE vehicles.emch= %s """
                cur.execute(dbquery_2,(trailing_arm_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "trailing_arm with trailing_arm id: %s added successfully in vehicle with following EMCH number: %s"
                    % (trailing_arm_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
