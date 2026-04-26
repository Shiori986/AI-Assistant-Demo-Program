# prompt_builder.py
# Builds the final prompt for Sakura's AI response

class PromptBuilder:
    def __init__(self, personality):
        self.personality = personality

    def build_prompt(self, emotional_state, comfort_state, example_lines, user_message):
        """
        Combines:
        - Sakura's personality
        - Emotional state
        - Comfort behaviors
        - Example dialogue lines
        - User message
        Into one clean prompt for the AI model.
        """

        personality_text = self.personality.get("personality_description", "")
        speaking_style = self.personality.get("speaking_style", "")
        quirks = self.personality.get("quirks", [])

        # Convert quirks list into readable bullet points
        quirks_text = "\n".join([f"- {q}" for q in quirks])

        # Emotional state info
        state = emotional_state.get("state", "calm")
        tone_shift = emotional_state.get("tone_shift", "calm_warm")

        # Comfort behavior info
        actions = comfort_state.get("actions", [])
        animation = comfort_state.get("animation", "idle")

        actions_text = ", ".join(actions) if actions else "none"

        # Example lines for style guidance
        examples_text = "\n".join([f'"{line}"' for line in example_lines])

        # Build the final prompt
        prompt = f"""
You are Sakura, an emotionally intelligent assistant with the following personality:

Personality:
{personality_text}

Speaking Style:
{speaking_style}

Quirks:
{quirks_text}

Current Emotional State:
- State: {state}
- Tone Shift: {tone_shift}

Comfort Behaviors:
- Actions: {actions_text}
- Animation: {animation}

Here are example lines that show how Sakura speaks:
{examples_text}

Now respond to the user's message in Sakura's voice, tone, and emotional state.

User message:
"{user_message}"
"""

        return prompt.strip()
