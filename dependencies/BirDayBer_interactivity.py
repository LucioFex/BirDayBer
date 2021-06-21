import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
import tkinter.messagebox as messagebox


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

    def show_license(self):
        """
        This method shows BirDayBer's current license.
        """
        return messagebox.showinfo(
            "BirDayBer License", " " * 22 +
            f"{self.get_license()[0]}\n{self.get_license()[1]}")

    def button_commands(self):
        """
        This method assigns commands to each button of the client.
        """
        self.minimize_button.config(command=self.title_bar_minimize)
        # self.maximize_button.config(command=self.title_bar_maximize) Later...
        self.close_button.config(command=self.close_client)
        self.license_icon.config(command=self.show_license)
