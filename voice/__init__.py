import queue
import threading
import config
from voice.wakeword import wake_detector
from voice.stt import stt
from voice.tts import tts
from utils import logger

class VoiceLoop:
    def __init__(self, brain):
        self.brain = brain
        self.active = False
        self.q = queue.Queue()
        self.conversation_active = False

    def start(self):
        self.active = True
        wake_detector.start()
        threading.Thread(target=self._wake_loop, daemon=True).start()
        logger.info("Voice loop started")

    def _wake_loop(self):
        while self.active:
            wake_detector.wait_for_wake(timeout=5)
            if not self.active:
                break
            
            logger.info("Wake word detected!")
            tts.speak_async("Yes, old chap?")
            self.conversation_active = True
            
            while self.conversation_active:
                text = stt.listen(duration=8)
                if not text:
                    continue
                
                if "stop" in text.lower() or "exit" in text.lower() or "বন্ধ" in text.lower():
                    tts.speak_async("Very well then.")
                    self.conversation_active = False
                    break
                
                self.q.put(text)
                response = self.brain.process(text)
                tts.speak_async(response)

    def stop(self):
        self.active = False
        self.conversation_active = False
        wake_detector.stop()

voice_loop = None

def start_voice(brain):
    global voice_loop
    voice_loop = VoiceLoop(brain)
    voice_loop.start()

def stop_voice():
    global voice_loop
    if voice_loop:
        voice_loop.stop()