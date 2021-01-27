import unittest
import BirDayBer
"""
Testing file of BirDayBer.py.
"""


class BirDayBerClient_testing(unittest.TestCase):
    """
    BirDayBer graphical user interface testing.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the GUI and adds some people to be tested.
        """
        cls.interface = BirDayBer.Birdayber_client("testing/BirDayBer_db.db")

        cls.interface.add_person({  # ID 1
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": 'testing/image_test.png'},
            "birth": {"birth": "2003-07-15", "age": None},
            "person": {"per_first": "Severus", "per_last": "Snape"}})
        cls.interface.add_person({  # ID 2
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth": {"birth": "1919-12-23", "age": None},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    @classmethod
    def tearDownClass(cls):
        """
        Finish the process of the GUI and deletes all tested people.
        """
        people_id = cls.interface.get_people("id")
        for person in people_id:
            cls.interface.delete_person(person[0])

        cls.interface.close_client()
        cls.interface.drop_database()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_window_size(self):
        position = self.interface.window_resolution()

        self.assertNotEqual(position, "1x1+0+0")
        self.assertEqual(type(position), str)

    def test_people(self):
        all_people = self.interface.get_people("&all", "id")

        # id-name-photo-birthDate-age-country-gender-date (natural order)
        self.assertEqual(all_people, (
            (
                "Severus", "Snape", "testing/image_test.png",
                "2003", None, "Argentina",
                "Male", "2003-07-15"),
            (
                "Randolph", "Carter", None,
                "1919", None, "United States",
                "Male", "1919-12-23")))

    def test_license(self):
        license_data = self.interface.get_license()
        self.assertEqual(
            license_data, "Mit License", "2020-2021", "Luciano Esteban")

    def test_image(self):
        person_id = self.interface.get_people("photo", type="bytes")[0][0]
        self.assertEqual(type(person_id), bytes)

    def test_birthdayNotation(self):
        notification = self.interface.get_birthdays("num")
        self.assertEqual(notification, 0)


if __name__ == "__main__":
    unittest.main()
