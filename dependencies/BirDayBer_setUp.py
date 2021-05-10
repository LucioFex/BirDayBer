import dependencies.BirDayBer_DB as BirDayBer_DB
from PIL import Image
import tkinter as tk
import os


class Birdayber_setUp(BirDayBer_DB.Birdayber_database):
    """
    This class is specialized in the generation of the GUI.
    """
    def __init__(self, db_connection):
        super().__init__(db_connection)

        # Root and Frame - Generation and Configuration:
        self.root = tk.Tk()

        #   Deletion of the original Title Bar
        self.root.overrideredirect(1)
        #   Sets the window screen resolution
        self.window_init_resolution(
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight())
        #   Generation of new responsive images
        self.responsive_imgs()
        #  Generation of the main frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both")

        # Hidden Window - Generation and Configuration:
        self.hidden_window = tk.Toplevel(self.root)

        #   Hide of the top window
        self.hidden_window.geometry("0x0+10000+10000")
        self.hidden_window.attributes("-alpha", 0.0)
        #   Actions for maximizing and minimizing the root from the taskbar
        self.hidden_window.bind("<Unmap>", self.window_focus)
        self.hidden_window.bind("<FocusIn>", self.window_focus)

        # Implementation of actions for when the window is closed
        for widget in (self.root, self.hidden_window):
            widget.protocol("WM_DELETE_WINDOW", self.close_client)

        # Visual brand modifications
        for visual_brand in (self.root, self.hidden_window):
            visual_brand.title("BirDayBer")
            visual_brand.iconbitmap(
                "bin//system-content//visual-content//BirDayBerIcon.ico")

    def window_init_resolution(self, width, height):
        """
        This method returns the information of the best
        possible resolution and position for the client's window.
        Then it sets the new values in the root.geometry() function.
        It also calls the 'responsive_imgs' method to resize the system imgs.
        """

        self.screen_width = width - round(width / 4)
        self.screen_height = height - round(height / 4)

        self.x_position = round(width / 7.5)
        self.y_position = round(height / 8)

        self.root.geometry("%sx%s+%s+%s" % (
            self.screen_width, self.screen_height,
            self.x_position, self.y_position))

        self.root.update()
        return str(self.root.geometry())

    def responsive_imgs(self):
        """
        Method that modifies all the sizes of images and clone these in the
        BirDayBer's system to something more visible for the user.
        The new clones will be saved in the 'responsive' folder.
        """
        location = "bin//system-content//visual-content"
        files = next(os.walk(location))[2]  # All the images names

        def thumbnail_size(width, height):  # Thumbnail size calculation
            return self.screen_width * width, self.screen_height * height

        for img in files:
            responsive_img = Image.open("%s//%s" % (location, img))

            # Title bar section
            if img in (
                "close-button.png", "minimize-button.png",
                    "maximize-button.png", "maximized-button.png"):
                responsive_img.thumbnail(thumbnail_size(0.04, 0.04))
            # Title bar section
            elif img in ("BirDayBerIcon.png"):
                responsive_img.thumbnail(thumbnail_size(0.065, 0.065))
            # Main entry section
            elif img in ("user-white.png"):
                responsive_img.thumbnail(thumbnail_size(0.07, 0.09))
            # Footer section
            elif img in ("license.png"):
                responsive_img.thumbnail(thumbnail_size(0.056, 0.088))
            # People adder's icon
            elif img in ("add-person.png"):
                responsive_img.thumbnail(thumbnail_size(0.075, 0.087))
            # People adder's section and extra buttons
            elif img in ("nut.png", "about.png", "male.png", "female.png"):
                responsive_img.thumbnail(thumbnail_size(0.056, 0.069))
            # Gender radio buttons.
            elif img in ("radiobutton-0.png", "radiobutton-1.png"):
                responsive_img.thumbnail(thumbnail_size(0.015, 0.0255))
            # Image adder icon
            elif img in ("user-black.png"):
                responsive_img.thumbnail(thumbnail_size(0.048, 0.08))

            responsive_img.save("%s//responsive//%s" % (location, img))
            responsive_img.close()

    def title_bar_minimize(self):
        """
        This method is a manual way to minimize the window
        with the 'minimize' button of the title bar.
        """
        self.hidden_window.unbind("<FocusIn>")
        self.root.withdraw()
        self.root.update()
        self.hidden_window.bind("<FocusIn>", self.window_focus)

    def window_focus(self, event):
        """
        Method that declares if the program (recognized by the task manager)
        is focused or not. Then it will minimize or re-open the window.
        """
        self.root.update()
        if event.type == tk.EventType.FocusIn:
            self.root.deiconify()
        elif event.type == tk.EventType.Unmap:
            self.root.withdraw()

    def cursor_start_move(self, event): self.x, self.y = event.x, event.y

    def window_dragging(self, event):
        """
        Changes the position of the window without
        changing the mouse coordinates.

        This method works with the 'cursor_start_move' method.
        """
        cursor_position_x = event.x - self.x
        cursor_position_y = event.y - self.y

        window_position_x = self.root.winfo_x() + cursor_position_x
        window_position_y = self.root.winfo_y() + cursor_position_y

        self.root.geometry("+%s+%s" % (window_position_x, window_position_y))

    def close_client(self):
        """
        It makes the program close the database and stop mainlooping.
        """
        self.db.close_database()
        self.root.quit()
