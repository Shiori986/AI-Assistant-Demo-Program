import tkinter as tk
from tkinter import ttk, colorchooser, filedialog

class ChatWindow(tk.Toplevel):
    def __init__(self, convo_id, manager):
        super().__init__()

        self.title("Chat Window")
        self.geometry("1200x750")
        self.configure(bg="#f5f5f5")

        # Conversation ID
        self.convo_id = convo_id

        # Use the SAME ConversationManager passed from MainMenu
        self.manager = manager

        # User text color
        self.user_text_color = "#000000"

        # Light/Dark mode
        self.dark_mode = False

        # Sidebar visibility
        self.sidebar_visible = True

        # Build UI
        self.build_layout()

        # Load messages
        self.load_messages()

        # Keyboard shortcut for sidebar
        self.bind("<Control-l>", lambda e: self.toggle_sidebar())


    # ---------------------------------------------------------
    # BUILD LAYOUT
    # ---------------------------------------------------------
    def build_layout(self):

        # ---------------- LEFT SIDEBAR ----------------
        self.sidebar = tk.Frame(self, width=380, bg="#ffffff")
        self.sidebar.pack(side="left", fill="y")

        assistant = self.manager.active_assistant
        assistant_name = assistant.capitalize() if assistant else "Assistant"


        tk.Label(
            self.sidebar,
            text=f"{assistant_name} Controls",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff"
        ).pack(pady=10)

        # Conversation list container
        self.sidebar_convo_frame = tk.Frame(self.sidebar, bg="#ffffff")
        self.sidebar_convo_frame.pack(fill="both", expand=True)

        # Build conversation list
        self.build_conversation_list()

        # Roam toggle
        self.roam_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.sidebar,
            text="Roam Mode",
            variable=self.roam_var
        ).pack(anchor="w", padx=20, pady=5)

        # Text color selector
        ttk.Button(
            self.sidebar,
            text="Choose Text Color",
            command=self.choose_text_color
        ).pack(anchor="w", padx=20, pady=5)

        # Light/Dark mode toggle
        ttk.Button(
            self.sidebar,
            text="Toggle Light/Dark Mode",
            command=self.toggle_theme
        ).pack(anchor="w", padx=20, pady=5)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=10)

        tk.Label(
            self.sidebar,
            text="Conversations",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        # ---------------- MAIN CHAT AREA ----------------
        self.chat_area = tk.Frame(self, bg="#f5f5f5")
        self.chat_area.pack(side="left", fill="both", expand=True)

        self.chat_container = tk.Frame(self.chat_area, bg="#f5f5f5")
        self.chat_container.pack(fill="both", expand=True, padx=80, pady=40)

        self.chat_display = tk.Text(
            self.chat_container,
            wrap="word",
            state="disabled",
            bg="#ffffff",
            font=("Segoe UI", 12),
            padx=15,
            pady=15,
            relief="flat"
        )
        self.chat_display.pack(fill="both", expand=True)

        # ---------------- INPUT BAR ----------------
        self.input_bar = tk.Frame(self.chat_area, bg="#e8e8e8", height=90)
        self.input_bar.pack(fill="x", side="bottom", pady=15, padx=80)
        self.input_bar.configure(relief="raised", bd=2)

        self.mode_var = tk.StringVar(value="Quick")
        self.mode_dropdown = ttk.Combobox(
            self.input_bar,
            textvariable=self.mode_var,
            values=["Quick", "Research", "Study", "Professional Roleplay", "Creative Roleplay"],
            width=22
        )
        self.mode_dropdown.place(x=10, y=10)

        self.input_box = tk.Entry(self.input_bar, width=70, font=("Segoe UI", 12))
        self.input_box.place(x=10, y=50)
        self.input_box.bind("<Return>", self.send_message)

        self.upload_btn = tk.Button(
            self.input_bar,
            text="Upload",
            width=10,
            relief="raised",
            bd=3,
            command=self.upload_file
        )
        self.upload_btn.place(x=650, y=45)

        self.send_button = tk.Button(
            self.input_bar,
            text="✈",
            font=("Segoe UI", 14),
            width=4,
            relief="raised",
            bd=3,
            command=self.send_message
        )
        self.send_button.place(x=750, y=42)


    # ---------------------------------------------------------
    # SIDEBAR TOGGLE
    # ---------------------------------------------------------
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_visible = True


    # ---------------------------------------------------------
    # THEME TOGGLE
    # ---------------------------------------------------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.configure(bg="#1e1e1e")
            self.chat_area.configure(bg="#1e1e1e")
            self.chat_container.configure(bg="#1e1e1e")
            self.chat_display.configure(bg="#2d2d2d", fg="#ffffff")
            self.input_bar.configure(bg="#3a3a3a")
        else:
            self.configure(bg="#f5f5f5")
            self.chat_area.configure(bg="#f5f5f5")
            self.chat_container.configure(bg="#f5f5f5")
            self.chat_display.configure(bg="#ffffff", fg="#000000")
            self.input_bar.configure(bg="#e8e8e8")


    # ---------------------------------------------------------
    # COLOR PICKER
    # ---------------------------------------------------------
    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[1]:
            self.user_text_color = color[1]


    # ---------------------------------------------------------
    # FILE UPLOAD
    # ---------------------------------------------------------
    def upload_file(self):
        filedialog.askopenfilename(title="Select a file")


    # ---------------------------------------------------------
    # CONVERSATION LIST
    # ---------------------------------------------------------
    def build_conversation_list(self):
        for widget in self.sidebar_convo_frame.winfo_children():
            widget.destroy()

        conversations = self.manager.list_conversations()

        for convo in conversations:
            row = tk.Frame(self.sidebar_convo_frame, bg="#ffffff")
            row.pack(fill="x", padx=15, pady=3)

            btn = ttk.Button(
                row,
                text=convo["preview"][:25] + "...",
                command=lambda cid=convo["conversation_id"]: self.switch_conversation(cid)
            )

            btn.pack(side="left", fill="x", expand=True)

            del_btn = tk.Button(
                row,
                text="🗑️",
                bg="#ffffff",
                relief="flat",
                command=lambda cid=convo["conversation_id"]: self.delete_conversation(cid)

            )
            del_btn.pack(side="right", padx=5)


    # ---------------------------------------------------------
    # SWITCH CONVERSATION
    # ---------------------------------------------------------
    def switch_conversation(self, convo_id):
        self.convo_id = convo_id
        self.load_messages()


    # ---------------------------------------------------------
    # DELETE CONVERSATION
    # ---------------------------------------------------------
    def delete_conversation(self, convo_id):
        self.manager.delete_conversation(convo_id)

        conversations = self.manager.list_conversations()
        if conversations:
            self.convo_id = conversations[0]["conversation_id"]
        else:
            self.convo_id = self.manager.create_new_conversation()


        self.build_conversation_list()
        self.load_messages()


    # ---------------------------------------------------------
    # LOAD MESSAGES
    # ---------------------------------------------------------
    def load_messages(self):
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)

        convo = self.manager.load_conversation(self.convo_id)

        for msg in convo["messages"]:
            sender = msg["sender"]
            text = msg["text"]
            self.chat_display.insert(tk.END, f"{sender}: {text}\n\n")

        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)
    


    # ---------------------------------------------------------
    # SEND MESSAGE
    # ---------------------------------------------------------
    def send_message(self, event=None):
        text = self.input_box.get().strip()
        if not text:
            return

        # Save user message
        self.manager.save_message(self.convo_id, "You", text)

        # Display user message
        self.chat_display.config(state="normal")
        self.chat_display.insert(
            tk.END,
            f"You: {text}\n\n",
            ("user_color",)
        )
        self.chat_display.tag_config("user_color", foreground=self.user_text_color)
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

        self.input_box.delete(0, tk.END)

        # 🔹 Get AI response from the manager
        response = self.manager.get_ai_response(text)

        # 🔹 Safely determine assistant name
        assistant = self.manager.active_assistant
        assistant_name = assistant.capitalize() if assistant else "Assistant"

        # Save AI message
        self.manager.save_message(self.convo_id, assistant_name, response)

        # Display AI message with correct name
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{assistant_name}: {response}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

        # Refresh conversation list
        self.build_conversation_list()
