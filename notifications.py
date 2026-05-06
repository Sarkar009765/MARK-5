import threading
import time
import config
from utils import logger

class NotificationSystem:
    def __init__(self):
        self.handlers = []

    def start(self):
        logger.info("Notification system ready")

    def send(self, title: str, message: str, urgency: str = "normal"):
        logger.info(f"Notification [{urgency}]: {title} - {message}")
        
        for handler in self.handlers:
            try:
                handler(title, message, urgency)
            except Exception as e:
                logger.error(f"Handler error: {e}")

    def send_text(self, title: str, message: str):
        from voice.tts import tts
        tts.speak_async(f"{title}. {message}")

    def add_handler(self, handler):
        self.handlers.append(handler)

    def toast(self, title: str, message: str):
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5)
        except Exception as e:
            logger.warning(f"Toast unavailable: {e}")
            print(f"[NOTIFICATION] {title}: {message}")


notifier = NotificationSystem()

class NotificationManager:
    def __init__(self):
        self.last_weather_check = 0
        self.last_reminder = None

    def check(self, event_type: str):
        if event_type == "check":
            return self._notification_check()
        elif event_type == "hourly":
            return self._hourly_check()
        elif event_type == "daily":
            return self._daily_check()

    def _notification_check(self):
        current_time = time.time()
        if current_time - self.last_weather_check > 1800:
            try:
                from tools.web import WeatherTool
                w = WeatherTool()
                weather = w.execute(config.LANGUAGE or " Dhaka")
                if weather:
                    notifier.send("Weather", weather, "low")
                self.last_weather_check = current_time
            except Exception as e:
                logger.error(f"Weather check error: {e}")

    def _hourly_check(self):
        try:
            import psutil
            cpu = psutil.cpu_percent()
            if cpu > 90:
                notifier.send("High CPU", f"CPU at {cpu}%", "high")
            
            mem = psutil.virtual_memory()
            if mem.percent > 90:
                notifier.send("High Memory", f"Memory at {mem.percent}%", "high")
            
            disk = psutil.disk_usage('/')
            if disk.percent > 95:
                notifier.send("Low Disk", f"Disk space low ({disk.percent}% used)", "high")
        except Exception as e:
            logger.error(f"System check error: {e}")

    def _daily_check(self):
        notifier.send("Daily Summary", "ClawVis is running. All systems normal.", "low")

    def set_reminder(self, message: str, delay: int = 0):
        self.last_reminder = {"message": message, "time": time.time() + delay}


notification_manager = NotificationManager()