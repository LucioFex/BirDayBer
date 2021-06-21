import dependencies.BirDayBer_interfaceStructure as BirDayber_structure


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

        self.button_commands()
        # self.refresh_people_viewer()
        # self.refresh_today_birthdays()

    def button_commands(self):
        """
        This method assigns commands to each button of the client.
        """
        self.minimize_button.config(command=self.title_bar_minimize)
        # self.maximize_button.config(command=self.title_bar_maximize)
        self.close_button.config(command=self.close_client)
