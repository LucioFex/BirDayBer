import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
from dependencies.db_manager import file_to_base64
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
import tkinter as tk
from datetime import datetime
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


def formatted_birth_date(date):
    """
    This function returns a formatted version of the given date.
    The input must be in the following format: 'YYYY-MM-DD' (str),
    and the output will be in 'DD/MM/YYYY (str).

    The 'full' parameter specifies if the output will include the year or not.
    """
    date = datetime.strptime(date, "%Y-%m-%d")
    date = [str(date.day), str(date.month), str(date.year)]

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
        self.showed_people = []  # VAR to show the rows on the people finder
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
        self.accept.config(command=self.people_adder_accept)
        self.img_adder.config(command=self.people_adder_file_select)
        self.clear.config(command=self.clear_people_adder)

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
        self.reset_showed_people()

        for row, person in enumerate(self.people_found):
            self.person_spawn(
                person[0], [person[1], person[2], person[3], person[5]],
                row, person[4])

    def reset_showed_people(self):
        if len(self.showed_people) > 0:
            self.reset_people_finder()
            self.showed_people = []

    def person_spawn(self, person_id, texts, row, photo=None):
        """
        Method that renders one person row in the 'people finder section'.
        """
        new_photo = self.process_photo(photo, self.person_default_src, "row")
        preview_texts = [*texts]

        for index in range(len(preview_texts)):  # Data characters visual limit
            if len(preview_texts[index]) > 12:
                preview_texts[index] = preview_texts[index][0:12] + "..."

        # Add of the Age data
        texts.append(current_age(texts[2]))
        # YYYY-MM-DD -> DD/MM/YYYY
        texts[2] = formatted_birth_date(texts[2])

        row_person_border = tk.Frame(self.people_finder, bg="#79c1db")
        row_person = tk.Frame(row_person_border, bg="#8fd0e7")

        finder_row_content(
            row_person, preview_texts, self.screen_width,
            new_photo, self.skull_src,
            lambda: self.big_person_generation(person_id, texts, photo))

        row_person_border.grid(row=row, column=0)
        row_person.pack(pady=(0, self.screen_height * 0.006))
        self.showed_people.append(row_person_border)

    def big_person_generation(self, person_id, texts, photo=None):
        """
        Updates the big display of the selected person in the interface.
        """
        self.default_bg.pack_forget()
        self.right_mid_packing()

        self.current_id = person_id

        photo = self.process_photo(photo, self.default_big_img, "big")
        self.big_photo.config(image=photo)

        self.fullname_var.set(f"{texts[0]} {texts[1]}")
        self.country_var.set(texts[3])
        self.age_var.set(texts[4])
        self.birth_var.set(texts[2])

        self.trash.config(command=lambda: self.remove_person(person_id))

        self.switch_entry_state(
            person_id, self.fullname_big,
            self.edit_fullname, "fullname", "disabled")
        self.switch_entry_state(
            person_id, self.country_big,
            self.edit_country, "country", "disabled")
        self.switch_entry_state(
            person_id, self.birth_big,
            self.edit_birth, "birth", "disabled")

    def people_adder_file_select(self):
        filename = askopenfilename(
            initialdir="/", title="Select an image",
            filetypes=(("Images", ".jpg .jpeg .png .tiff .jif"), ))

        self.file_selected = filename
        self.convert_adder_img(filename)

    def convert_adder_img(self, filename):
        if filename == "":
            filename = "bin//system-content//visual-content//user-black-1.png"

        photo = file_to_base64(filename)
        photo = self.process_photo(photo, self.person_default_src, "adder")
        self.img_adder.config(image=photo)

    def people_adder_accept(self):
        """
        Method that adds people to the DataBase
        """
        # self.people_adder_check(field)  # Regular Expressions
        name = self.adder_name_var.get()
        surname = self.adder_surname_var.get()
        country = self.adder_country_var.get()
        birth = self.adder_birth_var.get()
        photo = self.file_selected

        self.add_person({
            "country": {"country": country},
            "gender": {"gender": "Male"},
            "photo": {"photo": photo},
            "birth": {"birth": birth},
            "person": {"per_first": name, "per_last": surname}})

        self.refresh_people_viewer()
        self.clear_people_adder()

    def people_adder_check(self, field):
        """
        Method that checks if the people adder's field input is correct
        """
        pass

    def clear_people_adder(self):
        self.convert_adder_img("")  # Sets the default adder image
        self.gender_selector.set(0)
        self.file_selected = ""
        self.adder_name_var.set("")
        self.adder_surname_var.set("")
        self.adder_country_var.set("")
        self.adder_birth_var.set("")

    def remove_person(self, person_id):
        self.remove_person_db(person_id)
        self.right_bg.pack_forget()

        self.right_mid_bg_packing()
        self.refresh_people_viewer()

    def switch_entry_state(self, person_id, entry, button, section, state):
        """
        Method to prepare or unprepare the selected entry to be updated.
        """
        if state == "disabled":
            entry.config(state=state, cursor="arrow")
            entry.unbind("<Return>")
            return button.config(
                image=self.edit_src, command=lambda: self.switch_entry_state(
                    person_id, entry, button, section, "normal"))

        entry.config(state=state, cursor="xterm")
        entry.focus(), entry.icursor(50)

        entry.bind(
            "<Return>", lambda x: self.update_person(person_id, section))
        return button.config(
            image=self.update_src, command=lambda:
            self.update_person(person_id, section))

    def update_person_fullname_query(self, person_id):
        fullname = self.fullname_var.get().split(" ")
        fullname.append("") if len(fullname) == 1 else None
        name, surname = fullname

        self.update_person_db(
            "person", "per_first", name, f"id_person = {person_id}")
        self.update_person_db(
            "person", "per_last", surname, f"id_person = {person_id}")

    def update_person_country_query(self, person_id):
        self.update_person_db(
            "country", "country", self.country_var.get(),
            f"id_country = {person_id}")

    def update_person_birth_query(self, person_id):
        self.update_person_db(
            "birth", "birth", self.birth_var.get(), f"id_birth = {person_id}")

    def update_person(self, person_id, section):
        """
        Method to update a row-person value, after changing
        the entry in the right-mid section.
        """
        # self.check_entry_regex(section)  # Regular expressions
        if section == "fullname":
            self.update_person_fullname_query(person_id)
            self.switch_entry_state(
                person_id, self.fullname_big,
                self.edit_fullname, section, "disabled")

        elif section == "country":
            self.update_person_country_query(person_id)
            self.switch_entry_state(
                person_id, self.country_big,
                self.edit_country, section, "disabled")

        elif section == "birth":
            self.update_person_birth_query(person_id)
            self.switch_entry_state(
                person_id, self.birth_big,
                self.edit_birth, section, "disabled")

        self.refresh_people_viewer()
