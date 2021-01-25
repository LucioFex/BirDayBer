import db_manager
import tkinter as tk


class Birdayber_client:

    def __init__(self, db_name):
        """
        Creation of the database and window preview configuration.
        """
        self.db = db_manager.Db_manager(db_name)
        self.window = tk.Tk()

        #  Window size and posotion definition
        self.window.geometry(self.window_resolution())
        self.window.mainloop()

    def window_resolution(self):
        """
        This method returns the information of the best
        possible resolution and position for the client's window.
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        print(screen_width)
        print(screen_height)
        screen_width = screen_width - round(screen_width / 4)
        screen_height = screen_height - round(screen_height / 4)

        x_position = round(screen_width / 6.3)
        y_position = round(screen_height / 7)
        print(x_position)

        return "%sx%s+%s+%s" % (
            screen_width, screen_height, x_position, y_position)


if __name__ == '__main__':
    BirDayBer = Birdayber_client("bin/BirDayBer_db")
