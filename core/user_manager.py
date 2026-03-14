import os
import json
from datetime import datetime

USERS_DIR = "data/users"
MAX_SUMMARIES = 100
MEMORY_EXPIRY_DAYS = 90


class UserManager:
    def __init__(self):
        os.makedirs(USERS_DIR, exist_ok=True)
        self.current_user = None
        self.profile = None

    def load_user(self, name):
        filename = os.path.join(USERS_DIR, f"{name.lower()}.json")
        existed = os.path.exists(filename)

        if not existed:
            self.profile = self._create_new_user(name)
            self.current_user = name.lower()
            self._save()
        else:
            with open(filename, "r") as f:
                self.profile = json.load(f)
            self.current_user = name.lower()

        self._cleanup_memory()
        return self.profile, existed

    def _create_new_user(self, name):
        return {
            "name": name,
            "face_encoding": [],
            "facts": {},
            "long_term_memory": [],
            "last_seen": str(datetime.now().date())
        }

    def _save(self):
        if not self.current_user:
            return

        filename = os.path.join(USERS_DIR, f"{self.current_user}.json")
        with open(filename, "w") as f:
            json.dump(self.profile, f, indent=2)

    def update_fact(self, key, value):
        self.profile["facts"][key] = value
        self._save()

    def add_summary(self, summary, tags=None):
        entry = {
            "date": str(datetime.now().date()),
            "summary": summary,
            "tags": tags or []
        }

        self.profile["long_term_memory"].append(entry)

        # Limit memory size
        if len(self.profile["long_term_memory"]) > MAX_SUMMARIES:
            self.profile["long_term_memory"] = \
                self.profile["long_term_memory"][-MAX_SUMMARIES:]

        self._save()

    def _cleanup_memory(self):
        today = datetime.now().date()
        cleaned = []

        for item in self.profile["long_term_memory"]:
            item_date = datetime.fromisoformat(item["date"]).date()
            if (today - item_date).days <= MEMORY_EXPIRY_DAYS:
                cleaned.append(item)

        self.profile["long_term_memory"] = cleaned
        self._save()

    def get_context_block(self):
        if not self.profile:
            return ""

        lines = [
            f"CURRENT USER: {self.profile['name']}",
            "KNOWN FACTS:"
        ]

        for k, v in self.profile["facts"].items():
            lines.append(f"- {k}: {v}")

        if self.profile["long_term_memory"]:
            lines.append("RECENT SUMMARIES:")
            for item in self.profile["long_term_memory"][-5:]:
                lines.append(f"- {item['summary']}")

        return "\n".join(lines)