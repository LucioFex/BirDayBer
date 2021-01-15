import unittest
# import BirDayBer
import db_manager
import os


class BirthDB_testing(unittest.TestCase):
    """
    BirDayBer database's testing.
    """
    @classmethod
    def setUpClass(cls):
        """
        It connects the testing DB and creates the tables and some rows.
        """
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
                f"""id_birth {id_type},
                id_country2_fk INTEGER, birth DATE, age INTEGER,
                FOREIGN KEY (id_country2_fk)
                REFERENCES country (id_country)""",

            "person":
                f"""id_person {id_type}, per_first VARCHAR(35),
                per_last VARCHAR(35), id_country1_fk INTEGER,
                id_gender1_fk INTEGER, id_birth1_fk INTEGER,
                id_photo1_fk INTEGER,
                FOREIGN KEY (id_country1_fk) REFERENCES country (id_country),
                FOREIGN KEY (id_gender1_fk) REFERENCES gender (id_gender),
                FOREIGN KEY (id_birth1_fk) REFERENCES birth_date (id_birth),
                FOREIGN KEY (id_photo1_fk) REFERENCES photo (id_photo)"""})
        del id_type

    @classmethod
    def tearDownClass(cls):
        """
        It close the DB and delete it.
        """
        cls.birth_db.close_database()
        os.remove("test_db.db")

    def setUp(self):
        """
        Insertion of all testing data
        """
        self.birth_db.add_rows({  # ID 1
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": 'conceptual/image_test.png'},
            "birth_date": {"birth": "2003-11-18", "age": None},
            "person": {"per_first": "Franco", "per_last": "Frias"}})

        self.birth_db.add_rows({  # ID 2
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth_date": {"birth": "1919-12-23", "age": None},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    def tearDown(self):
        """
        Deletion of every row in the columns.
        """
        for table in ("country", "gender", "photo", "birth_date", "person"):
            self.birth_db.remove_rows(table, "&deleteAll")

    def test_check_genders(self):
        all_genders = self.birth_db.column_search("gender", "gender")

        self.assertEqual(all_genders, (("Male",), ("Male",)))
        self.assertEqual(len(all_genders), 2)

        deleted = self.birth_db.remove_rows("gender", "gender = 'Male'")
        all_genders = self.birth_db.column_search("gender", "gender")

        self.assertEqual(deleted, "2 rows deleted")
        self.assertEqual(all_genders, ())
        self.assertEqual(len(all_genders), 0)

    def test_check_photos(self):
        all_photos = self.birth_db.column_search("photo", "photo")

        self.assertNotEqual(all_photos, ((None,), (None,)))
        self.assertEqual(len(all_photos), 2)

        deleted = self.birth_db.remove_rows("photo", "photo is Null")
        all_photos = self.birth_db.column_search("photo", "photo")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertNotEqual(all_photos, ((None,), ))
        self.assertEqual(len(all_photos), 1)

        all_photos = self.birth_db.column_search("photo", "id_photo, photo")
        db_manager.binary_to_photo(all_photos[0][0], all_photos[0][1])
        os.remove("bin//rows_content//photos//photo_%s.png" % all_photos[0][0])

    def test_check_countries(self):
        all_countries = self.birth_db.column_search("country", "country")

        self.assertEqual(all_countries, (("Argentina",), ("United States",)))
        self.assertEqual(len(all_countries), 2)

        deleted = self.birth_db.remove_rows("country", "country = 'Argentina'")
        all_countries = self.birth_db.column_search("country", "country")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_countries, (("United States",),))
        self.assertEqual(len(all_countries), 1)

    def test_check_births(self):
        all_births = self.birth_db.column_search("birth_date", "birth")

        self.assertEqual(all_births, (("2003-11-18",), ("1919-12-23",)))
        self.assertEqual(len(all_births), 2)

        deleted = self.birth_db.remove_rows(
            "birth_date", "birth = '1919-12-23'")
        all_births = self.birth_db.column_search("birth_date", "birth")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_births, (("2003-11-18",),))
        self.assertEqual(len(all_births), 1)

    def test_check_people(self):
        all_people = self.birth_db.column_search(
            "person", "per_first, per_last")

        self.assertEqual(all_people, (
            ("Franco", "Frias"), ("Randolph", "Carter")))
        self.assertEqual(len(all_people), 2)

        deleted = self.birth_db.remove_rows("person", "per_first = 'Franco'")
        all_people = self.birth_db.column_search("person", "per_first")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_people, (("Randolph",),))
        self.assertEqual(len(all_people), 1)

    def test_check_data(self):
        # self.birth_db.remove_rows("person", "per_first = 'Randolph'")
        all_data = self.birth_db.column_search(
            "person", "per_first, per_last, country, gender, birth",
            """INNER JOIN
                country on country.id_country = person.id_country1_fk
            INNER JOIN
                gender on gender.id_gender = person.id_gender1_fk
            INNER JOIN
                birth_date on birth_date.id_birth = person.id_birth1_fk""")

        self.assertEqual(all_data, (
            ("Franco", "Frias", "Argentina", "Male", "2003-11-18"),
            ("Randolph", "Carter", "United States", "Male", "1919-12-23")))


if __name__ == "__main__":
    unittest.main()
