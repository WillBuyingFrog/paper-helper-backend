import json
from channels.generic.websocket import AsyncWebsocketConsumer
import httpx

class TranslateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        origin_text = text_data_json['origin_text']

        # 调用LLM API获取翻译结果
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.deepseek.com/v1/chat/completions',
                json={
                    # 这里填写API所需的payload
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
                    "temperature": 0.3,
                    "top_p": 1
                },
                headers={
                    # 这里填写所需的headers
                },
                timeout=None  # 设置为None以允许无限超时，根据你的需求调整
            )
            translate_text = response.json()

        # 发送翻译结果到WebSocket
        await self.send(text_data=json.dumps({
            'translate_text': translate_text
        }))