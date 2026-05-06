import json
from pathlib import Path
import config
from memory.db import memory
from utils import logger
from tinydb import Query

class LearningModule:
    def __init__(self):
        self.pattern_file = config.DATA_DIR / "learning.json"
        self.patterns = self._load_patterns()
        self.feedback_file = config.DATA_DIR / "feedback.json"
        self.feedback = self._load_feedback()

    def _load_patterns(self) -> dict:
        if self.pattern_file.exists():
            with open(self.pattern_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_feedback(self) -> dict:
        if self.feedback_file.exists():
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def learn(self, user_input: str, response: str):
        user_lower = user_input.lower()
        words = user_lower.split()
        
        for word in words:
            if word not in self.patterns:
                self.patterns[word] = []
            
            if response not in self.patterns[word]:
                self.patterns[word].append(response)
        
        self._save_patterns()

    def _save_patterns(self):
        with open(self.pattern_file, "w", encoding="utf-8") as f:
            json.dump(self.patterns, f, indent=2, ensure_ascii=False)

    def get_feedback(self, user_input: str, response: str):
        key = f"{user_input}|{response}"
        return self.feedback.get(key, 0)

    def add_feedback(self, user_input: str, response: str, rating: int):
        key = f"{user_input}|{response}"
        current = self.feedback.get(key, 0)
        self.feedback[key] = current + rating
        
        with open(self.feedback_file, "w", encoding="utf-8") as f:
            json.dump(self.feedback, f, indent=2)

    def get_best_response(self, user_input: str) -> str:
        user_lower = user_input.lower()
        words = user_lower.split()
        
        scores = {}
        for word in words:
            if word in self.patterns:
                for resp in self.patterns[word]:
                    scores[resp] = scores.get(resp, 0) + 1
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        return None

    def get_stats(self) -> str:
        pattern_count = len(self.patterns)
        feedback_count = len(self.feedback)
        
        positive = sum(1 for v in self.feedback.values() if v > 0)
        negative = sum(abs(v) for v in self.feedback.values() if v < 0)
        
        return (f"Patterns learned: {pattern_count}\n"
                f"Feedback received: {feedback_count}\n"
                f"Positive: {positive}, Negative: {negative}")


learning = LearningModule()