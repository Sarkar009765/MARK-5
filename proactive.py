import schedule
import time
import threading
from datetime import datetime
from utils import logger

class ProactiveScheduler:
    def __init__(self):
        self.running = False
        self.callbacks = []
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("Proactive scheduler started")

    def stop(self):
        self.running = False

    def _run(self):
        self._setup_jobs()
        while self.running:
            schedule.run_pending()
            time.sleep(60)

    def _setup_jobs(self):
        schedule.every(30).minutes.do(self.check_notifications)
        schedule.every(1).hours.do(self.hourly_check)
        schedule.every(1).days.do(self.daily_summary)

    def on_notification(self, callback):
        self.callbacks.append(callback)

    def check_notifications(self):
        for cb in self.callbacks:
            try:
                cb("check")
            except Exception as e:
                logger.error(f"Notification error: {e}")

    def hourly_check(self):
        for cb in self.callbacks:
            try:
                cb("hourly")
            except Exception as e:
                logger.error(f"Hourly check error: {e}")

    def daily_summary(self):
        for cb in self.callbacks:
            try:
                cb("daily")
            except Exception as e:
                logger.error(f"Daily summary error: {e}")

    def run_now(self, event_type: str):
        if event_type == "check":
            self.check_notifications()
        elif event_type == "hourly":
            self.hourly_check()
        elif event_type == "daily":
            self.daily_summary()


proactive_scheduler = ProactiveScheduler()