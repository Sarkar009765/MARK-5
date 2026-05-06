import os
import config
from utils import logger

class STT:
    def __init__(self):
        self.vosk_model = None
        self.recognizer = None

    def init_vosk(self):
        try:
            import vosk
            model_path = config.VOICE_MODEL_PATH
            if os.path.exists(model_path):
                self.vosk_model = vosk.Model(model_path)
                self.recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
                logger.info("STT Vosk model loaded")
                return True
            else:
                logger.warning("STT model not found, using fallback")
                return False
        except Exception as e:
            logger.error(f"STT init error: {e}")
            return False

    def listen(self, duration: float = 5.0) -> str:
        if not self.recognizer:
            if not self.init_vosk():
                return input("You: ")

        try:
            import pyaudio
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            
            logger.info(f"Listening for {duration}s...")
            frames = []
            import time
            start_time = time.time()
            
            while time.time() - start_time < duration:
                data = stream.read(4096, exception_on_overflow=False)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            audio_data = b"".join(frames)
            if self.recognizer.AcceptWaveform(audio_data):
                result = eval(self.recognizer.Result())
                text = result.get("text", "")
                logger.info(f"Recognized: {text}")
                return text
            return ""
        except Exception as e:
            logger.error(f"STT listen error: {e}")
            return input("You: ")

stt = STT()