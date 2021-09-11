import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
from dependencies.db_manager import file_to_base64
from tkinter.filedialog import askopenfilename
from plyer import notification
from datetime import datetime
from threading import Thread
import tkinter.messagebox as messagebox
import tkinter as tk
import webbrowser
import time
import re


def open_github():
    webbrowser.open("https://github.com/LucioFex")


def open_twitter():
    webbrowser.open("https://twitter.com/LucioFex")


def check_birthday(birthday):
    """
    Function to check if today is someone's birthday.
    """
    birthday = birthday.split("/")[0:2]
    today = datetime.strftime(datetime.now(), "%d/%m").split("/")

    if int(birthday[0]) == int(today[0]) and int(birthday[1]) == int(today[1]):
        return True
    return False


def check_realistic_birth_date(date):
    """
    Function to check if the inserted date of birth is not futurist.
    """
    date = date.split("/")
    today = datetime.strftime(datetime.now(), "%d/%m/%Y").split("/")

    logic_1 = (
        int(date[0]) > int(today[0]) and  # Day
        int(date[1]) >= int(today[1]) and  # Month
        int(date[2]) >= int(today[2]))  # Year

    logic_2 = (
        int(date[0]) >= int(today[0]) and  # Day
        int(date[1]) > int(today[1]) and  # Month
        int(date[2]) >= int(today[2]))  # Year

    logic_3 = (
        int(date[0]) >= int(today[0]) and  # Day
        int(date[1]) >= int(today[1]) and  # Month
        int(date[2]) > int(today[2]))  # Year

    if logic_1 or logic_2 or logic_3:
        return False
    return True


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


def formatted_birth_date(date, formatted):
    """
    This function formats the given date to the selected format.
    """
    if formatted == "DD/MM/YYYY":  # Input Date: "YYYY-MM-DD"
        date = datetime.strptime(date, "%Y-%m-%d")
        date = [str(date.day), str(date.month), str(date.year)]
        return "/".join(date)

    elif formatted == "YYYY-MM-DD":  # Input Date: "DD/MM/YYYY"
        date = date.split("/")
        date = [date[2], date[1], date[0]]
        return "-".join(date)


