# comfort_manager.py
# Applies Sakura's comfort behaviors based on emotional state

class ComfortManager:
    def __init__(self, behavior_rules):
        self.rules = behavior_rules.get("comfort_behaviors", {})

    def apply_comfort(self, emotional_state):
        """
        Takes Sakura's emotional state (from EmotionManager)
        and returns comfort actions + animation + dialogue pool adjustments.
        """

        state = emotional_state.get("state", "calm")

        # 1. Stress → use stress comfort behaviors
        if state == "concern":
            behavior = self.rules.get("stress_detected", {})
            return {
                "actions": behavior.get("actions", []),
                "animation": behavior.get("animation", "concerned"),
                "dialogue_pool": behavior.get("dialogue_pool", "comfort.soft")
            }

        # 2. Confusion → use confusion support behaviors
        if state == "clarifying":
            behavior = self.rules.get("confusion_support", {})
            return {
                "actions": behavior.get("actions", []),
                "animation": behavior.get("animation", "thinking"),
                "dialogue_pool": behavior.get("dialogue_pool", "clarification.gentle")
            }

        # 3. Joy → use joy amplification behaviors
        if state == "confidence":
            behavior = self.rules.get("joy_amplification", {})
            return {
                "actions": behavior.get("actions", []),
                "animation": behavior.get("animation", "celebrating"),
                "dialogue_pool": behavior.get("dialogue_pool", "encouragement.quiet_affirmation")
            }

        # 4. Neutral → no special comfort behavior
        return {
            "actions": [],
            "animation": "idle",
            "dialogue_pool": emotional_state.get("dialogue_pool", "greetings.soft")
        }
