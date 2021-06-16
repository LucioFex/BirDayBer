import dependencies.BirDayBer_interactivity as BirDayBer_interactivity


class Birdayber(BirDayBer_interactivity.BirDayBer_interactivity):
    """
    This class is prepared to generate all the visual
    aspect and functionality of the main window (GUI).
    """
    def __init__(self, db_connection, mainloop=False):
        """
        If the 'mainloop' parameter is 'True' the program will main-loop.
        """
        super().__init__(db_connection)
        self.root.mainloop() if mainloop else None


if __name__ == '__main__':
    Birdayber("bin//BirDayBer.db", True)
