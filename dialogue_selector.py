# dialogue_selector.py
# Selects the correct dialogue pool for Sakura based on emotional + comfort state

import random

class DialogueSelector:
    def __init__(self, dialogue_pack):
        self.dialogue = dialogue_pack

    def get_lines_from_pool(self, pool_name):
        """
        pool_name examples:
        - "comfort.concerned"
        - "clarification.gentle"
        - "encouragement.quiet_affirmation"
        - "greetings.soft"
        """

        # Split pool name into category + subcategory
        try:
            category, sub = pool_name.split(".")
        except ValueError:
            # If pool name is invalid, fall back to soft greetings
            category, sub = "greetings", "soft"

        # Navigate the dialogue pack safely
        category_data = self.dialogue.get(category, {})
        lines = category_data.get(sub, [])

        # If no lines found, fall back to a safe default
        if not lines:
            return ["I'm here if you need me."]

        # Return 2–3 random lines to give the AI examples
        return random.sample(lines, min(3, len(lines)))
