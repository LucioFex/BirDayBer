import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
import tkinter.messagebox as messagebox
import tkinter as tk
import webbrowser


def finder_row_content(master, texts, width, img, skull, command=None):
    """
    Function to automate the finder label content generation.
    The "content" parameter must recieve a tuple or list of 4 elements.
    """
    row_person_img = tk.Button(
        master, activebackground="#8fd0e7", bd=0,
        bg="#8fd0e7", image=img, cursor="hand2")
    row_person_img.grid(row=0, column=0, rowspan=2)

    array = ((0, 1), (1, 1), (0, 2), (1, 2))  # Grid
    for text, grid in zip(texts, array):
        row_person = tk.Label(
            master, bg="#6aaec6", fg="#e3e3e3", width=round(width * .0085),
            font=("Century Gothic", round(width * 0.0082)), text=text)

        row_person.grid(row=grid[0], column=grid[1], padx=width * 0.007)

    row_person_skull = tk.Label(master, bg="#8fd0e7", image=skull, bd=0)
    row_person_skull.grid(row=0, column=3, rowspan=2)


class BirDayBer_interactivity(BirDayber_structure.Interface_structure):
    """
    Class that manages the interactivity of the BirDayBer's client.
    """
    def __init__(self):
        """
        It assign all events to buttons and it loads all
        people from the database in the 'people_viewer' method.
        """
        super().__init__()

        self.settings_state = False  # VAR to don't open more than one window
        self.button_commands()
        # self.refresh_people_viewer()
        # self.refresh_today_birthdays()

    def button_commands(self):
        """
        This method assigns commands to each button of the client.
        """
        self.minimize_button.config(command=self.title_bar_minimize)
        # self.maximize_button.config(command=self.title_bar_maximize) Later...
        self.close_button.config(command=self.close_client)
        self.license_icon.config(command=self.show_license)
        self.about_icon.config(command=self.open_about)
        self.github_icon.config(command=self.open_github)
        self.twitter_icon.config(command=self.open_twitter)
        self.nut_icon.config(command=self.open_settings)

    def show_license(self):
        return messagebox.showinfo(
            "BirDayBer License",
            f"{self.get_license()[0]}\n{self.get_license()[1]}")

    def open_about(self):
        return messagebox.showinfo("About BirDayBer", self.get_version())

    def open_github(self):
        self.github_icon.config(command=self.open_github)
        webbrowser.open("https://github.com/LucioFex")

    def open_twitter(self):
        self.twitter_icon.config(command=self.open_twitter)
        webbrowser.open("https://twitter.com/LucioFex")

    def refresh_people_viewer(self):
        pass

    def row_person_spawn(self, texts, photo, row):
        """
        Method that renders one person row in the 'people finder section'.
        """
        self.row_person_border = tk.Frame(self.people_finder, bg="#79c1db")
        self.row_person = tk.Frame(self.row_person_border, bg="#8fd0e7")

        finder_row_content(
            self.row_person, texts, self.screen_width, photo, self.skull_src)

        self.row_person_border.grid(row=row, column=0)
        self.row_person.pack(pady=(0, self.screen_height * 0.006))

        return self.row_person_border
