from datetime import datetime
import unittest
import BirDayBer
"""
Testing file for BirDayBer.py user's interactivity.
"""


def current_age(birth_date):
    """
    Function that calculates the inserted birth date (YYYY-MM-DD),
    and calculates the current age in a INT.
    """
    birth_date = birth_date.split("/")
    birth_date = f"{birth_date[2]}-{birth_date[1]}-{birth_date[0]}"

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
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": 'testing//image_test.png'},
            "birth": {"birth": "2003-07-15"},
            "person": {"per_first": "Severus", "per_last": "Snape"}})
        self.interface.add_person({
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth": {"birth": "1919-12-23"},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    def tearDown(self):
        self.interface.remove_all_people()

    def test_settings_button(self):
        self.assertFalse(self.interface.get_settings())
        self.interface.open_settings()

        self.assertTrue(self.interface.get_settings())
        self.assertEqual(len(self.interface.settings.winfo_children()), 5)

        self.interface.close_settings()
        self.assertFalse(self.interface.get_settings())

    def test_people_viewer(self):
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 3)
        self.interface.remove_person(1)
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 2)
        self.interface.remove_person(2)
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 1)

    def test_people_browser(self):
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 3)
        self.interface.seach_person("ape")
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 2)
        self.interface.seach_person("")
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 3)
        self.interface.seach_person("randolphofenicalado")
        self.assertTrue(len(self.interface.people_finder.winfo_children()), 1)

    def test_person_select(self):
        age = current_age(self.interface.get_selected_person("birth"))

        # No person selected
        self.assertEqual(len(self.interface.right_bg.winfo_children()), 1)
        self.assertIsNone(self.interface.get_selected_person())

        # Person selected
        self.interface.select_person(1)
        self.assertEqual(len(self.interface.right_bg.winfo_children()), 9)

        self.assertEqual(
            self.interface.get_selected_person(), [
                "Randolph", "Carter", "23/12/1919", age,
                "Male", "United States", "12/1919"])


if __name__ == "__main__":
    unittest.main()