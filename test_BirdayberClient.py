import unittest
import BirDayBer
import os
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
        cls.interface = BirDayBer.Birdayber_client("testing//BirDayBer.db")

        cls.interface.add_person({
            "countries": {"country": "Argentina"},
            "genders": {"gender": "Male"},
            "photos": {"photo": 'testing//image_test.png'},
            "births": {"birth": "2003-07-15"},
            "people": {"per_first": "Severus", "per_last": "Snape"}})
        cls.interface.add_person({
            "countries": {"country": "United States"},
            "genders": {"gender": "Male"},
            "photos": {"photo": None},
            "births": {"birth": "1919-12-23"},
            "people": {"per_first": "Randolph", "per_last": "Carter"}})

    @classmethod
    def tearDownClass(cls):
        """
        Finish the process of the GUI and deletes all tested people.
        """
        # people_id = cls.interface.get_people()
        # for person in people_id:
        #     cls.interface.delete_person(person[0])

        cls.interface.close_client()
        cls.interface.drop_database()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_window_size(self):
        position = self.interface.window_init_resolution()

        self.assertNotEqual(position, "1x1+0+0")
        self.assertIsInstance(position, str)

    def test_people(self):
        all_people = self.interface.get_people("&None%", False)

        self.assertEqual(all_people, (
            (
                "Severus", "Snape", "2003-07-15",
                None, "Argentina", "Male"),
            (
                "Randolph", "Carter", "1919-12-23",
                None, "United States", "Male")))

    def test_license(self):
        license_data = self.interface.get_license()
        self.assertEqual(
            license_data,
            ("MIT License", "Copyright (c) 2020-2021 Luciano Esteban"))

    def test_default_images(self):
        for image in (
            "about.png", "add_person.png", "nut.png", "BirDayBerIcon.png",
            "cancel_person.png", "close-button.png", "edit.png",
            "garbage1.png", "garbage2.png", "twitter.png", "license.png",
            "maximize-button.png", "maximized-button.png",
            "minimize-button.png", "party_hat_female.png", "github.png",
                "party_hat_male.png", "party_randolph.png", "randolph.png"):

            self.assertTrue(os.path.exists(
                "bin//system_content//visual_content//%s" % image))

    def test_responsive_images(self):
        self.interface.responsive_imgs()
        for image in (
            "about.png", "add_person.png", "nut.png", "BirDayBerIcon.png",
            "cancel_person.png", "close-button.png", "edit.png",
            "garbage1.png", "garbage2.png", "twitter.png", "license.png",
            "maximize-button.png", "maximized-button.png",
            "minimize-button.png", "party_hat_female.png", "github.png",
                "party_hat_male.png", "party_randolph.png", "randolph.png"):

            img = "bin//system_content//visual_content//responsive//%s" % image
            self.assertTrue(os.path.exists(img))
            os.remove(img)


if __name__ == "__main__":
    unittest.main()
