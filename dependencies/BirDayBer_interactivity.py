import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
import tkinter as tk


class BirDayBer_interactivity(BirDayber_structure.Interface_structure):
    """
    Class that manages the interactivity of the BirDayBer's client.
    """
    def __init__(self, db_connection):
        """
        It assign all events to buttons and it loads all
        people from the database in the 'people_viewer' method.
        """
        super().__init__(db_connection)
