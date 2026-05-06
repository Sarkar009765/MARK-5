import os
from pathlib import Path
from tinydb import TinyDB, Query
import config

class MemoryDB:
    def __init__(self):
        self.db = TinyDB(config.MEMORY_DB)
        self.conversations = self.db.table("conversations")
        self.patterns = self.db.table("patterns")
        self.preferences = self.db.table("preferences")

    def add_message(self, role: str, content: str):
        self.conversations.insert({
            "role": role,
            "content": content,
            "timestamp": self._get_timestamp()
        })
        self._cleanup()

    def get_conversations(self, limit: int = None) -> list:
        if limit:
            return self.conversations.all()[-limit:]
        return self.conversations.all()

    def save_pattern(self, pattern: str, response: str):
        existing = self.patterns.search(Query()["pattern"] == pattern)
        if existing:
            self.patterns.update(
                {"count": existing[0]["count"] + 1, "response": response},
                Query()["pattern"] == pattern
            )
        else:
            self.patterns.insert({"pattern": pattern, "response": response, "count": 1})

    def get_patterns(self) -> list:
        return self.patterns.all()

    def save_preference(self, key: str, value: str):
        existing = self.preferences.search(Query()["key"] == key)
        if existing:
            self.preferences.update({"value": value}, Query()["key"] == key)
        else:
            self.preferences.insert({"key": key, "value": value})

    def get_preference(self, key: str) -> str:
        result = self.preferences.search(Query()["key"] == key)
        return result[0]["value"] if result else None

    def _cleanup(self):
        all_msgs = self.conversations.all()
        if len(all_msgs) > config.MAX_MEMORY_MESSAGES:
            for msg in all_msgs[:-config.MAX_MEMORY_MESSAGES]:
                self.conversations.remove(doc_ids=[msg.doc_id])

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


memory = MemoryDB()