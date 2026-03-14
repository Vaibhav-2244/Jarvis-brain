class ConversationState:
    def __init__(self):
        self.entities = {}

    def update_from_text(self, user_input):
        words = user_input.split()

        # Basic entity capture pattern:
        # "X is Y" → store as fact
        if " is " in user_input.lower():
            parts = user_input.split(" is ")
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value = parts[1].strip()
                if len(key) < 40:
                    self.entities[key] = value

    def get_context_block(self):
        if not self.entities:
            return ""

        lines = ["KNOWN CONTEXT:"]
        for k, v in self.entities.items():
            lines.append(f"- {k}: {v}")

        return "\n".join(lines)

    def get(self, key):
        return self.entities.get(key.lower())
