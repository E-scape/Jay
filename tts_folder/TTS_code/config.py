#POI_TTS.py, POI_STT.py
CREDENTIALS_PATH = r"<your_path>(gcloud_credentials_path)/Json_file/~~.json"

#POI_TTS.py
mp3_path = r"<your_path>/tts_folder/TTS_mp3_file"

#POI_STT.py
stt_startsound = r"<your_path>/stt_start,end_sound/stt_start.mp3"
stt_endsound = r"<your_path>/stt_start,end_sound/stt_end.mp3"



#poi_route_fusion.py
Tmap_key = "Tmap_api_key"

positive_responses = {
    "네", "예", "넹", "넵", "어", "응", "그래", "얍", "좋아", "yes", "네요",
    "예요", "넹요", "넵요", "어요", "응요", "그래요", "얍요", "좋아요", "yes"
    }

negative_responses = {
    "아니", "아니요", "싫어", "아니야", "no", "nope",
    " 아니", " 아니요", " 싫어", " 아니야", " no", " nope"
    }
