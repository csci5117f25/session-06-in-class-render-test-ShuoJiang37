import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import logging
from flask import Flask, render_template, request, current_app
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
pool = None


def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']  
    current_app.logger.info("Creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()

data = []

@app.route('/', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        comment = request.form.get('comment')
        with get_db_cursor(True) as cur:
            current_app.logger.info("Adding user %s with comment: %s", username, comment)
            data.append({'username': username, 'comment': comment})
            cur.execute(
                "INSERT INTO users (username, usercomment) VALUES (%s, %s)",
                (username, comment)
            )
    return render_template('index.html', data=data)

with app.app_context():
    setup()

