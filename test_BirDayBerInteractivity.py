from datetime import datetime
import unittest
import BirDayBer
"""
Testing file for BirDayBer.py user's interactivity.
"""


def current_age(birth_date):
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")

    age = today.year - birth_date.year - 1
    if (today.month, today.day) >= (birth_date.month, birth_date.day):
        age += 1
    return age


class BirDayBerInteractivity_testing(unittest.TestCase):
    """
    BirDayBer's user interactivity.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize the GUI and adds some people to be tested.
        """
        cls.interface = BirDayBer.Birdayber("testing//BirDayBer.db")

    @classmethod
    def tearDownClass(cls):
        """
        Finish the process of the GUI and deletes all tested people.
        """
        cls.interface.close_client()
        cls.interface.drop_database()

    def setUp(self):
        self.interface.add_person({
            "countries": {"country": "Argentina"},
            "genders": {"gender": "Male"},
            "photos": {"photo": 'testing//image_test.png'},
            "births": {"birth": "2003-07-15"},
            "people": {"per_first": "Severus", "per_last": "Snape"}})
        self.interface.add_person({
            "countries": {"country": "United States"},
            "genders": {"gender": "Male"},
            "photos": {"photo": None},
            "births": {"birth": "1919-12-23"},
            "people": {"per_first": "Randolph", "per_last": "Carter"}})

    def tearDown(self):
        self.interface.remove_all_people()

    def test_settings_button(self):
        self.assertFalse(self.interface.get_settings())
        self.interface.open_settings()

        self.assertTrue(self.interface.get_settings())
        self.assertEqual(len(self.interface.settings.winfo_children()), 5)

        self.interface.close_settings()
        self.assertFalse(self.interface.get_settings())

    def test_people_view(self):
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 2)
        self.interface.remove_person(1)
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 1)
        self.interface.remove_person(2)
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 0)

    def test_person_select(self):
        # No person selected
        self.assertEqual(len(self.interface.right_bg.winfo_children()), 1)
        self.assertIsNone(self.interface.get_selected_person())

        # Person selected
        self.interface.select_person(1)
        self.assertEqual(len(self.interface.right_bg.winfo_children()), 9)

        self.assertEqual(
            self.interface.get_selected_person(), [
                "Randolph", "Carter", "23/12/1919", 102,
                "Male", "United States", "12/1919"])


if __name__ == "__main__":
    unittest.main()
