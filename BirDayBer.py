import db_manager
import tkinter as tk
import os


class Birdayber_client:
    def __init__(self, db_connection, mainloop=False):
        """
        Method that only accepts a sqlite3 database lotaction and Boolean:
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
        Method that only accepts sqlite3 database locations:
        Generation of the database connection and tables.
        The generation of the tables is pre-created.
        """
        self.db = db_manager.Db_manager(db_connection)
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        self.db.create_table({
            "gender":
                f"""id_gender {id_type},
                gender VARCHAR(6) NOT NULL""",
            "photo":
                f"""id_photo {id_type},
                photo BLOB""",
            "country":
                f"""id_country {id_type},
                country VARCHAR(40)""",
            "birth":
                f"""id_birth {id_type},
                id_country2_fk INTEGER,
                birth DATE NOT NULL,
                age INTEGER""",
            "person":
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
            "add_person method only accepts as a parameter a <class 'dict'>," +
            " but a '%s' was recieved." % type(person))

    def get_people(self, id_person="&None%", binary=True):  # Continue here...
        """
        Method that only accepts Str or Int:
        This method brings all the information of the people.
        The parameter "id" is part of a WHERE clause. If there's no WHERE
        given, then all the data will be displayed.

        Special parameters:

        If the 'id_person' parameter is "&None%",
        then there'll be no WHERE clause.

        If the 'binary' parameter is False, then the photo (BLOB) 
        will be omitted. If it's True, then it will return
        the binary data that it has (the photo data).
        """
        if binary:
            selection = (
                "per_first, per_last, birth, age, photo, country, gender",
                "INNER JOIN photo on photo.id_photo = person.id_photo1_fk")
        elif binary is False:
            selection = (
                "per_first, per_last, birth, age, country, gender",
                "INNER JOIN photo on photo.id_photo = person.id_photo1_fk")

        if id_person != "&None%":
            id_person = "id_person = %s" % id_person

        people_data = self.db.column_search(
            "person", selection[0],
            """INNER JOIN
                birth on birth.id_birth = person.id_birth1_fk %s
            INNER JOIN
                country on country.id_country = person.id_country1_fk
            INNER JOIN
                gender on gender.id_gender = person.id_gender1_fk"""
            % (selection[1]), id_person)

        return people_data

    def drop_database(self):
        """
        This method deletes the database file.
        """
        self.db.drop_database()

    def close_client(self):
        """
        It makes the program stop mainlooping.
        """
        self.window.destroy()


if __name__ == '__main__':
    BirDayBer = Birdayber_client("bin//BirDayBer_db.db", True)
