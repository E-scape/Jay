# function.py
import os
import cv2, signal, base64, requests, time
from config import *
from key import *
from gpt_tts import poi_tts

async def capture_image():
    # 이미지 저장 경로
    save_folder = image_path
    
    # 저장 폴더가 존재하지 않으면 생성
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 비디오 캡처 객체 생성
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cap.read()
    if ret:
        # 이미지 저장 파일 경로 생성
        file_path = os.path.join(save_folder, 'captured_image.jpg')
        time.sleep(0.3)  # 카메라 안정화 대기
        cv2.imwrite(file_path, frame)  # 이미지 저장
    else:
        raise ValueError("Failed to capture image from webcam")

    # 리소스 해제
    cap.release()
    cv2.destroyAllWindows()

    return file_path  # 저장된 이미지 파일의 전체 경로 반환

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def send_image_to_chatgpt(encoded_image, transcription_result):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_KEY}"
    }
    message_content = f"나는 시각장애인이야. 답변을 짧고 명확하게 답변해줘. 내 질문은 다음과 같다. {transcription_result}."

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
    response.raise_for_status()
    return response.json()


async def main(command: str):
    transcription_result = command
    file_path = await capture_image()
    encoded_image = encode_image(file_path)
    result = await send_image_to_chatgpt(encoded_image, transcription_result)
    result_last = result['choices'][0]['message']['content']
    print(result_last)
    await poi_tts(f"{result_last}","response.mp3")
    cv2.destroyAllWindows()
        # 강제 종료
    os.kill(os.getpid(), signal.SIGTERM)