# SakuraEngine.py
# Main engine that combines all Sakura modules

import json
import os
from openai import OpenAI

from .tone_detector import ToneDetector
from .emotion_manager import EmotionManager
from .comfort_manager import ComfortManager
from .dialogue_selector import DialogueSelector
from .prompt_builder import PromptBuilder


class SakuraEngine:
    def __init__(self):
        base_path = "."

        # Load Sakura's files
        self.personality = self.load_json(os.path.join(base_path, "characters", "Sakura.json"))
        self.dialogue = self.load_json(os.path.join(base_path, "dialog_packs", "Sakura_Dialog", "Sakura Dialog.json"))
        self.emotion_rules = self.load_json(os.path.join(base_path, "config", "sakura_emotion.json"))
        self.behavior_rules = self.load_json(os.path.join(base_path, "config", "sakura_behavior.json"))

        # Initialize helper modules
        self.tone_detector = ToneDetector(self.emotion_rules)
        self.emotion_manager = EmotionManager(self.emotion_rules)
        self.comfort_manager = ComfortManager(self.behavior_rules)
        self.dialogue_selector = DialogueSelector(self.dialogue)
        self.prompt_builder = PromptBuilder(self.personality)

        # ---------------------------------------------------------
        # LOAD API KEY FROM Assistant_App/config/api_key.json
        # ---------------------------------------------------------
        api_key = None
        try:
            key_path = os.path.join(base_path, "config", "api_key.json")
            with open(key_path, "r", encoding="utf-8") as f:
                key_data = json.load(f)
                api_key = key_data.get("OPENAI_API_KEY")
        except Exception as e:
            print("Failed to load API key:", e)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)

    def load_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return {}

    def generate_response(self, user_message):
        """
        Full Sakura response pipeline:
        1. Detect tone
        2. Determine emotional state
        3. Apply comfort behaviors
        4. Select dialogue examples
        5. Build final prompt
        6. Send prompt to AI model
        """

        # 1. Tone detection
        tone = self.tone_detector.detect_tone(user_message)

        # 2. Emotional state
        emotional_state = self.emotion_manager.get_emotional_state(tone)

        # 3. Comfort behaviors
        comfort_state = self.comfort_manager.apply_comfort(emotional_state)

        # 4. Dialogue examples
        pool_name = comfort_state.get("dialogue_pool", emotional_state.get("dialogue_pool"))
        example_lines = self.dialogue_selector.get_lines_from_pool(pool_name)

        # 5. Build final prompt
        prompt = self.prompt_builder.build_prompt(
            emotional_state,
            comfort_state,
            example_lines,
            user_message
        )

        # 6. Send prompt to AI model
        ai_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return ai_response.choices[0].message.content

