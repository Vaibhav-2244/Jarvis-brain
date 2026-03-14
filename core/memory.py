class ConversationMemory:
    def __init__(self, max_turns=4):
        self.max_turns = max_turns
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        self._trim()

    def get(self):
        return self.history

    def _trim(self):
        max_messages = self.max_turns * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]
