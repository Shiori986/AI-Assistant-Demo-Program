import json
import tkinter as tk
from tkinter import messagebox


class AssistantSelectionWindow(tk.Toplevel):
    """
    Updated Assistant Selection Window
    - Now uses Toplevel (popup)
    - Accepts a callback so the main menu can update itself
    - Does NOT save settings directly (main menu handles that)
    """

    def __init__(self, parent, manager, on_confirm_callback):
        super().__init__(parent)

        self.title("Choose Your Assistant")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")

        self.manager = manager
        self.on_confirm_callback = on_confirm_callback
        self.selected_assistant = None

        # Load assistant definitions
        self.assistants = self.load_assistant_definitions()

        # Title
        title = tk.Label(
            self,
            text="Choose Your Assistant",
            font=("Segoe UI", 18, "bold"),
            bg="#f0f0f0"
        )
        title.pack(pady=20)

        # Frame for assistant list
        self.list_frame = tk.Frame(self, bg="#f0f0f0")
        self.list_frame.pack(pady=10, fill="both", expand=True)

        # Build assistant buttons
        self.build_assistant_buttons()

        # Confirm button
        self.confirm_button = tk.Button(
            self,
            text="Confirm Selection",
            font=("Segoe UI", 12),
            state="disabled",
            command=self.confirm_selection
        )
        self.confirm_button.pack(pady=20)

    def load_assistant_definitions(self):
        try:
            with open("assistants.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load assistants.json:\n{e}")
            return {}

    def build_assistant_buttons(self):
        for name, data in self.assistants.items():
            available = data.get("available", False)
            description = data.get("description", "No description provided.")

            # Button frame
            frame = tk.Frame(self.list_frame, bg="#ffffff", bd=2, relief="groove")
            frame.pack(fill="x", pady=5, padx=20)

            # Assistant name
            label = tk.Label(
                frame,
                text=name,
                font=("Segoe UI", 14, "bold"),
                bg="#ffffff"
            )
            label.pack(anchor="w", padx=10, pady=2)

            # Description
            desc = tk.Label(
                frame,
                text=description,
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg="#555555",
                justify="left"
            )
            desc.pack(anchor="w", padx=10)

            # Select button
            if available:
                btn = tk.Button(
                    frame,
                    text="Select",
                    command=lambda n=name: self.select_assistant(n)
                )
            else:
                btn = tk.Button(
                    frame,
                    text="Coming Soon",
                    state="disabled"
                )

            btn.pack(anchor="e", padx=10, pady=5)

    def select_assistant(self, name):
        self.selected_assistant = name
        self.confirm_button.config(state="normal")
        messagebox.showinfo("Assistant Selected", f"You selected {name}.")

    def confirm_selection(self):
        if not self.selected_assistant:
            messagebox.showwarning("No Selection", "Please choose an assistant first.")
            return

        # Notify main menu
        self.on_confirm_callback(self.selected_assistant)

        # Close window
        self.destroy()
