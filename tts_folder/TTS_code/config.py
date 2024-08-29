#POI_TTS.py, POI_STT.py
CREDENTIALS_PATH = r"C:\Users\alsrn\projects\Jay\tts_folder\Json_file\stt_navi.json"

#POI_TTS.py
mp3_path = r"C:\Users\alsrn\projects\Jay\tts_folder\TTS_mp3_file"

image_path = r"C:\Users\alsrn\projects\Jay\tts_folder\image"

#POI_STT.py
stt_startsound = r"~\tts_folder\stt_start,end_sound\stt_start.mp3"
stt_endsound = r"~\tts_folder\stt_start,end_sound\stt_end.mp3"

positive_responses = {
    "네", "예", "넹", "넵", "어", "응", "그래", "얍", "좋아", "yes", "네요",
    "예요", "넹요", "넵요", "어요", "응요", "그래요", "얍요", "좋아요", "yes"
    }

negative_responses = {
    "아니", "아니요", "싫어", "아니야", "no", "nope",
    " 아니", " 아니요", " 싫어", " 아니야", " no", " nope"
    }

retry_responses = {
    "다시검색","다시 검색","다시", "재검색","다시해", "다시해줘", "다시해주세요", "다시해줄래", "다시해줄래요",
    "한번더", "한번더해", "한번더해줘", "한번더해주세요", "한번더해줄래", "한번더해줄래요",
    "retry", "retry please", "retry once more", "retry one more time"
    }    