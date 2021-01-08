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

    @classmethod
    def tearDownClass(cls):
        # It should close the DB.
        cls.birth_db.close_database()

    def setUp(self):
        pass

    def tearDown(self):
        # All rows deletion.  Check later
        # self.birth_db.remove_rows("gender", "&deleteAll")
        # self.birth_db.remove_rows("photo", "&deleteAll")
        # self.birth_db.remove_rows("birth_date", "&deleteAll")
        # self.birth_db.remove_rows("person", "&deleteAll")
        pass

    def test_check_genders(self):
        all_genders = self.birth_db.column_search("gender", "gender")

        self.assertEqual(all_genders, ("Male", "Male"))
        self.assertEqual(len(all_genders), 2)

        deleted = self.birth_db.remove_rows("gender", "id_gender = 1")
        all_genders = self.birth_db.column_search("gender", "gender")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_genders, ("Male",))
        self.assertEqual(len(all_genders), 1)

    def test_check_photos(self):
        all_photos = self.birth_db.column_search("photo", "photo")

        self.assertEqual(all_photos, (None, None))
        self.assertEqual(len(all_photos), 2)

        deleted = self.birth_db.remove_rows("photo", "id_photo = 1")
        all_photos = self.birth_db.column_search("photo", "photo")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_photos, (None,))
        self.assertEqual(len(all_photos), 1)

    def test_check_countries(self):
        all_countries = self.birth_db.column_search("country", "country")

        self.assertEqual(all_countries, ("Argentina", "United States"))
        self.assertEqual(len(all_countries), 2)

        deleted = self.birth_db.remove_rows("country", "id_country = 1")
        all_countries = self.birth_db.column_search("country", "country")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_countries, ("United States",))
        self.assertEqual(len(all_countries), 1)

    def test_check_births(self):
        all_births = self.birth_db.column_search("birth_date", "birth")

        self.assertEqual(all_births, ("2003-11-18", "1919-12-23"))
        self.assertEqual(len(all_births), 2)

        deleted = self.birth_db.remove_rows("birth_date", "id_birth = 1")
        all_births = self.birth_db.column_search("birth_date", "birth")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_births, ("1919-12-23",))
        self.assertEqual(len(all_births), 1)

    def test_check_people(self):
        all_people = self.birth_db.column_search("person", "per_first")

        self.assertEqual(all_people, ("Franco", "Randolph"))
        self.assertEqual(len(all_people), 2)

        deleted = self.birth_db.remove_rows("person", "id_person = 1")
        all_people = self.birth_db.column_search("person", "per_first")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_people, ("Randolph",))
        self.assertEqual(len(all_people), 1)


if __name__ == "__main__":
    unittest.main()
