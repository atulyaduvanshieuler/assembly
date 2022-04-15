FROM public.ecr.aws/lambda/python:3.8

COPY update_reservoir.py requirements.txt verify_reservoir.py ./

RUN python3.8 -m pip install -r requirements.txt -t .


#RUN '/var/lang/bin/python3.8 -m pip install --upgrade pip'

RUN pip install psycopg2-binary

#RUN pg_ctl -D /var/lib/postgresql/data -l logfile start

# Command can be overwritten by providing a different command in the template directly.
CMD ["update_reservoir.lambda_handler"]

