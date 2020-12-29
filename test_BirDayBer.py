import unittest
# import BirDayBer
import BirDayBerDB_manager


class BirthDB_testing(unittest.TestCase):
    # BirDayBer database's testing
    @classmethod
    def setUpClass(cls):
        # It should connect the testing DB.

        cls.birth_db = BirDayBerDB_manager.Birthdays_db()
        cls.birth_db.prepare_database("test_db.db")

    @classmethod
    def tearDownClass(cls):
        # It should close the DB.

        cls.birth_db.close_database()

    def setUp(self, cls):
        # The ID will be set automatically.

        cls.birth_db.add_person("Franco", "Frias", "Argentina",
                                "Male", "2003-11-18", None)

        cls.birth_db.add_person("Randolph", "Carter", "United States",
                                "Male", "1919-12-23", None)

    def tearDown(self, cls):
        # All rows deletion.

        cls.birth_db.remove_people([1, 2])  # id 1 = Franco | id 2 = Randolph

    def test_check_names(self, cls):
        self.all_names = cls.birth_db.people_names()

        self.assertEqual(self.all_names, ("Franco", "Randolph"))
        self.assertEqual(len(self.all_names), 2)

    def test_check_surnames(self, cls):
        self.all_surnames = cls.birth_db.people_surnames()

        self.assertEqual(self.all_surnames, ("Frias", "Carter"))
        self.assertEqual(len(self.all_surnames), 2)

    def test_check_births(self, cls):
        self.all_births = cls.birth_db.people_birth()

        self.assertEqual(self.all_births, ("2003-11-18", "1919-12-23"))
        self.assertEqual(len(self.all_births), 2)

    def test_check_ages(self, cls):
        self.all_ages = cls.birth_db.people_age()

        self.assertEqual(self.all_ages, ("Frias", "Carter"))
        self.assertEqual(len(self.all_ages), 2)

    def test_check_countries(self, cls):
        self.all_countries = cls.birth_db.people_age()

        self.assertEqual(self.all_countries, ("Argentina", "United States"))
        self.assertEqual(len(self.all_countries), 2)

    def test_check_genders(self, cls):
        self.all_genders = cls.birth_db.people_age()

        self.assertEqual(self.all_genders, ("Male", "Male"))
        self.assertEqual(len(self.all_genders), 2)

    def test_check_photos(self, cls):
        self.all_photos = cls.birth_db.people_age()

        self.assertEqual(self.all_photos, (None, None))
        self.assertEqual(len(self.all_photos), 2)


if __name__ == "__main__":
    unittest.main()
