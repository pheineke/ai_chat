import asyncio
from flask import Flask, render_template, request, jsonify, redirect, url_for
import ollama
import requests
import threading
import time

from chat import * 

app = Flask(__name__)

instruction = []

def thread_main():
    global instruction
    while True:
        if len(instruction) > 0:
            content = instruction.pop()

            add_message(user='user', content=content)

            history = get_history_llm() + [
                    {
                        'role': 'user',
                        'content': f"{content}",
                    },
                ]
            
            print(history)

            response = ollama.chat(
                model='llama3.2', 
                messages=history
            )

            response = response['message']['content']

            add_message(user='assistant', content=response)
        
        time.sleep(1)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':   
        content = request.form.get('text')
        if content != '/clear':
            instruction.append(content)
        else: clear_history()

    return redirect(url_for('.index'))

@app.route("/history", methods=['GET', 'POST'])
def history():
    return jsonify(get_history())


llm_thread = threading.Thread(target = thread_main)
llm_thread.daemon = True
llm_thread.start()

app.run(host='0.0.0.0', port=5000, debug=True)