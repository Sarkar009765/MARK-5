import threading
import config
from utils import logger

class TTS:
    def __init__(self):
        self.engine = None
        self.rate = 150
        self.volume = 1.0
        self.voice = None

    def init(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower() or '大卫' in voice.name or 'Zira' in voice.name:
                    self.engine.setProperty('voice', voice.id)
                    break
            
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            logger.info("TTS pyttsx3 initialized")
            return True
        except Exception as e:
            logger.error(f"TTS init error: {e}")
            return False

    def speak(self, text: str, use_async: bool = False):
        if not self.engine:
            self.init()
        
        if not self.engine:
            logger.warning("TTS unavailable, printing instead")
            print(f"Jarvis: {text}")
            return

        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS speak error: {e}")
                print(f"Jarvis: {text}")

        if use_async:
            threading.Thread(target=_speak, daemon=True).start()
        else:
            _speak()

    def speak_async(self, text: str):
        self.speak(text, use_async=True)

tts = TTS()