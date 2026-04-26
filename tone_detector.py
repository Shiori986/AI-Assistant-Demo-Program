# tone_detector.py
# Simple keyword-based tone detection for Sakura

class ToneDetector:
    def __init__(self, emotion_rules):
        self.rules = emotion_rules.get("tone_detection", {})

    def detect_tone(self, user_message):
        message = user_message.lower()

        # 1. Check for stress keywords
        stress = self.rules.get("user_stress", {})
        for word in stress.get("keywords", []):
            if word in message:
                return "stress"

        # 2. Check for confusion keywords
        confusion = self.rules.get("user_confusion", {})
        for word in confusion.get("keywords", []):
            if word in message:
                return "confusion"

        # 3. Check for joy keywords
        joy = self.rules.get("user_joy", {})
        for word in joy.get("keywords", []):
            if word in message:
                return "joy"

        # 4. If no tone detected, return neutral
        return "neutral"
