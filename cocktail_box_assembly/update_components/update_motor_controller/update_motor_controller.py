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
    motor_controller_id = body["motor_controller_id"]
    print(emch_number, motor_controller_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(motor_controller_id)
            if verification[0]:

                dbquery="""
                            UPDATE cocktail_box_assemblies 
                            SET {component_column_name_in_subassembly_table}=sub_query_1.id FROM
                            (SELECT id FROM {component_table_name} WHERE motor_controller_id=%s) AS sub_query_1,
                            (SELECT cocktail_box_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE cocktail_box_assemblies.id=sub_query_2.cocktail_box_assembly
                        """

                cur.execute(dbquery,(motor_controller_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "motor_controller with motor_controller id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (motor_controller_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
