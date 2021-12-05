# polls/init_db.py
from sqlalchemy import create_engine, MetaData

from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.db import question, choice


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(question.insert(), [
        {'question_text': 'O que há de novo?',
         'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.execute(choice.insert(), [
        {'choice_text': 'Não muito', 'votos': 0, 'question_id': 1},
        {'choice_text': 'O céu', 'votos': 0, 'question_id': 1},
        {'choice_text': 'Apenas hackeando de novo', 'votos': 0, 'question_id': 1},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)