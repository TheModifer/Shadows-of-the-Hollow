import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import json
import os

SAVE_FILE = "savegame.json"
IMAGE_FILE = "image.png"

# Define the story structure
story = {
    "start": {
        "text": (
            "A middle-aged man awakens in a dark, eerie forest. His headache pounds like a war drum. "
            "Fear grips him. He stands, noticing shadows shift around him. A blood-curdling scream pierces the stillness. "
            "It’s chilling, almost human but twisted. Paranoia settles in his bones. To his left, a ruined building looms. "
            "To the right, a narrow forest path flickers with light."
        ),
        "choices": [
            ("Enter the ruined building", "ruin_building"),
            ("Follow the lighted path", "path_light")
        ]
    },
    "ruin_building": {
        "text": (
            "You push open the rusted door. Inside, shadows crawl. A dark mass floats nearby. "
            "It morphs into your reflection, then shifts to images of lost dreams. It lashes forward."
        ),
        "choices": [
            ("Face it", "consumed_by_entity"),
            ("Run back into the forest", "path_light")
        ]
    },
    "consumed_by_entity": {
        "text": (
            "The entity engulfs you. Smoke billows from your eyes. Your body falls limp as your soul is devoured."
        ),
        "choices": []
    },
    "path_light": {
        "text": (
            "You follow the flickering light. Whispers circle you. A cabin emerges ahead, its chimney spilling ghostly smoke."
        ),
        "choices": [
            ("Approach the cabin", "cabin_arrival"),
            ("Climb a tree to scout the area", "climb_tree")
        ]
    },
    "climb_tree": {
        "text": (
            "From above, you see the cabin and a clearing where a dark mass slithers. It knows you're watching."
        ),
        "choices": [
            ("Descend and approach the cabin", "cabin_arrival")
        ]
    },
    "cabin_arrival": {
        "text": (
            "The door creaks open as you approach. Inside, the air is thick with memories. A ghostly woman stirs the air. "
            "You recognize her: your mother. On the table, a letter lies next to a photo of your sister in a distant town."
        ),
        "choices": [
            ("Read the letter and accept the past", "acceptance_approach")
        ]
    },
    "acceptance_approach": {
        "text": (
            "As you read, guilt fades. Your father's voice echoes with sorrow, not anger. The entity looms again. "
            "You stand firm. Smoke rises as you breathe deep and accept."
        ),
        "choices": [
            ("Stand your ground", "final_acceptance")
        ]
    },
    "final_acceptance": {
        "text": (
            "The final clash is impending. The dark mass surges forward, ready to consume him. He stands firm. "
            "He feels the struggle of acceptance. As they collide, the forest shudders; a cacophony of screams and silence envelops him. "
            "Light bursts through the trees. He wakes up in his small room, breathless. Memories intact. Whole again."
        ),
        "choices": []
    }
}

# Save/Load functions
def save_game(state, filename=SAVE_FILE):
    with open(filename, 'w') as f:
        json.dump({"current_node": state}, f)

def load_game(filename=SAVE_FILE):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get("current_node", "start")
    return "start"

def delete_save(filename=SAVE_FILE):
    if os.path.exists(filename):
        os.remove(filename)

class TitleScreen(tk.Frame):
    def __init__(self, master, start_callback, load_callback):
        super().__init__(master, bg="#1e1e1e")
        self.start_callback = start_callback
        self.load_callback = load_callback

        try:
            image = Image.open(IMAGE_FILE)
            image = image.resize((760, 420), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
        except Exception as e:
            self.bg_image = None
            print(f"Image load failed: {e}")

        self.pack(fill="both", expand=True)

        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image, bg="#1e1e1e")
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = tk.Label(
            self,
            text="Shadows of the Hollow",
            font=("Georgia", 32, "bold"),
            fg="#eaeaea",
            bg="#000000",
            padx=20,
            pady=10
        )
        self.title_label.place(relx=0.5, rely=0.1, anchor="n")

        self.button_frame = tk.Frame(self, bg="#000000")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(
            self.button_frame,
            text="New Game",
            command=self.start_callback,
            bg="#3a3a3a",
            fg="white",
            font=("Georgia", 14),
            width=20,
            pady=5
        ).pack(pady=10)

        tk.Button(
            self.button_frame,
            text="Load Game",
            command=self.load_callback,
            bg="#3a3a3a",
            fg="white",
            font=("Georgia", 14),
            width=20,
            pady=5
        ).pack(pady=10)

class HorrorAdventureGame(tk.Tk):
    def __init__(self, story_data):
        super().__init__()
        self.title("Shadows of the Hollow")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e")
        self.story_data = story_data

        self.title_screen = TitleScreen(self, self.start_game, self.load_game_dialog)

    def start_game(self):
        self.title_screen.destroy()
        self.current_node = "start"
        self.init_game_screen()

    def init_game_screen(self):
        self.text_label = tk.Label(
            self,
            text="",
            wraplength=760,
            justify="left",
            font=("Georgia", 14),
            fg="#f0e6d2",
            bg="#1e1e1e"
        )
        self.text_label.pack(pady=30, padx=20)

        self.choices_frame = tk.Frame(self, bg="#1e1e1e")
        self.choices_frame.pack(pady=10)

        self.button_frame = tk.Frame(self, bg="#1e1e1e")
        self.button_frame.pack(pady=10)

        tk.Button(
            self.button_frame,
            text="New Game",
            command=self.reset_game,
            bg="#3a3a3a",
            fg="white",
            font=("Georgia", 12),
            relief="raised",
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            self.button_frame,
            text="Save Game",
            command=self.save_game_dialog,
            bg="#3a3a3a",
            fg="white",
            font=("Georgia", 12),
            relief="raised",
            padx=10,
            pady=5
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            self.button_frame,
            text="Load Game",
            command=self.load_game_dialog,
            bg="#3a3a3a",
            fg="white",
            font=("Georgia", 12),
            relief="raised",
            padx=10,
            pady=5
        ).grid(row=0, column=2, padx=10)

        self.show_node(self.current_node)

    def reset_game(self):
        delete_save()
        self.current_node = "start"
        self.show_node(self.current_node)

    def save_game_dialog(self):
        filename = filedialog.asksaveasfilename(
            title="Save Game",
            defaultextension=".json",
            filetypes=[("Save Files", "*.json")]
        )
        if filename:
            try:
                save_game(self.current_node, filename)
                messagebox.showinfo("Game Saved", f"Game saved successfully as:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def load_game_dialog(self):
        filename = filedialog.askopenfilename(
            title="Load Game",
            filetypes=[("Save Files", "*.json")]
        )
        if filename:
            try:
                self.current_node = load_game(filename)
                if hasattr(self, 'text_label'):
                    self.show_node(self.current_node)
                else:
                    self.title_screen.destroy()
                    self.init_game_screen()
                messagebox.showinfo("Game Loaded", f"Game loaded from:\n{filename}")
            except Exception as e:
                messagebox.showerror("Load Error", str(e))

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
                font=("Georgia", 12, "bold"),
                bg="#2e2e2e",
                fg="#eaeaea",
                command=lambda n=next_node: self.show_node(n),
                wraplength=700,
                width=60,
                anchor="w",
                padx=10,
                pady=5
            )
            button.pack(pady=5)

if __name__ == "__main__":
    app = HorrorAdventureGame(story)
    app.mainloop()