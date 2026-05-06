import os
import queue
import threading
import config
from utils import logger

class WakeWordDetector:
    def __init__(self):
        self.q = queue.Queue()
        self.listening = False
        self.audio_stream = None
        self.vosk_model = None
        self.recognizer = None

    def init_vosk(self):
        try:
            import vosk
            model_path = config.VOICE_MODEL_PATH
            if os.path.exists(model_path):
                self.vosk_model = vosk.Model(model_path)
                self.recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
                logger.info("Vosk model loaded")
                return True
            else:
                logger.warning(f"Vosk model not found at {model_path}")
                return False
        except Exception as e:
            logger.error(f"Vosk init error: {e}")
            return False

    def start(self):
        if not self.init_vosk():
            logger.info("Using fallback mic mode")
            return
        
        self.listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self):
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            self.audio_stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            
            while self.listening:
                data = self.audio_stream.read(4096, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    if config.WAKE_WORD.lower() in result.lower():
                        self.q.put("wake")
        except Exception as e:
            logger.error(f"Wake word error: {e}")

    def wait_for_wake(self, timeout=None):
        try:
            return self.q.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self):
        self.listening = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

wake_detector = WakeWordDetector()