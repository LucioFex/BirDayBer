import db_manager
import tkinter as tk
from PIL import Image
import os


def wrong_input_type(desired, acquired):
    """
    Function that raises a ValueError because of the data type given.
    """
    raise ValueError(
        "add_person method only expects as a parameter a " +
        "%s, but a %s was recieved." % (desired, acquired))


class Birdayber_database:
    """
    This class is specialized in the generation and maintenance
    of the DB and get data of the project's LICENSE.
    """
    def __init__(self, db_connection):
        """
        Method that only accepts a sqlite3 database lotaction and Boolean:
        Creation of the database and preparation to generate the interface.
        If the second parameter is 'True' the program will start main-looping.
        """
        #  Db management and generation:
        if os.path.exists(db_connection) is False:  # If there's not db
            self.generate_database(db_connection)
        self.db = db_manager.Db_manager(db_connection)  # If there's a db

    def get_license(self):
        """
        This method returns the type of BirDayBer project's license,
        the duration of this one and the name of its creator.
        """
        license_type = []
        with open("LICENSE", "r", encoding="utf-8") as license_data:
            license_type.append(license_data.readlines()[0][0:-1])
            license_data.seek(0)
            license_type.append(license_data.readlines()[2][0:-1])

        return tuple(license_type)

    def generate_database(self, db_connection):
        """
        Method that only accepts sqlite3 database locations:
        Generation of the database connection and tables.
        The generation of the tables is pre-created.
        """
        self.db = db_manager.Db_manager(db_connection)
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        self.db.create_table({
            "genders":
                f"""id_gender {id_type},
                gender VARCHAR(6) NOT NULL""",
            "photos":
                f"""id_photo {id_type},
                photo BLOB""",
            "countries":
                f"""id_country {id_type},
                country VARCHAR(40)""",
            "births":
                f"""id_birth {id_type},
                birth DATE NOT NULL,
                age INTEGER""",

            "people":
                f"""id_person {id_type},
                per_first VARCHAR(35) NOT NULL,
                per_last VARCHAR(35),
                id_country1_fk INTEGER NOT NULL,
                id_gender1_fk INTEGER NOT NULL,
                id_birth1_fk INTEGER NOT NULL,
                id_photo1_fk INTEGER NOT NULL,
                FOREIGN KEY (id_country1_fk) REFERENCES country (id_country),
                FOREIGN KEY (id_gender1_fk) REFERENCES gender (id_gender),
                FOREIGN KEY (id_birth1_fk) REFERENCES birth (id_birth),
                FOREIGN KEY (id_photo1_fk) REFERENCES photo (id_photo)"""})

        del id_type
        return db_connection

    def add_person(self, person):
        """
        Method that only accepts dicts:
        Addition of people to the database.
        Every key in the dictionary must be a String, like in the example.

        For example:
            self.add_person({
                "country": {"country": "United States"},
                "gender": {"gender": "Male"},
                "photo": {"photo": None},
                "birth": {"birth": "1919-12-23", "age": None},
                "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """
        if type(person) == dict:  # Data type detector
            for row in person.items():
                if type(row[0]) != str:
                    wrong_input_type(str, type(row))
                elif type(row[1]) != dict:
                    wrong_input_type(dict, type(row))

            return self.db.add_rows(person)  # If all the data type is fine
        return wrong_input_type(dict, type(row))

    def get_people(self, id_person="&None%", binary=True):
        """
        Method that only accepts Str or Int:
        This method brings all the information of the people.
        The parameter "id" is part of a WHERE clause. If there's no WHERE
        given or "&None%" recieved, then all the data will be displayed.
        """
        if id_person != "&None%":
            id_person = "id_person = %s" % id_person

        if binary:
            select = "per_first, per_last, birth, age, photo, country, gender"
        elif binary is False:
            select = "per_first, per_last, birth, age, country, gender"

        people_data = self.db.column_search(
            "people", select,
            """INNER JOIN
                births on births.id_birth = people.id_birth1_fk
            INNER JOIN
                photos on photos.id_photo = people.id_photo1_fk
            INNER JOIN
                countries on countries.id_country = people.id_country1_fk
            INNER JOIN
                genders on genders.id_gender = people.id_gender1_fk""",
            id_person)

        return people_data

    def drop_database(self):
        """
        This method deletes the database file.
        """
        self.db.close_database()
        self.db.drop_database()


