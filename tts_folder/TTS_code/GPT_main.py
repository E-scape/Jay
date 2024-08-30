import asyncio, os, subprocess, keyboard, time
from config import *
from GPT_function import *
from POI_TTS import poi_tts as tts
from POI_STT import main as stt
def subroutine():
    while True:#ble 신호가 들어오면 실행
        try:
            # 음성 입력 받기
            #tts("명령을 말씀해 주세요.", "prompt.mp3")
            command = "앞에 출입문이 있어?"#stt()  # 실제로는 stt()에서 명령어를 받아야 합니다.
            print(f"인식된 명령: {command}")  # 디버깅을 위한 출력

            if '길 안내' in command.lower():
                tts("길안내를 시작합니다.", "poiroute.mp3")
                subprocess.run(["python", os.path.join(os.path.dirname(__file__), "poi_route_fusion.py")])
                
            else:
                asyncio.run(main(f"{command}"))

        except Exception as e:
            print(f"오류 발생: {e}")
            tts("오류가 발생했습니다. 다시 시도해주세요.", "error.mp3")

        

def main_loop():
    print("키보드 입력 대기 중. 'w'를 눌러야 루프가 실행됩니다.")
    
    # 키보드 입력을 기다리기 위해 True 루프 사용
    while True:
        if keyboard.is_pressed('w'):  # 'w' 키가 눌렸는지 확인
            print("키보드 입력 감지: 'w' 키가 눌렸습니다.")
            subroutine()  # 서브루틴 실행
            time.sleep(1)
            
        else:
            print("키보드 입력 대기 중...")
            time.sleep(0.1)  # 입력 감지 주기를 조정하기 위해 잠시 대기    

if __name__ == '__main__':
    main_loop()
    '''    try:
        asyncio.run(main())s
    finally:
        print("프로그램을 종료합니다.")
        # 모든 외부 리소스 해제
        cv2.destroyAllWindows()
        # 강제 종료
        os.kill(os.getpid(), signal.SIGTERM)'''
