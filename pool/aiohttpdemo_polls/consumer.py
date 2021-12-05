#!/usr/bin/env python
import psycopg2
import pika
import db
import json
import aiopg.sa
from settings import config
import psycopg2


try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# channel.queue_bind(exchange='logs', queue='hello')

print(' [*] Esperando por logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    
    data = json.loads(body)
    cur = conn.cursor()
    cur.execute(
        'update choice set votes = votes + 1 where question_id = %s and id = %s',
        (data['question_id'], data['choices_id'])
        )
    conn.commit()
    print(" [x] %r" % body)

channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

channel.start_consuming()


