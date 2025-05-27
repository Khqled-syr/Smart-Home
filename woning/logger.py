import datetime
from collections import deque


class Logger:
    def __init__(self, filename="smart_home.log", max_messages=50):
        self.filename = filename
        self.recent_messages = deque(
            maxlen=max_messages
        )  # Store recent messages in memory

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.recent_messages.append(log_entry)  # Add to recent messages
        with open(self.filename, "a") as f:
            f.write(log_entry + "\n")

    def get_recent_messages(self):
        return list(self.recent_messages)
