from aiohttp import web
from . import db
import aiohttp_jinja2
import pika
import json



@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return {'questions': questions}


@aiohttp_jinja2.template('detail.html')
async def poll(request):

    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']
        
        try:
            question, choices = await db.get_question(conn,
                                                      question_id)
            
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            'question': question,
            'choices': choices
        }


@aiohttp_jinja2.template('results.html')
async def results(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']

        try:
            question, choices = await db.get_question(conn,
                                                      question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return {
            'question': question,
            'choices': choices
        }


async def vote(request):
    async with request.app['db'].acquire() as conn:

        question_id = int(request.match_info['question_id'])
        data = await request.post()
        question, choices = await db.get_question(conn, question_id)
        try:
            choice_id = int(data['choice'])


        except (KeyError, TypeError, ValueError) as e:
            raise web.HTTPBadRequest(
                text='Você não especificou uma escolha') from e
        try:
            # await db.vote(conn, question_id, choice_id)
            # # RABBIT
            
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            
            channel.basic_publish(exchange='votacao',
                                routing_key='hello',
                                body=json.dumps({
                                    'question_id': question_id,
                                    'choices_id': choice_id,
                                    'text': choices[choice_id - 1][1]
                                }))
            print(f"[x] Enviada escolha {choice_id}:'{choices[choice_id - 1][1]}'")

            connection.close()
            # FIM
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        router = request.app.router
        url = router['results'].url_for(question_id=str(question_id))
        return web.HTTPFound(location=url)