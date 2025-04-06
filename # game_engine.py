# game_engine.py

import tkinter as tk
from tkinter import messagebox
from save_system import save_game, load_game, delete_save

class HorrorAdventureGame(tk.Tk):
    def __init__(self, story_data):
        super().__init__()
        self.title("Shadows of the Hollow")
        self.geometry("620x420")

        self.story_data = story_data
        self.current_node = load_game()

        self.text_label = tk.Label(self, text="", wraplength=580, justify="left", font=("Helvetica", 12))
        self.text_label.pack(pady=20)

        self.choices_frame = tk.Frame(self)
        self.choices_frame.pack(pady=10)

        self.reset_button = tk.Button(self, text="New Game", command=self.reset_game)
        self.reset_button.pack(pady=5)

        self.show_node(self.current_node)

    def reset_game(self):
        delete_save()
        self.show_node("start")

    def show_node(self, node_key):
        node = self.story_data.get(node_key)
        if not node:
            messagebox.showerror("Error", f"Story node '{node_key}' not found.")
            return

        self.current_node = node_key
        save_game(self.current_node)
        self.text_label.config(text=node["text"])

        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        for choice_text, next_node in node.get("choices", []):
            button = tk.Button(
                self.choices_frame,
                text=choice_text,
                font=("Helvetica", 10, "bold"),
                command=lambda n=next_node: self.show_node(n),
                wraplength=500,
                width=50,
                anchor="w",
                padx=10
            )
            button.pack(pady=4)
