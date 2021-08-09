import dependencies.db_manager as db_manager
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
    def __init__(self):
        """
        Method that only accepts a sqlite3 database lotaction and Boolean:
        Creation of the database and preparation to generate the interface.
        If the second parameter is 'True' the program will start main-looping.
        """
        super().__init__()
        #  Db management and generation:
        if not os.path.exists(self.db_path):  # If there's not db
            self.generate_database()
        self.db = db_manager.Db_manager(self.db_path)  # If there's a db

    def generate_database(self):
        """
        Method that only accepts sqlite3 database locations:
        Generation of the database connection and tables.
        The generation of the tables is pre-created.
        """
        self.db = db_manager.Db_manager(self.db_path)
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
                birth DATE NOT NULL""",
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

        return self.db_path

    def add_person(self, person):
        """
        Method that only accepts dicts:
        Addition of people to the database.
        Every key in the dictionary must be a String, like in the example.

        Example:
            self.add_person({
                "country": {"country": "United States"},
                "gender": {"gender": "Male"},
                "photo": {"photo": None},
                "birth": {"birth": "1919-12-23"},
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
            select = "per_first, per_last, birth, photo, country, gender"
        elif not binary:
            select = "per_first, per_last, birth, country, gender"

        people_data = self.db.column_search(
            "person", select,
            """INNER JOIN
                birth on birth.id_birth = person.id_birth1_fk
            INNER JOIN
                photo on photo.id_photo = person.id_photo1_fk
            INNER JOIN
                country on country.id_country = person.id_country1_fk
            INNER JOIN
                gender on gender.id_gender = person.id_gender1_fk""",
            id_person)

        return people_data

    def remove_person(self, person_id):
        """
        This method removes one person.
        """
        self.db.remove_rows("person", f"id_person = {person_id}")

    def reset_database(self):
        """
        Reset of the entire database.
        """
        for table in ("country", "gender", "photo", "birth", "person"):
            self.db.remove_rows(table, "&deleteAll")

    def drop_database(self):
        """
        This method deletes the database file.
        """
        self.db.close_database()
        self.db.drop_database()
