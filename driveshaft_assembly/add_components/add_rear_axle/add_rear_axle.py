import json
import psycopg2
from psycopg2 import sql
from verify_rear_axle import verify_function

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

                dbquery_1 = """INSERT INTO driveshaft_assemblies(rear_axle) SELECT id FROM rear_axles WHERE rear_axle_id = (%s)"""
                cur.execute(dbquery_1, (rear_axle_id,))
                conn.commit()

                dbquery_2="""UPDATE vehicles SET driveshaft_assembly = sub_query_1.id FROM
                (SELECT id FROM driveshaft_assemblies WHERE driveshaft_assemblies.rear_axle IN
                (SELECT id FROM rear_axles WHERE rear_axles.rear_axle_id = %s)) AS sub_query_1     
                WHERE vehicles.emch= %s """
                cur.execute(dbquery_2,(rear_axle_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "rear_axle with rear_axle id: %s added successfully in vehicle with following EMCH number: %s"
                    % (rear_axle_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