class Birdayber_setUp(Birdayber_database):
    """
    This class is specialized in the generation of the GUI.
    """
    def __init__(self, db_connection):
        super().__init__(db_connection)

        # Root and Frame - Generation and Configuration:
        self.root = tk.Tk()

        #   Deletion of the original Title Bar
        self.root.overrideredirect(1)
        #   Sets the window screen resolution
        self.window_init_resolution(
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight())
        #   Generation of new responsive images
        self.responsive_imgs()
        #  Generation of the main frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH)

        # Hidden Window - Generation and Configuration:
        self.hidden_window = tk.Toplevel(self.root)

        #   Hide of the top window
        self.hidden_window.geometry("0x0+10000+10000")
        self.hidden_window.attributes("-alpha", 0.0)
        #   Actions for maximizing and minimizing the root from the taskbar
        self.hidden_window.bind("<Unmap>", self.window_focus)
        self.hidden_window.bind("<FocusIn>", self.window_focus)

        # Implementation of actions for when the window is closed
        for widget in (self.root, self.hidden_window):
            widget.protocol("WM_DELETE_WINDOW", self.close_client)

        # Visual brand modifications
        for visual_brand in (self.root, self.hidden_window):
            visual_brand.title("BirDayBer")
            visual_brand.iconbitmap(
                "bin//system_content//visual_content//BirDayBerIcon.ico")

    def window_init_resolution(self, width, height):
        """
        This method returns the information of the best
        possible resolution and position for the client's window.
        Then it sets the new values in the root.geometry() function.
        It also calls the 'responsive_imgs' method to resize the system imgs.
        """

        self.screen_width = width - round(width / 4)
        self.screen_height = height - round(height / 4)

        self.x_position = round(width / 7.5)
        self.y_position = round(height / 8)

        self.root.geometry("%sx%s+%s+%s" % (
            self.screen_width, self.screen_height,
            self.x_position, self.y_position))

        self.root.update()
        return str(self.root.geometry())

    def responsive_imgs(self):
        """
        Method that modifies all the sizes of images and clone these in the
        BirDayBer's system to something more visible for the user.
        The new clones will be saved in the 'responsive' folder.
        """
        location = "bin//system_content//visual_content"
        files = next(os.walk(location))[2]

        for img in files:  # (Refactor when you have all the imgs)
            # Title bar section
            if img in (
                "close-button.png", "minimize-button.png",
                    "maximize-button.png", "maximized-button.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 0.04),
                    round(self.screen_height * 0.04)))
                responsive_img.save("%s//responsive//%s" % (location, img))
            # Title bar section
            elif img in ("BirDayBerIcon.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 0.065),
                    round(self.screen_height * 0.065)))
                responsive_img.save("%s//responsive//%s" % (location, img))
            # Main entry section
            elif img in ("user_white.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 0.07),
                    round(self.screen_height * 0.09)))
                responsive_img.save("%s//responsive//%s" % (location, img))
            # Footer section
            elif img in ("license.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 0.056),
                    round(self.screen_height * 0.088)))
                responsive_img.save("%s//responsive//%s" % (location, img))
            # People adder's icon
            elif img in ("add_person.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 0.075),
                    round(self.screen_height * 0.087)))
                responsive_img.save("%s//responsive//%s" % (location, img))
            # People adder's section and extra buttons
            elif img in ("nut.png", "about.png", "male.png", "female.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 0.056),
                    round(self.screen_height * 0.069)))
                responsive_img.save("%s//responsive//%s" % (location, img))

    def title_bar_minimize(self):
        """
        This method is a manual way to minimize the window
        with the 'minimize' button of the title bar.
        """
        self.hidden_window.unbind("<FocusIn>")
        self.root.withdraw()
        self.root.update()
        self.hidden_window.bind("<FocusIn>", self.window_focus)

    def window_focus(self, event):
        """
        Method that declares if the program (recognized by the task manager)
        is focused or not. Then it will minimize or re-open the window.
        """
        self.root.update()
        if event.type == tk.EventType.FocusIn:
            self.root.deiconify()
        elif event.type == tk.EventType.Unmap:
            self.root.withdraw()

    def cursor_start_move(self, event): self.x, self.y = event.x, event.y

    def window_dragging(self, event):
        """
        Changes the position of the window without
        changing the mouse coordinates.

        This method works with the 'cursor_start_move' method.
        """
        cursor_position_x = event.x - self.x
        cursor_position_y = event.y - self.y

        window_position_x = self.root.winfo_x() + cursor_position_x
        window_position_y = self.root.winfo_y() + cursor_position_y

        self.root.geometry("+%s+%s" % (window_position_x, window_position_y))

    def close_client(self):
        """
        It makes the program close the database and stop mainlooping.
        """
        self.db.close_database()
        self.root.quit()


