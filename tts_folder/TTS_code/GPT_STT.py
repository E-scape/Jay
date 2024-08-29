import queue, sys, os, pyaudio,  asyncio
from playsound import playsound
from google.cloud import speech
from config import CREDENTIALS_PATH, stt_startsound, stt_endsound

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

async def play_sound_async(sound_file):
    await asyncio.to_thread(playsound, sound_file)

# 오디오 녹음 파라미터
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """마이크로폰 스트림을 열어 오디오 청크를 생성하는 제너레이터입니다."""

    def __init__(self, rate: int = RATE, chunk: int = CHUNK) -> None:
        """오디오와 제너레이터는 메인 스레드에서 보장됩니다."""
        self._rate = rate
        self._chunk = chunk

        # 스레드 안전한 오디오 데이터 버퍼 생성
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self) -> object:
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # API는 현재 단일 채널(모노) 오디오만 지원합니다
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # 오디오 스트림을 비동기적으로 실행하여 버퍼가 오버플로우되지 않도록 합니다.
            # 네트워크 요청 등을 하는 동안 오디오 장치의 버퍼가 오버플로우하는 것을 방지하기 위함입니다.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> None:
        """연결이 끊겼는지 여부에 관계없이 스트림을 닫습니다."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True  
        # 제너레이터가 종료되도록 신호를 보냅니다.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        frame_count: object,
        time_info: object,
        status_flags: object,
    ) -> object:
        """오디오 스트림에서 데이터를 지속적으로 버퍼로 수집합니다.

        Args:
            in_data: 오디오 데이터(bytes 객체)
            frame_count: 캡처된 프레임 수
            time_info: 시간 정보
            status_flags: 상태 플래그

        Returns:
            오디오 데이터(bytes 객체)
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self) -> object:
        """오디오 데이터 스트림에서 오디오 청크를 생성하는 제너레이터입니다.

        Args:
            self: MicrophoneStream 객체

        Yields:
            오디오 청크(bytes 객체)
        """
        while not self.closed:
            # 데이터가 적어도 하나는 있는지 확인하기 위해 블로킹 get()을 사용하고,
            # 청크가 None이면 오디오 스트림의 끝을 나타내므로 반복을 중지합니다.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # 현재 버퍼에 남아 있는 다른 데이터도 소비합니다.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


result = None
done = asyncio.Event()

async def listen_print_loop(responses):
    global result
    num_chars_printed = 0
    
    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue
        
        transcript = result.alternatives[0].transcript

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            done.set()  # 음성 인식이 완료되었음을 알립니다.
            return transcript

    return None

async def main():
    language_code = "ko-KR"
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_spoken_punctuation=True,
        model="command_and_search",
        speech_contexts=[speech.SpeechContext(
            phrases = ["네", "예", "아니요", "아니오"],
            boost = 10.0
        )]
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True, single_utterance=True,
        enable_voice_activity_events=True,
    )

    await play_sound_async(stt_startsound)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content) 
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
    
        # 3초 타이머 설정
        timer = asyncio.create_task(asyncio.sleep(2))
        
        transcript_task = asyncio.create_task(listen_print_loop(responses))
        
        done, pending = await asyncio.wait(
            [timer, transcript_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        transcript = transcript_task.result() if transcript_task in done else None

        await play_sound_async(stt_endsound)
        return transcript

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"인식된 텍스트: {result}")
    else:
        print("음성 인식 시간 초과 또는 인식 실패")