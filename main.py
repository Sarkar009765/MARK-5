import sys
import schedule
import time
import threading
import config
from brain.llm import Brain
from memory.db import memory
from voice.tts import tts
from proactive import proactive_scheduler, notification_manager
from notifications import notifier
from learning import learning
from telegram_bot import init_telegram
from utils import logger

class ClawVis:
    def __init__(self):
        self.running = False
        self.scheduler_thread = None
        self.brain = None
        self.telegram = None

    def start(self):
        self.running = True
        logger.info("ClawVis starting...")
        logger.info(f"RAM Target: ≤2.2GB | Model: {config.MODEL_NAME}")
        
        tts.init()
        
        self.brain = Brain()
        
        self.start_telegram()
        
        self.start_proactive()
        
        tts.speak_async("ClawVis activated. Say Jarvis to begin.")
        logger.info("ClawVis is ready. Say 'Jarvis' to activate!")
        
        self.main_loop()

    def start_telegram(self):
        if config.TELEGRAM_BOT_TOKEN:
            self.telegram = init_telegram(self.brain)
            self.telegram.start()
            logger.info("Telegram bot started")

    def start_proactive(self):
        proactive_scheduler.on_notification(notification_manager.check)
        proactive_scheduler.start()
        notifier.start()
        logger.info("Proactive system started")

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
            proactive_scheduler.stop()
            if self.telegram:
                self.telegram.stop()
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