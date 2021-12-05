# rabbitmq_vote
Projeto para estudo de Aiohttp e RabbitMQ. Se trata de um sistema de votos que envia mensagens via RabbitMQ para uma fila e essa fila para o banco de dados.



Para rodar o banco
´´´
docker run --rm -e POSTGRES_PASSWORD=postgres -it -p 5432:5432 postgres
´´´

Para rodar o app
´´´
python -m aiohttpdemo_polls
´´´


Para ver a movimentaçao
´´´
docker logs -f rabbitmq
´´´