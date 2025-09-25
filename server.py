import os
import psycopg2

from flask import Flask, render_template, request

app = Flask(__name__)

data = []

@app.route('/',methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        data.append({'username': request.form.get('username'), 'comment':request.form.get('comment')})
        print(data)
    return render_template('index.html', data=data)