import os, asyncio
from playsound import playsound
from google.cloud import texttospeech
from config import mp3_path, CREDENTIALS_PATH

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
os.chdir(mp3_path)

async def poi_tts(text, output_file_name):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = await asyncio.to_thread(
        client.synthesize_speech,
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    async with asyncio.Lock():
        with open(output_file_name, "wb") as out:
            out.write(response.audio_content)
            print(f'실행 파일: "{output_file_name}"')

    await asyncio.sleep(0.1)

    await asyncio.to_thread(playsound, f"{mp3_path}/{output_file_name}")

if __name__ == "__main__":
    asyncio.run(poi_tts("복정역으로 안내할까요?", "is this place.mp3"))