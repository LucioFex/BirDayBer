import dependencies.BirDayBer_DB as BirDayBer_DB
from PIL import (Image, ImageOps, ImageTk)
from pystray import MenuItem as item
from base64 import b64decode
from ctypes import windll
from io import BytesIO
import tkinter as tk
import pystray
import os


def decode_db_photo(img):
    img = img[
        img.find(b"<plain_txt_msg:img>") + len(b"<plain_txt_msg:img>"):
        img.find(b"<!plain_txt_msg>")]

    img = b64decode(img)
    buf = BytesIO(img)

    photo = Image.open(buf)
    return photo


class Birdayber_setUp(BirDayBer_DB.Birdayber_database):
    """
    This class is specialized in the generation of the GUI.
    """
    def __init__(self):
        super().__init__()
        # Deletion of the original Title Bar
        self.root.overrideredirect(1)

        # Sets the window screen resolution
        geometry = self.main_window_resolution(
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight())
        self.root.geometry(geometry)

        # Generation of new responsive images
        self.responsive_imgs()

        # Generation of the main frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both")

        # Attribute to check if the app is a Stray icon or not
        self.stray_icon_state = False

        # Implementation of actions for when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.close_client)

        # Visual brand modifications
        self.root.title("BirDayBer")
        self.root.iconbitmap(
            "bin//system-content//visual-content//BirDayBerIcon.ico")

    def set_appwindow(self):
        """
        Method to make the window discoverable by the task manager.
        """
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080

        hwnd = windll.user32.GetParent(self.root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

        # re-assert the new window style
        self.root.wm_withdraw()
        self.root.after(10, lambda: self.root.wm_deiconify())

    def main_window_resolution(self, width, height):
        """
        This method provides the main window of a geometry and position.
        """
        self.screen_width = 1440
        self.screen_height = 810

        self.x_position = round(width / 7.5)
        self.y_position = round(height / 8)

        self.prepare_resized_widgets_dict()
        return (
            f"{self.screen_width}x{self.screen_height}+" +
            f"{self.x_position}+{self.y_position}")

    def settings_window_resolution(self):
        """
        This method provides the toplevel of a geometry and position.
        """
        self.settings_width = round(
            self.root.winfo_screenwidth() * 0.252 + 192)
        self.settings_height = round(
            self.root.winfo_screenheight() * 0.434 + 216)

        self.x_settings_position = round(self.root.winfo_screenwidth() / 3)
        self.y_settings_position = round(self.root.winfo_screenheight() / 5.5)

        self.settings.geometry(
            f"{self.settings_width}x{self.settings_height}+" +
            f"{self.x_settings_position}+{self.y_settings_position}")

    def prepare_resized_widgets_dict(self):
        """
        Method to improve the widgets resizement depending on the screen size
        """
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        if (width, height) >= (1600, 900):
            self.sizes = {
                "title-bar": (14, 7),
                "left-top": (38, 19, 24, 23.328, 21.6, 11.34, 14.4),
                "left-mid": (22, 25, 13.77, 10.53, 417.6, 380.7, 10.08),
                "left-bot": (3.24, 23.328, 7.2, 50),
                "right-top": (
                    13.77, 4.05, 174.96, 8.64, 16.2,
                    24.3, 14.4, 25.11, 8.1, 3.24),
                "right-mid": (4.32, 9.72, 6.48, 5.76, 3.24, 2.88, 18.63),
                "right-bot": (23, 78.48, 810),
                "adder-entry": (14, 13, 19.8225, 15.39, 19.777),
                "mid-entry": ((17, 26), (16, 20), (5, 29), (14, 20), 6.48),
                "settings": (72, 24, 7.29, 8.1, 19, 202.5, 2.88),
                "mid-border": (5.67, 64.08, 105.408, 20.25, 36, 10.08, 10.53)
            }

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
            return self.lang["license"][0], self.lang["license"][1]

    def get_version(self):
        """
        Method that returns the current version of the project
        """
        try:
            def check_version(file):
                if "### `Version: " in file:
                    return file

            with open("README.md", "r", encoding="utf-8") as readme:
                version = filter(check_version, readme.readlines())
                return next(version)[5: -2]

        except FileNotFoundError:
            return self.lang["version"]

    def thumbnail_size(self, width, height):
        """Thumbnail img size calculation"""
        return self.screen_width * width, self.screen_height * height

    def responsive_imgs(self):  # Refactor later...
        """
        Method that modifies all the sizes of images and clone these in the
        BirDayBer's system to something more visible for the user.
        The new clones will be saved in the 'responsive' folder.
        """
        location = "bin//system-content//visual-content"
        files = next(os.walk(location))[2]  # All the images names

        for img in files:
            responsive_img = Image.open("%s//%s" % (location, img))

            # Title bar section
            if img in (
                "close-button.png", "minimize-button.png",
                    "maximize-button.png", "maximized-button.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.04, 0.04))
            # Title bar section
            elif img in ("BirDayBerIcon.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.065, 0.065))
            # Main entry section
            elif img in ("user-white.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.07, 0.09))
            # Footer section
            elif img in ("license.png", "privacy-policy.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.07, 0.08))
            # People adder's icon
            elif img in ("add-person.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.075, 0.087))
            # Extra buttons in the right-top section
            elif img in ("nut.png", "about.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.056, 0.069))
            # Gender radio buttons.
            elif img in ("radiobutton-0.png", "radiobutton-1.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.015, 0.0255))
            # Accept and clear buttons of the people_adder widget
            elif img in ("accept.png", "clear.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.040, 0.059))
            # Skull icon
            elif img in ("randolph.png", "party-randolph.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.051, 0.073))
            # Garbage icons
            elif img in ("garbage1.png", "garbage2.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.1, 0.1))
            # Image adder icon
            elif img in ("user-black-1.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.056, 0.24))
            # Person default icon
            elif img in ("user-black-2.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.05, 0.2))
            # Image not found (user base image)
            elif img in ("image-not-found.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.37, 0.37))
            # Twitter & GitHub icon
            elif img in ("twitter.png", "github.png", "linkedin.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.041, 0.073))
            # Edit icon
            elif img in ("edit.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.028, 0.028))
            # Update button icon
            elif img in ("update.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.028, 0.028))
            # Default right-mid background
            elif img in ("default-right-img.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.596, 0.596))
            # Settings-checkbutton icons
            elif img in ("checkButton0.png", "checkButton1.png"):
                responsive_img.thumbnail(self.thumbnail_size(0.066, 0.065))

            # Gender icons
            elif img in ("male.png", "female.png"):
                # Small icons
                responsive_img.thumbnail(self.thumbnail_size(0.021, 0.037))
                responsive_img.save("%s//responsive//%s" % (
                    location, img.replace(".png", "2.png")))
                responsive_img.close()

                # Big icons
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail(self.thumbnail_size(0.056, 0.069))

            responsive_img.save("%s//responsive//%s" % (location, img))
            responsive_img.close()

    def circular_img(self, img, mask):
        """
        This method creates a circular image of the given arguments,
        then it saves the image in the 'visual-content' folder if it is
        a system img. If it's a user img, then I saves the img in the DB.
        """
        mask = Image.open(mask).convert("L")

        output_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output_img.putalpha(mask)

        img.close(), mask.close()
        return output_img

    def title_bar_minimize(self):
        """
        This method is a manual way to minimize the window
        with the 'minimize' button of the title bar.
        """
        self.root.withdraw()
        self.root.overrideredirect(0)
        self.root.iconify()
        self.root.update()
        self.root.bind("<FocusIn>", self.window_focus)

    def window_focus(self, event):
        """
        Method that declares if the program (recognized by the task manager)
        is focused or not. Then it will minimize or re-open the window.
        """
        self.root.unbind("<FocusIn>")
        self.root.withdraw()
        self.root.update()

        self.root.overrideredirect(1)
        self.root.deiconify()
        self.root.after(10, self.set_appwindow)

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

    def process_photo(self, photo, default, target):
        """
        Method that process the input photo, to return a circle version
        compatible with tkinter (tk.PhotoImage type).
        """
        if photo is None:
            return default

        photo = decode_db_photo(photo)
        mask = "bin/system-content/visual-content/mask.png"
        photo = self.circular_img(photo, mask)

        if target == "row":
            return self.finder_row_photo(photo)
        elif target == "big":
            return self.big_row_photo(photo)
        elif target == "adder":
            return self.adder_row_photo(photo)

    def finder_row_photo(self, photo):
        """
        Images adapted to the finder_people section.
        """
        photo.thumbnail(self.thumbnail_size(0.05, 0.2))
        self.people_photos.append(ImageTk.PhotoImage(photo))

        photo.close()
        return self.people_photos[-1]

    def big_row_photo(self, photo):
        """
        Images adapted to the right-mid section.
        """
        photo.thumbnail(self.thumbnail_size(0.37, 0.37))
        self.current_big_image = ImageTk.PhotoImage(photo)

        photo.close()
        return self.current_big_image

    def adder_row_photo(self, photo):
        """
        Images adapted to the people_adder section.
        """
        photo.thumbnail(self.thumbnail_size(0.056, 0.24))
        self.current_adder_image = ImageTk.PhotoImage(photo)

        photo.close()
        return self.current_adder_image

    def turn_strayicon_on(self):
        """
        Method to convert the app into a Stray Icon.
        """
        self.stray_icon_state = True
        self.prepare_birthday_notification()

        self.root.withdraw()
        if self.settings_state:
            self.close_settings()

        app_icon = "bin//system-content//visual-content//BirDayBerIcon.ico"
        stray_image = Image.open(app_icon)

        stray_menu = pystray.Menu(
            item(self.lang["stray-icon"][0], self.open_client),
            item(self.lang["stray-icon"][1], self.close_client))

        self.stray_icon = pystray.Icon(
            "name", stray_image, "BirDayBer", stray_menu)

        self.stray_icon.run()

    def open_client(self):
        """
        Method to open the client from the Stray Icon in the TaskBar.
        """
        self.stray_icon_state = False
        self.stray_icon.stop()
        self.root.after(0, lambda: self.root.deiconify())

    def close_client(self):
        """
        It makes the program close the database and stop mainlooping.
        """
        if self.stray_icon_state:
            self.stray_icon.stop()

        self.update_new_configurations()
        self.db.close_database()
        self.root.quit()

        try:
            # This will not affect the flow of the program,
            # because it already has its own cleaning actions performed.
            raise KeyboardInterrupt("Kill the Notification Thread")
        except KeyboardInterrupt:
            return
