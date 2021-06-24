import dependencies.BirDayBer_DB as BirDayBer_DB
from PIL import (Image, ImageOps)
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
        self.main_window_resolution(
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

    def main_window_resolution(self, width, height):
        """
        This method provides the main window of a geometry and position.
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

    def toplevel_window_resolution(self):
        """
        This method provides the toplevel of a geometry and position.
        """
        pass

    def get_license(self):
        """
        This method returns the type of BirDayBer project's license,
        the duration of this one and the name of its creator.
        """
        license_type = []
        try:
            with open("LICENSE", "r", encoding="utf-8") as license_data:
                license_type.append(license_data.readlines()[0][0:-1])
                license_data.seek(0)
                license_type.append(license_data.readlines()[2][0:-1])
            return (" " * 22 + license_type[0], license_type[1])

        except FileNotFoundError:
            return (
                " " * 8 + "License not Found",
                "Problem trying to find the file")

    def get_version(self):
        try:
            def check_version(file):
                if "### `Version: " in file:
                    return file

            with open("README.md", "r", encoding="utf-8") as readme:
                version = filter(check_version, readme.readlines())
                return next(version)[5: -2]

        except FileNotFoundError:
            return "Cannot get version without readme file"

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
            # Extra buttons in the right-top section
            elif img in ("nut.png", "about.png"):
                responsive_img.thumbnail(thumbnail_size(0.056, 0.069))
            # Gender radio buttons.
            elif img in ("radiobutton-0.png", "radiobutton-1.png"):
                responsive_img.thumbnail(thumbnail_size(0.015, 0.0255))
            # Accept and clear buttons of the people_adder widget
            elif img in ("accept.png", "clear.png"):
                responsive_img.thumbnail(thumbnail_size(0.040, 0.059))
            # Skull icon
            elif img in ("randolph.png"):
                responsive_img.thumbnail(thumbnail_size(0.051, 0.073))
            # Garbage icons
            elif img in ("garbage1.png", "garbage2.png"):
                responsive_img.thumbnail(thumbnail_size(0.1, 0.1))
            # Image adder icon (circular)
            elif img in ("user-black.png"):
                responsive_img.thumbnail(thumbnail_size(0.056, 0.24))
            # Image not found (user base image)
            elif img in ("image-not-found.png"):
                responsive_img.thumbnail(thumbnail_size(0.37, 0.37))
            # Twitter icon
            elif img in ("twitter.png"):
                responsive_img.thumbnail(thumbnail_size(0.041, 0.073))
            # GitHub icon
            elif img in ("github.png"):
                responsive_img.thumbnail(thumbnail_size(0.041, 0.073))
            # GitHub icon
            elif img in ("edit.png"):
                responsive_img.thumbnail(thumbnail_size(0.014, 0.014))

            # Gender icons
            elif img in ("male.png", "female.png"):
                # Small icons
                responsive_img.thumbnail(thumbnail_size(0.021, 0.037))
                responsive_img.save("%s//responsive//%s" % (
                    location, img.replace(".png", "2.png")))
                responsive_img.close()

                # Big icons
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail(thumbnail_size(0.056, 0.069))

            responsive_img.save("%s//responsive//%s" % (location, img))
            responsive_img.close()

    def circular_imgs(self, img, mask):
        """
        This method creates a circular image of the given arguments,
        then it saves the image in the 'visual-content' folder if it is
        a system img. If it's a user img, then I saves the img in the DB.
        """
        image = Image.open(img)
        mask = Image.open(mask).convert("L")

        output_img = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        output_img.putalpha(mask)

        img = img.replace(".png", "2.png")
        output_img.save(img)

        image.close(), mask.close()
        return img

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
