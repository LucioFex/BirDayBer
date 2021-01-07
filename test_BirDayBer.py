import unittest
# import BirDayBer
import db_manager


class BirthDB_testing(unittest.TestCase):
    # BirDayBer database's testing
    @classmethod
    def setUpClass(cls):
        # It should connect the testing DB.
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        cls.birth_db = db_manager.Db_manager("test_db.db")
        cls.birth_db.create_table({
            "gender":
                f"id_gender {id_type}, gender VARCHAR(6)",

            "photo":
                f"id_photo {id_type}, photo BLOB",

            "country":
                f"id_country {id_type}, country VARCHAR(40)",

            "birth_date":
                f"id_birth {id_type}, " +
                "id_country2 INTEGER, birth DATE, age INTEGER, " +
                "FOREIGN KEY (id_country2) REFERENCES country (id_country)",

            "person":
                f"id_person {id_type}, per_first VARCHAR(35), " +
                "per_last VARCHAR(35), id_country1 INTEGER, " +
                "id_gender1 INTEGER, id_birth1 INTEGER, id_photo1 INTEGER, " +
                "FOREIGN KEY (id_country1) REFERENCES country (id_country), " +
                "FOREIGN KEY (id_gender1) REFERENCES gender (id_gender), " +
                "FOREIGN KEY (id_birth1) REFERENCES birth_date (id_birth), " +
                "FOREIGN KEY (id_photo1) REFERENCES photo (id_photo)"})

        del id_type

    @classmethod
    def tearDownClass(cls):
        # It should close the DB.

        cls.birth_db.close_database()

    def setUp(cls):
        # The ID will be set automatically.

        cls.birth_db.add_rows({  # ID 1
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth_date": {"birth": "2003-11-18", "age": None},
            "person": {"per_first": "Franco", "per_last": "Frias"}})

        cls.birth_db.add_rows({  # ID 2
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth_date": {"birth": "1919-12-23", "age": None},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    def tearDown(cls):
        # All rows deletion.

        cls.birth_db.remove_rows([1, 2])  # id 1 = Franco | id 2 = Randolph

    def test_check_names(self, cls):
        self.all_names = cls.birth_db.column_search("person", "per_first")

        self.assertEqual(self.all_names, ("Franco", "Randolph"))
        self.assertEqual(len(self.all_names), 2)

    def test_check_surnames(self, cls):
        self.all_surnames = cls.birth_db.column_search("person", "per_last")

        self.assertEqual(self.all_surnames, ("Frias", "Carter"))
        self.assertEqual(len(self.all_surnames), 2)

    def test_check_births(self, cls):
        self.all_births = cls.birth_db.column_search("birth_date", "birth")

        self.assertEqual(self.all_births, ("2003-11-18", "1919-12-23"))
        self.assertEqual(len(self.all_births), 2)

    def test_check_ages(self, cls):
        self.all_ages = cls.birth_db.column_search("birth_date", "age")

        self.assertEqual(self.all_ages, (None, None))
        self.assertEqual(len(self.all_ages), 2)

    def test_check_countries(self, cls):
        self.all_countries = cls.birth_db.column_search("country", "country")

        self.assertEqual(self.all_countries, ("Argentina", "United States"))
        self.assertEqual(len(self.all_countries), 2)

    def test_check_genders(self, cls):
        self.all_genders = cls.birth_db.column_search("gender", "gender")

        self.assertEqual(self.all_genders, ("Male", "Male"))
        self.assertEqual(len(self.all_genders), 2)

    def test_check_photos(self, cls):
        self.all_photos = cls.birth_db.column_search("photo", "photo")

        self.assertEqual(self.all_photos, (None, None))
        self.assertEqual(len(self.all_photos), 2)


# if __name__ == "__main__":
#     unittest.main()