class Interface_structure(Birdayber_setUp):
    """
    This class generates the frames (background) and labels
    for the user interactivity with the GUI.
    """
    def __init__(self, db_connection):
        """
        Generation of the left and right side in the main body.
        """
        super().__init__(db_connection)

        # Generation of the title bar
        self.titlebar_init()

        location = "bin//system_content//visual_content//responsive//"

        self.root.config(bg="DarkOliveGreen4")
        self.frame.config(bg="ForestGreen")

        self.left_side = tk.Frame(self.frame, bg="#43575f")
        self.right_side = tk.Frame(self.frame, bg="#3b4d54")

        self.left_side.pack(side=tk.LEFT, fill=tk.BOTH)
        self.right_side.pack(side=tk.LEFT, fill=tk.BOTH)

        self.person_icon_img = tk.PhotoImage(file=location + "user_white.png")
        self.license_img = tk.PhotoImage(file=location + "license.png")
        self.male_img = tk.PhotoImage(file=location + "male.png")
        self.female_img = tk.PhotoImage(file=location + "female.png")
        self.people_adder_img = tk.PhotoImage(file=location + "add_person.png")
        self.about_img = tk.PhotoImage(file=location + "about.png")
        self.nut_img = tk.PhotoImage(file=location + "nut.png")

        # Generation of the structure of the body
        self.left_side_structure_top(location)
        self.left_side_structure_middle(location)
        self.left_side_structure_bottom(location)
        self.right_side_structure_top(location)
        self.right_side_structure_middle(location)
        self.right_side_structure_bottom(location)

    def titlebar_init(self):
        """
        Generation of the new Title Bar and elimination of the previous one.
        """
        location = "bin//system_content//visual_content//responsive//"

        self.titlebar_img = []
        for img in ("close-button.png", "maximize-button.png",
                    "minimize-button.png", "BirDayBerIcon.png"):
            self.titlebar_img.append(tk.PhotoImage(file=location + img))

        self.title_bar = tk.Frame(
            self.frame, bg="#316477", height=round(self.screen_height / 20))
        self.title_bar.pack(fill=tk.X)

        buttons = []
        for index in range(3):  # Generation of buttons
            buttons.append(tk.Button(
                self.title_bar, image=self.titlebar_img[index], bg="#2c5c6d",
                relief=tk.FLAT, bd=0, activebackground="#1e5061"))
            buttons[index].pack(side=tk.RIGHT, ipadx=14, ipady=7, fill=tk.Y)

        buttons[0].config(
            activebackground="#911722", command=self.close_client)
        buttons[2].config(command=self.title_bar_minimize)

        self.icon = tk.Label(
            self.title_bar, image=self.titlebar_img[3], bg="#316477")
        self.icon.pack(side=tk.LEFT)

        for label in (self.title_bar, self.icon):
            label.bind("<ButtonPress-1>", self.cursor_start_move)
            label.bind("<B1-Motion>", self.window_dragging)

    def left_side_structure_top(self, location):
        """
        Method that generates the base for the top-left appearance of the GUI.
        """
        self.left_top = tk.Frame(self.left_side, bg="#43575f")
        self.search_edge = tk.Frame(self.left_top, bg="#334248")
        self.search_background = tk.Frame(self.search_edge, bg="#517684")

        self.title = tk.Label(
            self.left_top, bg="#334248", text="BirDayBer", fg="#e3e3e3",
            font=("Century Gothic", round(self.screen_width / 38)))

        self.person_icon = tk.Label(
            self.search_background, image=self.person_icon_img, bg="#4d717f")

        self.search_entry = tk.Entry(
            self.search_background, bg="#517684", selectbackground="#4a92ab",
            relief=tk.FLAT, fg="#e3e3e3", insertbackground="#d7f5ff",
            width=round(self.screen_width / 75),
            font=("Century Gothic", round(self.screen_width / 60)))
        self.search_entry.insert(0, "Search")  # Remove from here later

        self.left_top.pack()
        self.person_icon.pack(side=tk.LEFT)

        self.title.pack(
            anchor="w", padx=(self.screen_width * 0.0162, 0),
            pady=self.screen_width * 0.015)

        self.search_edge.pack(
            anchor="w", padx=(self.screen_width * 0.0162))

        self.search_background.pack(pady=(0, self.screen_height * 0.014))

        self.search_entry.pack(
            side=tk.LEFT, fill=tk.Y, padx=(self.screen_width / 100, 0))

    def left_side_structure_middle(self, location):
        """
        Method that generates the base for the mid-left appearance of the GUI.
        """
        self.left_middle = tk.Frame(self.left_side, bg="#334248")

        self.people_over = tk.Label(
            self.left_middle, relief=tk.FLAT, text="People",
            font=("Century Gothic", round(self.screen_width / 64)),
            width=round(self.screen_width / 57), bg="#5f99af", fg="#e7e7e7")

        self.people_finder = tk.Label(
            self.left_middle, bg="#5d8999",
            height=round(self.screen_height / 34))

        self.left_middle.pack(pady=(self.screen_height * 0.017, 0))
        self.people_over.pack(side=tk.TOP)

        self.people_finder.pack(
            fill=tk.X, pady=(0, self.screen_height * 0.013))

    def left_side_structure_bottom(self, location):
        """
        Method that generates the base for the bot-left appearance of the GUI.
        """
        self.left_bottom = tk.Frame(self.left_side, bg="#43575f")

        self.license_icon = tk.Label(
            self.left_bottom, image=self.license_img, bg="#43575f")

        self.left_bottom.pack(fill=tk.BOTH, ipady=50)
        self.license_icon.pack(
            side=tk.LEFT, pady=(self.screen_height * 0.012, 0),
            padx=(self.screen_width * 0.0162, 0))

    def right_side_structure_top(self, location):
        """
        Method that generates the base for the top-right appearance of the GUI.
        """
        self.right_top = tk.Frame(self.right_side, bg="#3b4d54")
        self.people_adder_bg = tk.Frame(self.right_top, bg="#367892")

        self.people_adder = tk.Label(
            self.people_adder_bg, bg="#66838e",
            width=round(self.screen_width / 20),
            height=round(self.screen_height / 108.5))

        self.people_adder_icon = tk.Label(
            self.right_top, bg="#3b4d54", image=self.people_adder_img)
        self.nut_icon = tk.Label(
            self.right_top, bg="#3b4d54", image=self.nut_img)
        self.about_icon = tk.Label(
            self.right_top, bg="#3b4d54", image=self.about_img)

        self.right_top.pack(side=tk.TOP)
        self.people_adder_bg.pack(
            padx=(self.screen_width * 0.0518, 0),
            pady=(self.screen_height * 0.03, 0), side=tk.LEFT)
        self.people_adder.pack(padx=self.screen_height * 0.005)
        self.people_adder_icon.pack(
            pady=(self.screen_height * 0.090, 0), side=tk.LEFT)
        for icon in (self.nut_icon, self.about_icon):
            icon.pack(
                padx=(self.screen_width * 0.14, self.screen_width * 0.011),
                pady=(self.screen_height * 0.015, 0), side=tk.TOP)

        self.people_adder_structure()

    def people_adder_structure(self):
        """
        Method that generates the structure (no functionality)
        to the "self.people_adder" widget.
        """
        self.first_name_edge = tk.Frame(self.people_adder, bg="#136687")
        self.second_name_edge = tk.Frame(self.people_adder, bg="#136687")
        self.birth_date_edge = tk.Frame(self.people_adder, bg="#136687")
        self.country_edge = tk.Frame(self.people_adder, bg="#136687")

        self.first_name = tk.Entry(
            self.first_name_edge, bg="blue", relief=tk.FLAT,
            font=("Century Gothic", round(self.screen_width * 0.007)),
            width=round(self.screen_width * 0.0115))
        self.second_name = tk.Entry(
            self.second_name_edge, bg="red", relief=tk.FLAT,
            font=("Century Gothic", round(self.screen_width * 0.007)),
            width=round(self.screen_width * 0.0115))
        self.birth_date = tk.Entry(
            self.birth_date_edge, bg="green", relief=tk.FLAT,
            font=("Century Gothic", round(self.screen_width * 0.007)),
            width=round(self.screen_width * 0.0115))
        self.country = tk.Entry(
            self.country_edge, bg="purple", relief=tk.FLAT,
            font=("Century Gothic", round(self.screen_width * 0.007)),
            width=round(self.screen_width * 0.0115))

        self.first_name_edge.grid(
            row=0, column=0,
            pady=(self.screen_height * 0.0315, self.screen_height * 0.01575))
        self.second_name_edge.grid(
            row=1, column=0,
            pady=(self.screen_height * 0.01575, self.screen_height * 0.0315))
        self.birth_date_edge.grid(
            row=0, column=1,
            pady=(self.screen_height * 0.0315, self.screen_height * 0.01575))
        self.country_edge.grid(
            row=1, column=1,
            pady=(self.screen_height * 0.01575, self.screen_height * 0.0315))

        self.first_name.pack()
        self.second_name.pack()
        self.birth_date.pack()
        self.country.pack()

    def right_side_structure_middle(self, location):
        """
        Method that generates the base for the mid-right appearance of the GUI.
        """
        pass

    def right_side_structure_bottom(self, location):
        """
        Method that generates the base for the bop-right appearance of the GUI.
        """
        pass


class Birdayber(Interface_structure):
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
