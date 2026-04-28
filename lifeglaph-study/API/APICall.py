# Geminiのライブラリ
from google import genai
from google.genai import types
# GPTのライブラリ
from openai import OpenAI
# Grokのライブラリ
import os
from xai_sdk import Client
from xai_sdk.chat import user, image
# 共通ライブラリ
from PIL import Image
import io
import time

class GeminiContent():
    def __init__(self):
        with open("API/Gemini","r",encoding="utf-8") as f:
            self.GEMINI_API_KEY=f.readline()
        self.client = genai.Client(api_key=self.GEMINI_API_KEY)
        self.model = "gemini-3-pro-preview"
        self.thinking_level = "low"

    def give_test(self,questions):
        response = self.client.models.generate_content(
            model=self.model,
            contents=questions,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level=self.thinking_level)
            ),
        )
        time.sleep(10)
        return response.text

    def give_test_fig(self, questions, fig):
        # 1. MatplotlibのFigureオブジェクトをメモリ上のPNG画像（バイトデータ）に変換
        buf = io.BytesIO()
        fig.savefig(buf, format='png') # figをPNG形式でbufに保存
        buf.seek(0)
        img = Image.open(buf)

        response = self.client.models.generate_content(
            model=self.model,
            contents=[img, questions],
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level=self.thinking_level)
            ),
        )
        buf.close()
        time.sleep(5)
        return response.text

class GPTContent():
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-5.2"

    def give_test(self, questions):
        response = self.client.responses.create(
            model=self.model,
            input=questions
        )
        return (response.output_text)

    def give_test_fig(self, questions, fig):
        # 1. MatplotlibのFigureオブジェクトをメモリ上のPNG画像（バイトデータ）に変換
        buf = io.BytesIO()
        fig.savefig(buf, format='png') # figをPNG形式でbufに保存
        buf.seek(0)
        with open(buf, "rb") as file_content:
            result = self.client.files.create(
                file=file_content,
                purpose="vision",
            )
        file_id = result.id
        buf.close()

        response = self.client.response.create(
            model=self.model,
            input=[
                {
                    "content":[
                        {
                            "type": "input_text",
                            "text": questions
                        },
                        {
                            "type": "input_image",
                            "file_id": file_id,
                        }
                    ]
                }
            ]
        )
        print (response.output_text)

class GrokContent():
    def __init__(self):
        self.client = Client(
            api_key=os.getenv("XAI_API_KEY"),
            management_api_key=os.getenv("XAI_MANAGEMENT_API_KEY"),
            timeout=3600,
        )
        self.model = "grok-4-1-fast-reasoning"

    def give_test(self, questions):
        chat = self.client.chat.create(
            model=self.model,
            store_messages=False
        )
        chat.append(user(questions))
        response = chat.sample()

        return response.content

    def give_test_fig(self, questions, fig):
        # 1. MatplotlibのFigureオブジェクトをメモリ上のPNG画像（バイトデータ）に変換
        buf = io.BytesIO()
        fig.savefig(buf, format='png') # figをPNG形式でbufに保存
        buf.seek(0)
        img = Image.open(buf)

        chat = self.client.chat.create(model=self.model)
        chat.append(
            user(
                questions,
                image(img)
            )
        )
        response = chat.sample()
        return response.content

