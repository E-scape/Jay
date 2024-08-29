import os
import time
from playsound import playsound, PlaysoundException
from google.cloud import texttospeech
from config import mp3_path, CREDENTIALS_PATH
from function import capture_image, encode_image, send_image_to_chatgpt
from POI_STT import main as stt_main
import asyncio

os.chdir(mp3_path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def safe_playsound(sound):
    try:
        playsound(sound)
    except PlaysoundException as e:
        print(f"플레이사운드 오류: {e}")
        try:
            # 대체 방법: os.system을 사용하여 재생
            os.system(f'start "" "{sound}"')
        except Exception as e:
            print(f"오디오 재생 실패: {e}")

def poi_tts(text, output_file_name):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    output_file_path = os.path.abspath(os.path.join(mp3_path, output_file_name))
    
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'오디오 파일이 "{output_file_path}"에 저장되었습니다.')
    
    print(f"재생할 사운드 파일 경로: {output_file_path}")
    safe_playsound(output_file_path)

async def main_loop():
    stt_result = stt_main()
    if stt_result:
        print("음성인식 결과:", stt_result)
        file_path = await capture_image()
        encoded_image = encode_image(file_path)
        tts_result = await send_image_to_chatgpt(encoded_image, stt_result)
        print("ChatGPT 응답:", tts_result)
        poi_tts(tts_result, "output.mp3")
    else:
        print("음성 인식 실패 또는 시간 초과")

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
    except Exception as e:
        print(f"오류 발생: {e}")
