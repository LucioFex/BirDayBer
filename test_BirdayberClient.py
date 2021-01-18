import unittest
import BirDayBer


class Birth_testing(unittest.TestCase):
    """
    BirDayBer graphical user interface testing.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the GUI.
        """
        cls.bir_interface = BirDayBer.Birdayber_main()
        cls.bir_interface.init_interface()

    @classmethod
    def tearDownClass(cls):
        """
        Finish the process of the GUI.
        """
        cls.bir_interface.close_interface()

    def setUp(self):
        pass

    def tearDown(self):
        pass
