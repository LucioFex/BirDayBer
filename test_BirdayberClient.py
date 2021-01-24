import unittest
import BirDayBer
"""
Testing file of BirDayBer.py.
"""


class Birth_testing(unittest.TestCase):
    """
    BirDayBer graphical user interface testing.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the GUI.
        """
        cls.interface = BirDayBer.Birdayber_client()
        cls.interface.new_database()

    @classmethod
    def tearDownClass(cls):
        """
        Finish the process of the GUI.
        """
        cls.interface.delete_database()
        cls.interface.close_client()

    def setUp(self):
        """
        It adds some people to be tested.
        """
        self.interface.add_person({  # ID 1
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": 'testing/image_test.png'},
            "birth": {"birth": "2003-07-15", "age": None},
            "person": {"per_first": "Severus", "per_last": "Snape"}})

        self.interface.add_person({  # ID 2
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth": {"birth": "1919-12-23", "age": None},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    def tearDown(self):
        """
        It delete all tested people.
        """
        people_id = self.interface.get_all_people("id")

        for person in people_id:
            self.interface.delete_person(person[0])

    def test_window_size(self):
        position = self.interface.get_window()

        self.assertNotEqual(position, "1x1+0+0")
        self.assertEqual(type(position), str)

    def test_menu_buttons(self):
        menu_buttons = self.interface.get_menu_buttons()

        self.assertEqual(len(menu_buttons), 5)
        self.assertEqual(menu_buttons, (
            "Add", "Remove", "Modify", "Config", "About"))

    def test_modifier_buttons(self):
        modifiers = self.interface.get_modifier_buttons()

        self.assertEqual(modifiers, (
            "Add Person", "Edit Person", "Delete Person"))
        self.assertEqual(len(modifiers), 5)

    def test_people(self):
        all_people = self.interface.get_all_people("&all", "id")

        # id-name-photo-birthYear-age-country-gender-date (natural order)
        self.assertEqual(all_people, (
            (
                "Severus", "Snape", "testing/image_test.png",
                "2003", None, "Argentina",
                "Male", "2003-07-15"),
            (
                "Randolph", "Carter", None,
                "1919", None, "United States",
                "Male", "2003-07-15")))

    def test_license(self):
        license_data = self.interface.get_license()

        self.assertEqual(
            license_data, "Mit License", "2020-2021", "Luciano Esteban")


if __name__ == "__main__":
    unittest.main()
