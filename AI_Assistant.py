import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Needed for loading the placeholder image

# Import your internal modules
from SRC.Systems.conversation_manager import ConversationManager
from SRC.Components.chat_window import ChatWindow
from SRC.Components.AssistantSelectionWindow import AssistantSelectionWindow


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_SETTINGS_PATH = os.path.join(BASE_DIR, "user_settings.json")


class MainMenu(tk.Tk):
    """
    Main application window.
    Left side = Navigation menu
    Right side = Dynamic content panel (setup screen or assistant placeholder)
    """

    def __init__(self):
        super().__init__()

        self.title("Multi-Assistant Desktop App")
        self.geometry("1100x650")
        self.configure(bg="#e8e8e8")

        # Shared conversation manager
        self.manager = ConversationManager()

        # Active assistant name
        self.active_assistant = None

        # Load settings
        self.load_user_settings()

        # Build UI layout
        self.build_layout()

        # Render right panel based on assistant selection
        self.update_right_panel()

    # ---------------------------------------------------------
    # LOAD / SAVE SETTINGS
    # ---------------------------------------------------------
    def load_user_settings(self):
        """
        Loads the user's selected assistant from user_settings.json.
        If missing, defaults to None (setup screen).
        """
        if not os.path.exists(USER_SETTINGS_PATH):
            self.active_assistant = None
            return

        try:
            with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.active_assistant = data.get("active_assistant", None)

                if self.active_assistant:
                    self.manager.set_active_assistant(self.active_assistant)

        except Exception as e:
            print("Failed to load user settings:", e)
            self.active_assistant = None

    def save_user_settings(self):
        """
        Saves the currently selected assistant.
        """
        data = {"active_assistant": self.active_assistant}

        try:
            with open(USER_SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Failed to save user settings:", e)

    # ---------------------------------------------------------
    # UI LAYOUT
    # ---------------------------------------------------------
    def build_layout(self):
        """
        Builds the two-panel layout:
        LEFT = Navigation menu
        RIGHT = Dynamic content panel
        """

        # Main container
        self.main_frame = tk.Frame(self, bg="#e8e8e8")
        self.main_frame.pack(fill="both", expand=True)

        # LEFT SIDEBAR
        self.sidebar = tk.Frame(self.main_frame, width=260, bg="#ffffff", relief="raised", bd=2)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="Main Menu",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff"
        ).pack(pady=20)

        # Buttons in sidebar
        self.build_sidebar_buttons()

        # RIGHT PANEL (dynamic)
        self.right_panel = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.right_panel.pack(side="left", fill="both", expand=True)

    def build_sidebar_buttons(self):
        btn_style = {"width": 22}  # ttk does NOT support font=

        ttk.Button(
            self.sidebar,
            text="Start New Conversation",
            command=self.start_new_conversation,
            **btn_style
        ).pack(pady=5)

        ttk.Button(
            self.sidebar,
            text="Open Existing Conversation",
            command=self.open_existing_conversation,
            **btn_style
        ).pack(pady=5)

        ttk.Button(
            self.sidebar,
            text="Delete Conversation",
            command=self.delete_conversation_prompt,
            **btn_style
        ).pack(pady=5)

        ttk.Button(
            self.sidebar,
            text="Switch Assistant",
            command=self.switch_assistant,
            **btn_style
        ).pack(pady=5)

        ttk.Button(
            self.sidebar,
            text="Customize Assistant",
            command=self.customize_assistant,
            **btn_style
        ).pack(pady=5)

        ttk.Button(
            self.sidebar,
            text="Show Recent Conversations",
            command=self.show_recent_conversations,
            **btn_style
        ).pack(pady=5)


    # ---------------------------------------------------------
    # RIGHT PANEL RENDERING
    # ---------------------------------------------------------
    def update_right_panel(self):
        """
        Clears and redraws the right panel depending on whether
        an assistant is selected.
        """

        for widget in self.right_panel.winfo_children():
            widget.destroy()

        if not self.active_assistant:
            self.render_setup_screen()
        else:
            self.render_assistant_screen()

    def render_setup_screen(self):
        """
        Right panel when NO assistant is selected.
        Shows a setup prompt.
        """

        tk.Label(
            self.right_panel,
            text="Choose Your AI Assistant",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f5f5"
        ).pack(pady=40)

        ttk.Button(
            self.right_panel,
            text="Select Assistant",
            command=self.switch_assistant,
            width=25
        ).pack(pady=10)

    def render_assistant_screen(self):
        """
        Right panel when an assistant IS selected.
        Shows placeholder image + assistant name + reset button.
        """

        tk.Label(
            self.right_panel,
            text=f"Active Assistant: {self.active_assistant}",
            font=("Segoe UI", 18, "bold"),
            bg="#f5f5f5"
        ).pack(pady=20)

        # Load placeholder image
        placeholder_path = os.path.join(
            BASE_DIR,
            "assets",
            "characters",
            self.active_assistant.capitalize()
,
            "placeholder.png"
        )

        try:
            img = Image.open(placeholder_path)
            img = img.resize((300, 450), Image.ANTIALIAS)
            self.placeholder_img = ImageTk.PhotoImage(img)

            tk.Label(
                self.right_panel,
                image=self.placeholder_img,
                bg="#f5f5f5"
            ).pack(pady=10)

        except Exception as e:
            tk.Label(
                self.right_panel,
                text=f"[Image failed to load]\n{e}",
                font=("Segoe UI", 12),
                bg="#f5f5f5",
                fg="red"
            ).pack(pady=20)

        ttk.Button(
            self.right_panel,
            text="Reset Assistant to Default",
            command=self.reset_assistant,
            width=25
        ).pack(pady=20)

    # ---------------------------------------------------------
    # BUTTON HANDLERS
    # ---------------------------------------------------------
    def start_new_conversation(self):
        if not self.active_assistant:
            messagebox.showwarning("No Assistant Selected", "Please Choose an Assistant first.")
            return 

        convo_id = self.manager.create_new_conversation()
        ChatWindow(convo_id, self.manager)    

    def open_existing_conversation(self):
        from tkinter import filedialog

        file_path = filedialog.askopenfilename(
            title="Open Conversation",
            initialdir=os.path.join(BASE_DIR, "conversations"),
            filetypes=[("JSON Files", "*.json")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            convo_id = data.get("conversation_id")
            if not convo_id:
                messagebox.showerror("Error", "Invalid conversation file.")
                return

            ChatWindow(convo_id, self.manager)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open conversation:\n{e}")

    def delete_conversation_prompt(self):
        conversations = self.manager.list_conversations()
        if not conversations:
            messagebox.showinfo("Delete Conversation", "No conversations to delete.")
            return

        latest = conversations[-1]
        confirm = messagebox.askyesno(
            "Delete Conversation",
            f"Delete the most recent conversation?\n\nPreview:\n{latest['preview'][:100]}"
        )

        if confirm:
            self.manager.delete_conversation(latest["conversation_id"])
            messagebox.showinfo("Delete Conversation", "Conversation deleted.")

    def switch_assistant(self):
        """
        Opens the assistant selection window.
        """

        def on_selected(name):
            self.active_assistant = name
            self.manager.set_active_assistant(name)
            self.save_user_settings()
            self.update_right_panel()

        AssistantSelectionWindow(self, self.manager, on_selected)

    def reset_assistant(self):
        """
        Clears the selected assistant and returns to setup screen.
        """
        self.active_assistant = None
        self.save_user_settings()
        self.update_right_panel()

    def customize_assistant(self):
        messagebox.showinfo("Customize Assistant", "Customization UI not implemented yet.")

    def show_recent_conversations(self):
        conversations = self.manager.list_conversations()
        if not conversations:
            messagebox.showinfo("Recent Conversations", "No conversations found.")
            return

        previews = "\n\n".join(
            f"- {c['id'][:8]}...: {c['preview'][:80]}"
            for c in conversations[-5:]
        )
        messagebox.showinfo("Recent Conversations", f"Last conversations:\n\n{previews}")


# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    os.chdir(BASE_DIR)
    app = MainMenu()
    app.mainloop()
