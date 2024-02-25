from flask import Flask, request
import requests
import json
import os

os.environ['FLASK_DEBUG'] = '1'

app = Flask(__name__)

translate_prompt = ""

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question')
    # 这里你需要替换为你的deepseek平台的API地址和API key
    url = "https://api.deepseek.com/v1/chat/completions"
    payload = json.dumps({
        "messages": [
            {
            "content": "You are a helpful assistant",
            "role": "system"
            },
            {
            "content": question,
            "role": "user"
            }
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "stop": None,
        "stream": False,
        "temperature": 1,
        "top_p": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-6ddecaa5bd764980b42bdfb7b18d408f'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    answer = response.text
    return answer   


@app.route('/translate', methods=['POST'])
def translate():
    
    # 从发送来的请求的body中获取原文，发送过来的格式为body中form-data格式的信息，form-data中有一个key为origin_text，对应value是需要翻译的原文
    origin_text = request.form.get('origin_text')

    url = "https://api.deepseek.com/v1/chat/completions"
    # print(translate_prompt + origin_text)
    
    
    payload = json.dumps({
        "messages": [
            {
            "content": "你是一个专业的论文翻译助手",
            "role": "system"
            },
            {
            "content": translate_prompt + origin_text,
            "role": "user"
            }
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "stop": None,
        "stream": False,
        "temperature": 1,
        "top_p": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-6ddecaa5bd764980b42bdfb7b18d408f'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    answer = response.json()
    translate_text = answer['choices'][0]['message']['content']

    return translate_text
    # answer = response.text
    # return answer



if __name__ == '__main__':
    # 从同目录的translate_prompt.txt中获取两边翻译的prompt
    translate_prompt = open("translate_prompt.txt", "r").read()
    app.run(host='0.0.0.0', port=5000)

# sk-6ddecaa5bd764980b42bdfb7b18d408f