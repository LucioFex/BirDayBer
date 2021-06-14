import dependencies.db_manager as db_manager
import unittest
"""
Testing file of BirDayBer.py.
"""


class BirDayBerDB_testing(unittest.TestCase):
    """
    BirDayBer database testing.
    """
    @classmethod
    def setUpClass(cls):
        """
        It connects the testing DB and creates the tables and some rows.
        """
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        cls.birth_db = db_manager.Db_manager("testing//test.db")
        cls.birth_db.create_table({
            "gender":
                f"id_gender {id_type}, gender VARCHAR(6)",

            "photo":
                f"id_photo {id_type}, photo_name VARCHAR(20), photo BLOB",

            "country":
                f"id_country {id_type}, country VARCHAR(40)",

            "birth":
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
                FOREIGN KEY (id_birth1_fk) REFERENCES birth (id_birth),
                FOREIGN KEY (id_photo1_fk) REFERENCES photo (id_photo)"""})
        del id_type

    @classmethod
    def tearDownClass(cls):
        """
        It close the DB and delete it.
        """
        cls.birth_db.close_database()
        cls.birth_db.drop_database()

    def setUp(self):
        """
        Insertion of all testing data.
        """
        self.birth_db.add_rows({
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": 'testing//image_test.png'},
            "birth": {"birth": "2003-07-15", "age": None},
            "person": {"per_first": "Severus", "per_last": "Snape"}})

        self.birth_db.add_rows({
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo_name": "No photo", "photo": None},
            "birth": {"birth": "1919-12-23", "age": None},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    def tearDown(self):
        """
        Deletion of every row in the columns.
        """
        for table in ("country", "gender", "photo", "birth", "person"):
            self.birth_db.remove_rows(table, "&deleteAll")

    def test_genders(self):
        all_genders = self.birth_db.column_search("gender", "gender")

        self.assertEqual(all_genders, (("Male",), ("Male",)))
        self.assertEqual(len(all_genders), 2)

        deleted = self.birth_db.remove_rows("gender", "gender = 'Male'")
        all_genders = self.birth_db.column_search("gender", "gender")

        self.assertEqual(deleted, "2 rows deleted")
        self.assertEqual(all_genders, ())
        self.assertEqual(len(all_genders), 0)

    def test_photos(self):
        all_photos = self.birth_db.column_search("photo", "photo_name, photo")
        self.assertNotEqual(all_photos, ((None, None), (None, None)))
        self.assertEqual(len(all_photos), 2)

        all_photos = self.birth_db.column_search("photo", "photo_name")
        self.assertEqual(all_photos, ((None,), ("No photo",)))

        deleted = self.birth_db.remove_rows("photo", "photo is Null")
        all_photos = self.birth_db.column_search("photo", "photo")
        self.assertEqual(deleted, "1 rows deleted")
        self.assertNotEqual(all_photos, ((None,), ))
        self.assertEqual(len(all_photos), 1)

        all_photos = self.birth_db.column_search("photo", "id_photo, photo")

        db_manager.binary_to_photo(
            all_photos[0][0], all_photos[0][1], "testing//")
        db_manager.delete_files("testing//photo_%s.png" % all_photos[0][0])

    def test_countries(self):
        all_countries = self.birth_db.column_search("country", "country")

        self.assertEqual(all_countries, (("Argentina",), ("United States",)))
        self.assertEqual(len(all_countries), 2)

        deleted = self.birth_db.remove_rows("country", "country = 'Argentina'")
        all_countries = self.birth_db.column_search("country", "country")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_countries, (("United States",),))
        self.assertEqual(len(all_countries), 1)

    def test_births(self):
        all_births = self.birth_db.column_search("birth", "birth")

        self.assertEqual(all_births, (("2003-07-15",), ("1919-12-23",)))
        self.assertEqual(len(all_births), 2)

        deleted = self.birth_db.remove_rows(
            "birth", "birth = '1919-12-23'")
        all_births = self.birth_db.column_search("birth", "birth")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_births, (("2003-07-15",),))
        self.assertEqual(len(all_births), 1)

    def test_people(self):
        all_people = self.birth_db.column_search(
            "person", "per_first, per_last")

        self.assertEqual(all_people, (
            ("Severus", "Snape"), ("Randolph", "Carter")))
        self.assertEqual(len(all_people), 2)

        deleted = self.birth_db.remove_rows("person", "per_first = 'Severus'")
        all_people = self.birth_db.column_search("person", "per_first")

        self.assertEqual(deleted, "1 rows deleted")
        self.assertEqual(all_people, (("Randolph",),))
        self.assertEqual(len(all_people), 1)

    def test_data(self):
        # self.birth_db.remove_rows("person", "per_first = 'Randolph'")
        all_data = self.birth_db.column_search(
            "person", "per_first, per_last, country, gender, birth",
            """INNER JOIN country on country.id_country = person.id_country1_fk
            INNER JOIN gender on gender.id_gender = person.id_gender1_fk
            INNER JOIN birth on birth.id_birth = person.id_birth1_fk""")

        self.assertEqual(all_data, (
            ("Severus", "Snape", "Argentina", "Male", "2003-07-15",),
            ("Randolph", "Carter", "United States", "Male", "1919-12-23",)))

    def test_foreign_values(self):
        foregin_values = self.birth_db.column_search(
            "person", """per_first, id_person, id_country1_fk,
            id_gender1_fk, id_birth1_fk, id_photo1_fk""")

        fk_1 = foregin_values[0][1]  # Example of foreign key of Subject 1
        fk_2 = foregin_values[1][1]  # Example of foreign key of Subject 2
        self.assertEqual(foregin_values, (
            ("Severus", fk_1, fk_1, fk_1, fk_1, fk_1),
            ("Randolph", fk_2, fk_2, fk_2, fk_2, fk_2)))


if __name__ == "__main__":
    unittest.main()
