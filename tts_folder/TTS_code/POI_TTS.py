import os, pygame
from google.cloud import texttospeech
from config import mp3_path, CREDENTIALS_PATH

# Set Google Cloud credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
os.chdir(mp3_path)

def poi_tts(text, output_file_name):
    # pygame 초기화
    #pygame.init()

    client = texttospeech.TextToSpeechClient()

    # 텍스트 입력
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 음성 설정 ( 언어 = 한국어, 성별 = 중립)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # 텍스트를 MP3 파일로 변환
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 택스트 음성 변환 수행
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio content to the specified file
    with open(output_file_name, "wb") as out:
        out.write(response.audio_content)
        print(f'실행 파일: "{output_file_name}"')
        

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the output MP3 file
    pygame.mixer.music.load(output_file_name)
    pygame.mixer.music.play()

    # Wait until the sound finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up pygame resources
    pygame.mixer.quit()
    #pygame.quit()

# Example usage:
if __name__ == "__main__":
    poi_tts("복정역으로 안내할까요?", "이장소로 안내할까요.mp3")
    pass
