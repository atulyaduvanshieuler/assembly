import json
import psycopg2
from psycopg2 import sql
from verify_cocktail_box import verify_function

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
    cocktail_box_id = body["cocktail_box_id"]
    print(emch_number, cocktail_box_id)

    with psycopg2.connect(**database_config) as conn: 
        with conn.cursor() as cur:
            verification=verify_function(cocktail_box_id)
            if verification[0]:

                dbquery_1 = """INSERT INTO cocktail_box_assemblies(cocktail_box) SELECT id FROM cocktail_boxes WHERE cocktail_box_id = (%s)"""
                cur.execute(dbquery_1, (cocktail_box_id,))
                conn.commit()

                dbquery_2="""UPDATE vehicles SET cocktail_box_assembly = sub_query_1.id FROM
                (SELECT id FROM cocktail_box_assemblies WHERE cocktail_box_assemblies.cocktail_box IN
                (SELECT id FROM cocktail_boxes WHERE cocktail_boxes.cocktail_box_id = %s)) AS sub_query_1     
                WHERE vehicles.emch= %s """
                cur.execute(dbquery_2,(cocktail_box_id,emch_number,))
                conn.commit()

                msg = {
                    "message": "cocktail_box with cocktail_box id: %s added successfully in vehicle with following EMCH number: %s"
                    % (cocktail_box_id, emch_number)
                }
            else:
                msg={"message":verification[1]}

    return {"statusCode": 200, "body": json.dumps(msg)}
