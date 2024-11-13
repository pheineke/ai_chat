import asyncio
from flask import Flask, render_template, request, jsonify, redirect, url_for
import ollama
import requests

from chat import * 

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('text')

        add_message(user='user', content=content)

        response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': f"{content}",
        },
        ])

        response = response['message']['content']

        add_message(user='ai', content=response)

    return render_template('index.html')

async def main(content):
    add_message(user='user', content=content)

    response = ollama.chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': f"{content}",
    },
    ])

    response = response['message']['content']

    add_message(user='ai', content=response)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':   
        content = request.form.get('text')     
        asyncio.run(main(content=content))

    return redirect(url_for('.index'))

@app.route("/history", methods=['GET', 'POST'])
def history():
    return jsonify(get_history())


app.run(host='0.0.0.0', port=5000, debug=True)