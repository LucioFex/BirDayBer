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
        data_test = ((
            ('Severus', 'Snape', '2003-07-15', None, 'Argentina', 'Male'),
            ('Randolph', 'Carter', '1919-12-23', None, 'United States', 'Male')
        ))

        self.assertEqual(self.interface.get_people(binary=False), data_test)
        self.interface.reset_database()
        self.assertEqual(self.interface.get_people(binary=False), ())

    def test_window_resize(self):
        window_data = self.interface.main_window_resolution(1920, 1080)
        self.assertEqual(window_data, "1440x810+256+135")

        window_data = self.interface.main_window_resolution(1680, 1050)
        self.assertEqual(window_data, "1260x788+224+131")

        window_data = self.interface.main_window_resolution(1600, 900)
        self.assertEqual(window_data, "1200x675+213+112")

        window_data = self.interface.main_window_resolution(1400, 900)
        self.assertEqual(window_data, "1050x675+187+112")

        window_data = self.interface.main_window_resolution(1366, 768)
        self.assertEqual(window_data, "1024x576+182+96")

        window_data = self.interface.main_window_resolution(1280, 1024)
        self.assertEqual(window_data, "960x768+171+128")

        window_data = self.interface.main_window_resolution(1280, 720)
        self.assertEqual(window_data, "960x540+171+90")

        window_data = self.interface.main_window_resolution(1024, 768)
        self.assertEqual(window_data, "768x576+137+96")

        window_data = self.interface.main_window_resolution(800, 600)
        self.assertEqual(window_data, "600x450+107+75")

    def test_people(self):
        all_people = self.interface.get_people(binary=False)

        self.assertEqual(all_people, (
            (
                "Severus", "Snape", "2003-07-15",
                None, "Argentina", "Male"),
            (
                "Randolph", "Carter", "1919-12-23",
                None, "United States", "Male")))

    def test_default_images(self):
        for image in (
            "about.png", "add-person.png", "nut.png", "BirDayBerIcon.png",
            "cancel-person.png", "close-button.png", "image-not-found.png",
            "garbage1.png", "garbage2.png", "twitter.png", "license.png",
            "maximize-button.png", "maximized-button.png", "github.png",
            "randolph.png", "minimize-button.png", "party-hat-female.png",
            "party-hat-male.png", "user-black.png", "user-white.png",
            "party-randolph.png", "edit.png", "radiobutton-0.png",
                "radiobutton-1.png", "accept.png", "clear.png"):

            self.assertTrue(os.path.exists(
                "bin//system-content//visual-content//%s" % image))

    def test_responsive_images(self):
        self.interface.responsive_imgs()
        for image in (
            "about.png", "add-person.png", "nut.png", "BirDayBerIcon.png",
            "cancel-person.png", "close-button.png", "image-not-found.png",
            "garbage1.png", "garbage2.png", "twitter.png", "license.png",
            "maximize-button.png", "maximized-button.png", "github.png",
            "randolph.png", "minimize-button.png", "party-hat-female.png",
            "party-hat-male.png", "user-black.png", "user-white.png",
            "party-randolph.png", "edit.png", "radiobutton-0.png",
                "radiobutton-1.png", "accept.png", "clear.png"):

            img = "bin//system-content//visual-content//responsive//%s" % image
            self.assertTrue(os.path.exists(img))
            os.remove(img)

    def test_circular_images(self):
        img = "bin//system-content//visual-content//user-black.png"
        mask = "bin//system-content//visual-content//mask.png"
        self.interface.circular_imgs(img, mask)

        img = "bin//system-content//visual-content//user-black2.png"
        self.assertTrue(os.path.exists(img))
        os.remove(img)

    def test_window_focus(self):
        root = self.interface.root

        self.assertEqual(root.tk.eval(f"wm stackorder {root}"), ". .!toplevel")
        self.interface.title_bar_minimize()
        self.assertEqual(root.tk.eval(f"wm stackorder {root}"), ".!toplevel")
        self.interface.root.deiconify()
        self.assertEqual(root.tk.eval(f"wm stackorder {root}"), ".!toplevel .")

    def test_total_children_per_widget(self):
        self.assertEqual(len(self.interface.root.winfo_children()), 2)
        self.assertEqual(len(self.interface.frame.winfo_children()), 3)
        self.assertEqual(len(self.interface.title_bar.winfo_children()), 4)
        self.assertEqual(len(self.interface.left_side.winfo_children()), 3)
        self.assertEqual(len(self.interface.right_side.winfo_children()), 3)
        self.assertEqual(len(self.interface.left_top.winfo_children()), 2)
        self.assertEqual(len(self.interface.left_mid.winfo_children()), 2)
        self.assertEqual(len(self.interface.right_top.winfo_children()), 4)
        self.assertEqual(len(self.interface.right_mid.winfo_children()), 1)
        self.assertEqual(len(self.interface.people_adder.winfo_children()), 11)
        self.assertEqual(len(self.interface.right_bottom.winfo_children()), 3)


if __name__ == "__main__":
    unittest.main()
