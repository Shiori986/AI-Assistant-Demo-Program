import os
import json
import uuid
from datetime import datetime

# Import your assistant engines
from SRC.Systems.AssistantEngines.SakuraEngine import SakuraEngine
from SRC.Systems.AssistantEngines.OrigamiEngine import OrigamiEngine


class ConversationManager:
    def __init__(self):
        # Folder for storing conversations
        self.folder = "conversations"
        os.makedirs(self.folder, exist_ok=True)

        # Active assistant engine
        self.engine = None
        self.active_assistant = None


        # Tracks whether a conversation is new (for first-message logic)
        self.is_new_conversation = True

    # ---------------------------------------------------------
    # ASSISTANT SELECTION
    # ---------------------------------------------------------
    def set_active_assistant(self, name):
        """
        Load the correct assistant engine based on the name.
        """
        name = name.lower()

        if name == "sakura":
            self.engine = SakuraEngine()
        elif name == "origami":
            self.engine = OrigamiEngine()
        else:
            raise ValueError(f"Unknown assistant: {name}")

        # Reset first-message flag
        self.is_new_conversation = True

    # ---------------------------------------------------------
    # CREATE NEW CONVERSATION
    # ---------------------------------------------------------
    def create_new_conversation(self):
        convo_id = str(uuid.uuid4())
        convo_path = os.path.join(self.folder, f"{convo_id}.json")

        data = {
            "conversation_id": convo_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }

        with open(convo_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        self.is_new_conversation = True
        return convo_id

    # ---------------------------------------------------------
    # LOAD CONVERSATION
    # ---------------------------------------------------------
    def load_conversation(self, convo_id):
        path = os.path.join(self.folder, f"{convo_id}.json")

        if not os.path.exists(path):
            return {"conversation_id": convo_id, "messages": []}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # SAVE MESSAGE
    # ---------------------------------------------------------
    def save_message(self, convo_id, sender, text):
        path = os.path.join(self.folder, f"{convo_id}.json")

        convo = self.load_conversation(convo_id)
        convo["messages"].append({
            "sender": sender,
            "text": text,
            "timestamp": datetime.now().isoformat()
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(convo, f, indent=4)

    # ---------------------------------------------------------
    # LIST CONVERSATIONS
    # ---------------------------------------------------------
    def list_conversations(self):
        conversations = []

        for filename in os.listdir(self.folder):
            if filename.endswith(".json"):
                path = os.path.join(self.folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                preview = ""
                if data["messages"]:
                    preview = data["messages"][-1]["text"]
                else:
                    preview = "(empty conversation)"

                conversations.append({
                    "conversation_id": data["conversation_id"],
                    "preview": preview
                })

        return conversations

    # ---------------------------------------------------------
    # DELETE CONVERSATION
    # ---------------------------------------------------------
    def delete_conversation(self, convo_id):
        path = os.path.join(self.folder, f"{convo_id}.json")
        if os.path.exists(path):
            os.remove(path)

    # ---------------------------------------------------------
    # GET AI RESPONSE
    # ---------------------------------------------------------
    def get_ai_response(self, user_message):
        """
        Routes the message to the active assistant engine.
        Handles first-message logic.
        """
        if self.engine is None:
            raise ValueError("No assistant engine has been selected.")

        # First message → use assistant's special intro
        if self.is_new_conversation:
            self.is_new_conversation = False
            if hasattr(self.engine, "get_first_message"):
                return self.engine.get_first_message()
            # If engine has no special first message
            return self.engine.generate_response(user_message)

        # Normal conversation
        return self.engine.generate_response(user_message)
