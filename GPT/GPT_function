# function.py
import os
from playsound import playsound
import pyaudio
import threading
import time
import cv2
import base64
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from config import *
import requests
from POI_STT import main as stt_main



async def capture_image():
    file_path = 'captured_image.jpg'
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(file_path, frame)
    else:
        raise ValueError("Failed to capture image from webcam")

    cap.release()
    cv2.destroyAllWindows()
    return file_path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def send_image_to_chatgpt(encoded_image,stt_result):
    global result
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    message_content = f"나는 시각장애인이야. {stt_result} 한국어로 짧게 설명해줘."

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message_content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.2,  # 창의성과 일관성의 균형을 위해 0.7 설정
        "top_p": 0.9,  # 확률 질량 기반의 응답 제한
        "max_tokens": 80,  # 응답의 최대 길이
        "n": 1,  # 생성할 응답의 수
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    return result['choices'][0]['message']['content']


   
