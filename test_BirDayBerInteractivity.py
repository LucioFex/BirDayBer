import unittest
import BirDayBer
"""
Testing file for BirDayBer.py user's interactivity.
"""


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


if __name__ == "__main__":
    unittest.main()
