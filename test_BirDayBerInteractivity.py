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
        pass

    def tearDown(self):
        pass
