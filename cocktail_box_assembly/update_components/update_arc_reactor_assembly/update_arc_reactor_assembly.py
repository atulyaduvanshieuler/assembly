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
    arc_reactor_assembly_id = body["arc_reactor_assembly_id"]
    print(emch_number, arc_reactor_assembly_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(arc_reactor_assembly_id)
            if verification[0]:

                dbquery="""
                            UPDATE cocktail_box_assemblies 
                            SET arc_reactor_assembly=sub_query_1.id FROM
                            (SELECT id FROM arc_reactor_assemblies WHERE arc_reactor_assembly_id=%s) AS sub_query_1,
                            (SELECT cocktail_box_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE cocktail_box_assemblies.id=sub_query_2.cocktail_box_assembly
                        """

                cur.execute(dbquery,(arc_reactor_assembly_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "arc_reactor_assembly with arc_reactor_assembly id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (arc_reactor_assembly_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
