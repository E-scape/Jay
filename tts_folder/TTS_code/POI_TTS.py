import os, time
from playsound import playsound
from google.cloud import texttospeech
from config import mp3_path, CREDENTIALS_PATH

# Set Google Cloud credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
os.chdir(mp3_path)

def poi_tts(text, output_file_name):

    client = texttospeech.TextToSpeechClient()

    # 텍스트 입력
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 음성 설정 ( 언어 = 한국어, 성별 = 중립)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # 텍스트를 MP3 파일로 변환
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3#LINEAR16
    )

    # 택스트 음성 변환 수행
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 파일 저장
    with open(output_file_name, "wb") as out:
        out.write(response.audio_content)
        print(f'실행 파일: "{output_file_name}"')

    # 파일 재생
    playsound(f"{mp3_path}/{output_file_name}")

# Example usage:
if __name__ == "__main__":
    
    start = time.time()
    poi_tts("복정역으로 안내할까요?", "is this place.mp3")
    end = time.time()
    print(end-start)
    pass
