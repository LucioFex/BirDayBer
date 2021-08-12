import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
import tkinter.messagebox as messagebox
from datetime import datetime
import tkinter as tk
import webbrowser


def current_age(birth_date):
    """
    Input example: 'YYYY-MM-DD' (str).
    Output: Age (int).
    """
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")

    age = today.year - birth_date.year - 1
    if (today.month, today.day) >= (birth_date.month, birth_date.day):
        age += 1

    return age


def formatted_birth_date(date, full=True):
    """
    This function returns a formatted version of the given date.
    The input must be in the following format: 'YYYY-MM-DD' (str),
    and the output will be in 'DD/MM/YYYY (str).

    The 'full' parameter specifies if the output will include the year or not.
    """
    date = datetime.strptime(date, "%Y-%m-%d")
    date = [str(date.day), str(date.month), str(date.year)]

    date.pop() if not full else None
    return "/".join(date)


def finder_row_content(master, texts, width, photo, skull, command):
    """
    Function to automate the finder label content generation.
    The "content" parameter must recieve a tuple or list of 4 elements.
    """
    row_person_img = tk.Button(
        master, activebackground="#8fd0e7", bd=0, bg="#8fd0e7",
        image=photo, cursor="hand2", command=command)
    row_person_img.grid(row=0, column=0, rowspan=2)

    array = ((0, 1), (1, 1), (0, 2), (1, 2))  # Grid
    for text, grid in zip(texts, array):
        row_person = tk.Label(
            master, bg="#6aaec6", fg="#e3e3e3", width=round(width * .0085),
            font=("Century Gothic", round(width * 0.0087), "bold"), text=text)

        row_person.grid(row=grid[0], column=grid[1], padx=width * 0.0066)

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
        self.refresh_people_viewer()
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

    def browser_filter(self, search=""):  # Unfinished
        """
        Method that filters people in the 'people_finder' section.
        """
        return self.get_people()

    def refresh_people_viewer(self):
        """
        Method to refresh the people_finder depending on the browser's result.
        """
        self.people_found = self.browser_filter()
        self.people_photos = []

        for row, person in enumerate(self.people_found):
            self.row_person_spawn(
                person[0], [person[1], person[2], person[3], person[5]],
                row, person[4])

    def row_person_spawn(self, person_id, texts, row, photo=None):
        """
        Method that renders one person row in the 'people finder section'.
        """
        new_photo = self.process_photo(photo, self.person_default_src, "row")

        for index in range(len(texts)):  # Data characters visual limit
            if len(texts[index]) > 12:
                texts[index] = texts[index][0:12] + "..."

        # Add of the Age data
        texts.append(current_age(texts[2]))
        # Add of the Birthday data
        texts.append(formatted_birth_date(texts[2], False))
        # YYYY-MM-DD -> DD/MM/YYYY
        texts[2] = formatted_birth_date(texts[2])

        self.row_person_border = tk.Frame(self.people_finder, bg="#79c1db")
        self.row_person = tk.Frame(self.row_person_border, bg="#8fd0e7")

        finder_row_content(
            self.row_person, texts, self.screen_width,
            new_photo, self.skull_src,
            lambda: self.big_person_spawn(person_id, texts, photo))

        self.row_person_border.grid(row=row, column=0)
        self.row_person.pack(pady=(0, self.screen_height * 0.006))

    def big_person_spawn(self, person_id, texts, photo=None):
        self.current_id = person_id

        photo = self.process_photo(photo, self.default_big_img, "big")
        self.big_photo.config(image=photo)

        self.fullname_var.set(f"{texts[0]} {texts[1]}")
        self.birth_var.set(texts[2])
        self.country_var.set(texts[3])
        self.age_var.set(texts[4])
        self.birthday_var.set(texts[5])
