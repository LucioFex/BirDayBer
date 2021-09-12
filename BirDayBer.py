import dependencies.BirDayBer_interactivity as BirDayBer_interactivity
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
        self.db_path = db_connection

        # self.load_preview_configuration()
        self.lang = "English"  # Refactor later...

        with open("bin//languages.json", "r", encoding="utf-8") as texts:
            self.lang = json.load(texts)

        super().__init__()
        self.root.mainloop() if mainloop else None


if __name__ == '__main__':
    Birdayber(r"bin//BirDayBer.db", True)
