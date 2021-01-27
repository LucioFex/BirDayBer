import db_manager
import tkinter as tk
import os


class Birdayber_client:
    def __init__(self, db_connection, mainloop=False):
        """
        Creation of the database and previous configuration of the main window.
        If the second parameter is 'True' the program will main-loop.
        """
        #  Db management and generation:
        if os.path.exists(db_connection) is False:  # If there's not db
            self.generate_database(db_connection)
        self.db = db_manager.Db_manager(db_connection)  # If there's a db

        #  Window size and posotion definition. Root generation:
        self.window = tk.Tk()
        self.window.geometry(self.window_resolution())
        self.window.update()
        self.window.mainloop() if mainloop else None

    def window_resolution(self):
        """
        This method returns the information of the best
        possible resolution and position for the client's window.
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        screen_width = screen_width - round(screen_width / 4)
        screen_height = screen_height - round(screen_height / 4)

        x_position = round(screen_width / 6.3)
        y_position = round(screen_height / 7)

        return "%sx%s+%s+%s" % (
            screen_width, screen_height, x_position, y_position)

    def generate_database(self, db_connection):
        """
        Generation of the database connection and tables.
        The generation of the tables is pre-created.
        """
        self.db = db_manager.Db_manager(db_connection)
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        self.db.create_table({
            "gender":
                f"""id_gender {id_type},
                gender VARCHAR(6)""",
            "photo":
                f"""id_photo {id_type},
                photo BLOB""",
            "country":
                f"""id_country {id_type},
                country VARCHAR(40)""",
            "birth":
                f"""id_birth {id_type},
                id_country2_fk INTEGER,
                birth DATE, age INTEGER""",
            "person":
                f"""id_person {id_type},
                per_first VARCHAR(35),
                per_last VARCHAR(35),
                id_country1_fk INTEGER,
                id_gender1_fk INTEGER,
                id_birth1_fk INTEGER,
                id_photo1_fk INTEGER,
                FOREIGN KEY (id_country1_fk) REFERENCES country (id_country),
                FOREIGN KEY (id_gender1_fk) REFERENCES gender (id_gender),
                FOREIGN KEY (id_birth1_fk) REFERENCES birth (id_birth),
                FOREIGN KEY (id_photo1_fk) REFERENCES photo (id_photo)"""})

        del id_type
        return db_connection

    def add_person(self, person):
        """
        Addition of people to the database. The method only accepts 'dicts'.

        For example:
            self.add_person({
                "country": {"country": "United States"},
                "gender": {"gender": "Male"},
                "photo": {"photo": None},
                "birth": {"birth": "1919-12-23", "age": None},
                "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """
        if type(person) == dict:
            return self.db.add_rows(person)

        raise ValueError(
            "add_person method only accepts as a parameter a 'dict' type" +
            "but recieved %s." % type(person))


if __name__ == '__main__':
    BirDayBer = Birdayber_client("bin//BirDayBer_db.db", True)
