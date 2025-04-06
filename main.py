# main.py

from game_engine import HorrorAdventureGame
from story_data import story # type: ignore

if __name__ == "__main__":
    app = HorrorAdventureGame(story)
    app.mainloop()