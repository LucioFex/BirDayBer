import dependencies.BirDayBer_interactivity as BirDayBer_interactivity
import tkinter as tk
import json


class Birdayber(BirDayBer_interactivity.BirDayBer_interactivity):
    """
    This class is prepared to generate all the visual
    aspect and functionality of the main window (GUI).
    """
    def __init__(self, db_connection, mainloop=False):
        """
        If the 'mainloop' parameter is 'True' the program will main-loop.
        """
        # Load of the connection with the database and root generation
        self.db_path = db_connection
        self.root = tk.Tk()

        self.load_previews_configurations()
        with open("bin//languages.json", "r", encoding="utf-8") as texts:
            self.lang = json.load(texts)[self.current_lang]

        super().__init__()
        self.root.mainloop() if mainloop else None

    def load_previews_configurations(self):
        """
        Method to load the previews configurations made in the settings widget
        """
        with open("bin//config.json", "r", encoding="utf-8") as json_file:
            config = json.load(json_file)

            self.sound_var = tk.BooleanVar(value=config["sound"])
            self.ask_before_del_var = tk.BooleanVar(value=config["row_delete"])
            self.current_lang = config["language"]

    def update_new_configurations(self):
        """
        Method to update the new configurations made in the settings widget
        """
        with open("bin//config.json", "r", encoding="utf-8") as json_file:
            config = json.load(json_file)

        config["sound"] = self.sound_var.get()
        config["row_delete"] = self.ask_before_del_var.get()
        config["language"] = self.current_lang

        with open("bin//config.json", "w", encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)


if __name__ == '__main__':
    Birdayber(r"bin//BirDayBer.db", True)
