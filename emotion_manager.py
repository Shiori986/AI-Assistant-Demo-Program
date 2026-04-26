# emotion_manager.py
# Determines Sakura's emotional state based on detected tone

class EmotionManager:
    def __init__(self, emotion_rules):
        self.rules = emotion_rules.get("internal_states", {})
        self.tone_rules = emotion_rules.get("tone_detection", {})

    def get_emotional_state(self, tone):
        """
        Takes a tone label (stress, confusion, joy, neutral)
        and returns Sakura's emotional state + recommended dialogue pool.
        """

        # 1. Stress → Concern state
        if tone == "stress":
            return {
                "state": "concern",
                "dialogue_pool": "comfort.concerned",
                "tone_shift": "soft_concerned"
            }

        # 2. Confusion → Clarification state
        if tone == "confusion":
            return {
                "state": "clarifying",
                "dialogue_pool": "clarification.gentle",
                "tone_shift": "clearer"
            }

        # 3. Joy → Confidence state
        if tone == "joy":
            return {
                "state": "confidence",
                "dialogue_pool": "encouragement.quiet_affirmation",
                "tone_shift": "warm_bright"
            }

        # 4. Neutral → Baseline calm state
        return {
            "state": "calm",
            "dialogue_pool": "greetings.soft",
            "tone_shift": "calm_warm"
        }