def finder_row_content(master, texts, width, bg1, bg2, photo, skull, command):
    """
    Function to automate the finder label content generation.
    The "content" parameter must recieve a tuple or list of 4 elements.
    """
    row_person_img = tk.Button(
        master, activebackground=bg1, bd=0, bg=bg1,
        image=photo, cursor="hand2", command=command)
    row_person_img.grid(row=0, column=0, rowspan=2)

    array = ((0, 1), (1, 1), (0, 2), (1, 2))  # Grid
    for text, grid in zip(texts, array):
        row_person = tk.Label(
            master, bg=bg2, fg="#e3e3e3", width=round(width * .0085),
            font=("Century Gothic", round(width * 0.0087), "bold"), text=text)

        row_person.grid(row=grid[0], column=grid[1], padx=width * 0.0066)

    row_person_skull = tk.Label(master, bg=bg1, image=skull, bd=0)
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
        self.showed_people = {}  # VAR to show the rows on the people finder
        self.button_commands()
        self.generate_people_viewer(False)
        self.refresh_today_birthdays()

        self.yscrollbar.bind("<Button-1>", self.scrollbar_at_bottom)

    def button_commands(self):
        """
        This method assigns commands to each button of the client.
        """
        # self.maximize_button.config(command=self.title_bar_maximize) Later...
        self.minimize_button.config(command=self.title_bar_minimize)
        self.close_button.config(command=self.turn_strayicon_on)
        self.license_icon.config(command=self.show_license)
        self.about_icon.config(command=self.open_about)
        self.github_icon.config(command=open_github)
        self.twitter_icon.config(command=open_twitter)
        self.nut_icon.config(command=self.open_settings)
        self.accept.config(command=self.people_adder_accept)
        self.img_adder.config(command=self.people_adder_file_select)
        self.clear.config(command=self.clear_people_adder)
        self.browser.bind("<Return>", self.search_in_browser)

    def show_license(self):
        return messagebox.showinfo(
            "BirDayBer License",
            f"{self.get_license()[0]}\n{self.get_license()[1]}")

    def open_about(self):
        return messagebox.showinfo("About BirDayBer", self.get_version())

    def refresh_today_birthdays(self):
        """
        Method to update the "Birthday Counter" label.
        """
        self.people_found = self.browser_filter(False)
        self.check_all_birthdays()

        birthdays_count = len(self.total_birthdays)
        label_txt = f"Today is the birthday of {birthdays_count} people"
        return self.birthday_counter.config(text=label_txt)

    def check_all_birthdays(self):
        """
        Get the total number of birthdays and refreshes the total birthdays var
        """
        self.total_birthdays = []
        for person in self.people_found:
            date = formatted_birth_date(person[3], "DD/MM/YYYY")
            if check_birthday(date):
                self.total_birthdays.append(f"{person[1]} {person[2]}")

    def browser_filter(self, filter=True):
        """
        Method that filters people in the 'people_finder' section.
        """
        if not filter:
            return self.get_people()

        obtained_people = self.get_people()
        filtered_people = []

        for person in obtained_people:
            fullname = person[1] + " " + person[2]
            search = re.search(self.search.get(), fullname, re.IGNORECASE)
            if search is None:
                continue
            filtered_people.append(person)

        return filtered_people

    def search_in_browser(self, event):
        """
        Method to search for a person in people_finder through the browser.
        """
        self.reset_people_finder()
        self.generate_people_viewer()

    def generate_people_viewer(self, filters=True):
        """
        Method to refresh the people_finder depending on the browser's result.
        """
        self.people_found = self.browser_filter(filters)
        self.people_photos = []
        self.showed_people = {}

        # It shows the first 6 people
        for row, person in enumerate(self.people_found[0:6]):
            self.person_spawn(
                person[0], [person[1], person[2], person[3], person[5]],
                row, person[6], person[4])

    def show_more_people(self):
        """
        Method to load another 6 rows in the people_finder.
        """
        if len(self.showed_people) == len(self.people_found):
            return

        limit = len(self.showed_people) + 6
        for row, person in enumerate(self.people_found):
            if row < limit - 6:
                continue

            self.person_spawn(
                person[0], [person[1], person[2], person[3], person[5]],
                row, person[6], person[4])

            if row == limit:
                break

    def scrollbar_at_bottom(self, event):
        """
        Method to detect if the people_finder scrollbar is at the bottom.
        If it is, then It will load 6 people more.
        """
        if self.yscrollbar.get()[1] > 0.9:
            self.show_more_people()

    def add_row_peopleviewer(self):
        """
        Method to refresh the people_viewer (row's add).
        """
        person = self.get_last_person()
        row = len(self.showed_people) + 1

        grid = True
        if row < len(self.people_found):
            self.people_found.append(person)
            grid = False

        self.canvas.update_idletasks()
        self.person_spawn(
            person[0], [person[1], person[2], person[3], person[5]],
            row, person[6], person[4], grid=grid)

    def update_row_peopleviewer(self, person_id):
        """
        Method to refresh the people_viewer (row's update).
        """
        person = self.get_people(person_id)[0]
        row = self.showed_people[person_id].grid_info()["row"]

        self.canvas.update_idletasks()
        self.showed_people[person_id].destroy()

        self.person_spawn(
            person[0], [person[1], person[2], person[3], person[5]],
            row, person[6], person[4])

    def remove_row_peopleviewer(self, person_id):
        """
        Method to refresh the people_viewer (row's removal).
        """
        self.canvas.update_idletasks()
        self.showed_people[person_id].destroy()
        self.showed_people.pop(person_id)
        self.people_found = self.get_people()

    def person_spawn(
            self, person_id, texts, row, gender, photo=None, grid=True):
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
        texts[2] = formatted_birth_date(texts[2], "DD/MM/YYYY")
        preview_texts[2] = formatted_birth_date(preview_texts[2], "DD/MM/YYYY")

        bg_1, bg_2, bg_3 = "#79c1db", "#8fd0e7", "#6aaec6"

        birthday = False
        if check_birthday(texts[2]):
            birthday = True

        if birthday:
            bg_2 = "#99d99a"

        row_person_border = tk.Frame(self.people_finder, bg=bg_1)
        row_person = tk.Frame(row_person_border, bg=bg_2)

        data = [
            row_person, preview_texts, self.screen_width, bg_2, bg_3,
            new_photo, self.skull_src, lambda:
            self.big_person_generation(person_id, texts, gender, photo)]

        if birthday:
            data[6] = self.skull_party_src

        finder_row_content(*data)
        self.showed_people[person_id] = row_person_border
        if not grid:
            return

        row_person_border.grid(row=row, column=0)
        row_person.pack(pady=(0, self.screen_height * 0.006))

    def big_person_generation(self, person_id, texts, gender, photo=None):
        """
        Updates the big display of the selected person in the interface.
        """
        self.default_bg.pack_forget()
        self.right_mid_packing()

        if check_birthday(texts[2]):
            self.skull_icon.config(image=self.skull_party_src)
        elif not check_birthday(texts[2]):
            self.skull_icon.config(image=self.skull_src)

        self.current_id = person_id
        self.current_big_image = self.default_big_img

        photo = self.process_photo(photo, self.default_big_img, "big")
        self.big_photo.config(
            image=photo, command=lambda: self.update_row_photo(person_id))

        genders = {1: self.male_small_src, 2: self.female_small_src}
        gender = genders[gender]
        self.gender_small_icon.config(image=gender)

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
            filetypes=(("Images", ".jpg .jpeg .png .tiff"), ))

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
        if self.people_adder_check() is False:
            return

        name = self.add_name_var.get()
        surname = self.add_surname_var.get()
        birth = formatted_birth_date(self.add_birth_var.get(), "YYYY-MM-DD")
        country = self.add_country_var.get()
        gender = self.gender_selector.get()
        photo = self.file_selected

        self.add_person({
            "country": {"country": country},
            "gender": {"gender": gender},
            "photo": {"photo": photo},
            "birth": {"birth": birth},
            "person": {"per_first": name, "per_last": surname}})

        self.refresh_today_birthdays()
        self.add_row_peopleviewer()
        self.clear_people_adder()

    def people_adder_check(self):
        """
        Method that checks if the people adder's fields input are correct.
        If any of these are, then It will throw an error message.
        """
        if self.check_name_field():
            return False
        elif self.check_birthdate_field(self.add_birth_var):
            return False
        elif self.check_gender_field():
            return False

        self.remove_adder_placeholders()

    def check_name_field(self):
        if self.add_name_var.get() == "First Name":
            messagebox.showerror(
                "Field incomplete",
                "Filling in the First Name field is mandatory.")
            return True

    def check_gender_field(self):
        if self.gender_selector.get() == 0:
            messagebox.showerror(
                "Field incomplete",
                "Filling in the Gender field is mandatory.")
            return True

    def check_birthdate_field(self, date_of_birth):
        pattern = re.compile(r'([0-3]*[0-9])+/([0-1]*[0-9])+/(\d{4})+')
        match = pattern.findall(date_of_birth.get())

        if match == []:
            messagebox.showerror(
                "Field format problem",
                "There was a problem with the Date of Birth field." +
                '\nTry adding a date of birth with this format: "DD/MM/YYYY.')
            return True

        try:
            datetime.strptime(date_of_birth.get(), "%d/%m/%Y")
            if check_realistic_birth_date(date_of_birth.get()) is False:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Field data problem",
                "There was a problem with the input numbers of the Date of " +
                "Birth field. Check if the inserted digits are correct.")
            return True

    def remove_adder_placeholders(self):
        matches = (
            (self.add_surname_var, "Second Name"),
            (self.add_country_var, "Country"))

        for entry in matches:
            if re.match(entry[0].get(), entry[1]) is not None:
                entry[0].set("")

    def clear_people_adder(self):
        self.convert_adder_img("")  # Sets the default adder image
        self.gender_selector.set(0)
        self.file_selected = ""
        self.add_name_var.set("First Name")
        self.add_surname_var.set("Second Name")
        self.add_country_var.set("Country")
        self.add_birth_var.set("Date of Birth")

    def reset_people_finder(self):
        for person_id in self.people_found:
            try:
                self.remove_row_peopleviewer(person_id[0])
            except KeyError:  # To don't exceed the self.showed_people length
                break

    def remove_person(self, person_id):
        """
        This method removes a person from the DB.
        """
        if self.ask_before_delete() == "no":
            return

        self.remove_person_db(person_id)
        self.right_bg.pack_forget()

        self.right_mid_bg_packing()
        self.remove_row_peopleviewer(person_id)

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
        birth_date = formatted_birth_date(self.birth_var.get(), "YYYY-MM-DD")
        self.update_person_db(
            "birth", "birth", birth_date, f"id_birth = {person_id}")

    def update_row_photo(self, person_id):
        """
        Method that displays a preview of the new selected image
        and asks the user to save it.
        """
        old_photo = self.current_big_image
        photo = self.select_new_photo()

        new_photo = self.process_photo(photo[0], self.current_big_image, "big")
        self.big_photo.config(image=new_photo)

        if self.ask_before_update_photo(photo[1]) == "no":
            self.current_big_image = old_photo
            return self.big_photo.config(image=self.current_big_image)

        self.update_person_db(
            "photo", "photo", photo[0], f"id_photo = {person_id}")

        self.update_row_peopleviewer(person_id)

    def select_new_photo(self):
        filename = askopenfilename(
            initialdir="/", title="Select an image",
            filetypes=(("Images", ".jpg .jpeg .png .tiff"), ))

        photo = file_to_base64(filename)
        return (photo, filename)

    def ask_before_update_photo(self, filename):
        if filename == "":
            return "no"

        answer = messagebox.askquestion(
            "Update Photo", "Are you sure you want to save this photo?")
        return answer

    def update_person(self, person_id, section):
        """
        Method to update a row-person value, after changing
        the entry in the right-mid section.
        """
        if self.check_updated_mid_entries() is False:
            return

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
            self.update_right_mid_birth_data()
            self.switch_entry_state(
                person_id, self.birth_big,
                self.edit_birth, section, "disabled")

        self.update_row_peopleviewer(person_id)

    def update_right_mid_birth_data(self):
        birth_date = formatted_birth_date(self.birth_var.get(), "YYYY-MM-DD")
        self.age_var.set(current_age(birth_date))
        self.refresh_today_birthdays()

        if check_birthday(self.birth_var.get()):
            return self.skull_icon.config(image=self.skull_party_src)
        return self.skull_icon.config(image=self.skull_src)

    def check_updated_mid_entries(self):
        if self.check_updated_fullname():
            return False
        if self.check_birthdate_field(self.birth_var):
            return False

    def check_updated_fullname(self):
        """
        Method that checks if the Full Name field is correct,
        checking if it has more than 1 space or if it is empty.
        """
        error_detected = False
        spaces = 0

        for char in self.fullname_var.get():
            spaces += 1 if char == " " else 0
            if spaces == 2:
                error_detected = True
                break

        if self.fullname_var.get() in ("", " "):
            messagebox.showerror(
                "Field incomplete",
                "Filling in the Full Name field is mandatory.")
            return True

        elif error_detected:
            messagebox.showerror(
                "Problem detected",
                "You cannot add more than one space in the Full Name field.")
            return True

    def ask_before_delete(self):
        """
        Method to generate a messagebox asking to delete a person from the DB.
        """
        if self.ask_before_del_var.get() is False:
            return "yes"

        answer = messagebox.askquestion(
            "Delete", "Are you sure you want to delete this person?")
        return answer

    def prepare_birthday_notification(self):
        """
        Method to prepare the OS notifications about the Birthdays.
        """
        if self.stray_icon_state is False:
            return
        self.refresh_today_birthdays()

        if len(self.total_birthdays) == 1:
            self.notification = Thread(
                target=self.birthday_notify, args=[self.total_birthdays[0]])

        elif len(self.total_birthdays) > 1:
            self.notification = Thread(
                target=self.birthday_notify, args=[len(self.total_birthdays)])

        self.notification.daemon = True
        self.notification.start()

    def birthday_notify(self, data):
        """
        Function to notify the user of someone's birthday.
        """
        time.sleep(10800)  # 3 hours of time to show the notification
        if self.stray_icon_state is False:
            return

        message = {
            str: f"Today is {data}'s birthday!",
            int: f"Today is the birthday of {data} people!"}

        notification.notify(
            title="BirDayBer", message=message[type(data)], timeout=5,
            app_icon="bin//system-content//visual-content//BirDayBerIcon.ico")
