import unittest
import BirDayBer
import os
"""
Testing file for BirDayBer.py's base and structure.
"""


class BirDayBerClient_testing(unittest.TestCase):
    """
    BirDayBer's GUI testing.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize the GUI and adds some people to be tested.
        """
        cls.interface = BirDayBer.Birdayber("testing//BirDayBer.db")

        cls.interface.add_person({
            "country": {"country": "Argentina"},
            "gender": {"gender": "Male"},
            "photo": {"photo": 'testing//image_test.png'},
            "birth": {"birth": "2003-07-15"},
            "person": {"per_first": "Severus", "per_last": "Snape"}})
        cls.interface.add_person({
            "country": {"country": "United States"},
            "gender": {"gender": "Male"},
            "photo": {"photo": None},
            "birth": {"birth": "1919-12-23"},
            "person": {"per_first": "Randolph", "per_last": "Carter"}})

    @classmethod
    def tearDownClass(cls):
        """
        Finish the process of the GUI and deletes all tested people.
        """
        cls.interface.close_client()
        cls.interface.drop_database()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reset_db(self):
        data = ((
            (1, 'Severus', 'Snape', '2003-07-15', 'Argentina', 'Male'),
            (2, 'Randolph', 'Carter', '1919-12-23', 'United States', 'Male')
        ))

        self.assertEqual(self.interface.get_people(binary=False), data)
        self.interface.reset_database()
        self.assertEqual(self.interface.get_people(binary=False), ())

    def test_window_resize(self):
        window_data = self.interface.main_window_resolution(1920, 1080)
        self.assertEqual(window_data, "1440x810+256+135")

    def test_people(self):
        all_people = self.interface.get_people(binary=False)

        self.assertEqual(all_people, (
            (1, "Severus", "Snape", "2003-07-15", "Argentina", "Male"),
            (2, "Randolph", "Carter", "1919-12-23", "United States", "Male")))

    def test_default_images(self):
        for image in (
            "about.png", "user-white.png", "github.png", "close-button.png",
            "image-not-found.png", "garbage1.png", "garbage2.png",
            "twitter.png", "license.png", "maximize-button.png",
            "maximized-button.png", "BirDayBerIcon.png",
            "randolph.png", "minimize-button.png", "party-hat-female.png",
            "party-hat-male.png", "user-black-1.png", "user-black-2.png",
            "nut.png", "party-randolph.png", "edit.png", "radiobutton-0.png",
                "radiobutton-1.png", "accept.png", "clear.png"):

            self.assertTrue(os.path.exists(
                "bin//system-content//visual-content//%s" % image))

    def test_responsive_images(self):
        self.interface.responsive_imgs()
        for image in (
            "about.png", "user-white.png", "github.png", "close-button.png",
            "image-not-found.png", "garbage1.png", "garbage2.png",
            "twitter.png", "license.png", "maximize-button.png",
            "maximized-button.png", "BirDayBerIcon.png",
            "randolph.png", "minimize-button.png", "party-hat-female.png",
            "party-hat-male.png", "user-black-1.png", "user-black-2.png",
            "nut.png", "party-randolph.png", "edit.png", "radiobutton-0.png",
                "radiobutton-1.png", "accept.png", "clear.png"):

            img = "bin//system-content//visual-content//responsive//%s" % image
            self.assertTrue(os.path.exists(img))
            os.remove(img)

    def test_window_focus(self):
        root = self.interface.root

        self.assertEqual(root.tk.eval(f"wm stackorder {root}"), ". .!toplevel")
        self.interface.title_bar_minimize()
        self.assertEqual(root.tk.eval(f"wm stackorder {root}"), ".!toplevel")
        self.interface.root.deiconify()
        self.assertEqual(root.tk.eval(f"wm stackorder {root}"), ".!toplevel .")


if __name__ == "__main__":
    unittest.main()
