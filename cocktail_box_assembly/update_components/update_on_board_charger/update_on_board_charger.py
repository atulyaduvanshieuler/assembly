import json
import psycopg2
from psycopg2 import sql
from verify_on_board_charger import verify_function

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
    on_board_charger_id = body["on_board_charger_id"]
    print(emch_number, on_board_charger_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(on_board_charger_id)
            if verification[0]:

                dbquery="""
                            UPDATE cocktail_box_assemblies 
                            SET on_board_charger=sub_query_1.id FROM
                            (SELECT id FROM on_board_chargers WHERE on_board_charger_id=%s) AS sub_query_1,
                            (SELECT cocktail_box_assembly FROM vehicles WHERE emch=%s) AS sub_query_2
                            WHERE cocktail_box_assemblies.id=sub_query_2.cocktail_box_assembly
                        """

                cur.execute(dbquery,(on_board_charger_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "on_board_charger with on_board_charger id: %s updated successfully in vehicle with following EMCH number: %s"
                    % (on_board_charger_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
