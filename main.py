import sys
import schedule
import time
import threading
import config
from brain.llm import Brain
from memory.db import memory
from voice.tts import tts
from utils import logger

class ClawVis:
    def __init__(self):
        self.running = False
        self.scheduler_thread = None
        self.brain = None

    def start(self):
        self.running = True
        logger.info("ClawVis starting...")
        logger.info(f"RAM Target: ≤2.2GB | Model: {config.MODEL_NAME}")
        
        tts.init()
        
        self.brain = Brain()
        
        self.start_scheduler()
        
        tts.speak_async("ClawVis activated. Say Jarvis to begin.")
        logger.info("ClawVis is ready. Say 'Jarvis' to activate!")
        
        self.main_loop()

    def start_scheduler(self):
        def run_schedule():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
        self.scheduler_thread.start()
        logger.info("Scheduler started")

    def main_loop(self):
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.running = False

def main():
    try:
        app = ClawVis()
        app.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()