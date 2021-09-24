import dependencies.BirDayBer_DB as BirDayBer_DB
from PIL import (Image, ImageOps, ImageTk)
from pystray import MenuItem as item
from base64 import b64decode
from ctypes import windll
from io import BytesIO
import tkinter as tk
import pystray
import json
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
        self.prepare_resized_widgets_dict()

        self.screen_width = self.sizes["window-size"][0]
        self.screen_height = self.sizes["window-size"][1]

        self.x_position = round(width / 7.5)
        self.y_position = round(height / 8)

        return (
            f"{self.screen_width}x{self.screen_height}+" +
            f"{self.x_position}+{self.y_position}")

    def settings_window_resolution(self):
        """
        This method provides the toplevel of a geometry and position.
        """
        self.settings_width = self.sizes["window-size"][2]
        self.settings_height = self.sizes["window-size"][3]

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

        with open("bin//resolution.json", "r", encoding="utf-8") as json_file:
            self.sizes = json.load(json_file)

        if (width, height) >= (1680, 1050):
            self.sizes = self.sizes[">=1680x1050"]
        elif (width, height) >= (1440, 900):
            self.sizes = self.sizes[">=1440x900"]
        elif (width, height) < (1440, 900):
            self.sizes = self.sizes["<1440x900"]

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
                responsive_img.thumbnail(
                    (self.sizes["src-width"][0], self.sizes["src-height"][0]))
            # Title bar section
            elif img in ("BirDayBerIcon.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][1], self.sizes["src-height"][1]))
            # Main entry section
            elif img in ("user-white.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][2], self.sizes["src-height"][2]))
            # Footer section
            elif img in ("license.png", "privacy-policy.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][3], self.sizes["src-height"][3]))
            # People adder's icon
            elif img in ("add-person.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][4], self.sizes["src-height"][4]))
            # Extra buttons in the right-top section
            elif img in ("nut.png", "about.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][5], self.sizes["src-height"][5]))
            # Gender radio buttons.
            elif img in ("radiobutton-0.png", "radiobutton-1.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][6], self.sizes["src-height"][6]))
            # Accept and clear buttons of the people_adder widget
            elif img in ("accept.png", "clear.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][7], self.sizes["src-height"][7]))
            # Skull icon
            elif img in ("randolph.png", "party-randolph.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][8], self.sizes["src-height"][8]))
            # Garbage icons
            elif img in ("garbage1.png", "garbage2.png"):
                responsive_img.thumbnail(
                    (self.sizes["src-width"][9], self.sizes["src-height"][9]))
            # Image adder icon
            elif img in ("user-black-1.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][10], self.sizes["src-height"][10]))
            # Person default icon
            elif img in ("user-black-2.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][11], self.sizes["src-height"][11]))
            # Image not found (user base image)
            elif img in ("image-not-found.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][12], self.sizes["src-height"][12]))
            # Twitter & GitHub icon
            elif img in ("twitter.png", "github.png", "linkedin.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][13], self.sizes["src-height"][13]))
            # Edit icon
            elif img in ("edit.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][14], self.sizes["src-height"][14]))
            # Update button icon
            elif img in ("update.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][15], self.sizes["src-height"][15]))
            # Default right-mid background
            elif img in ("default-right-img.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][16], self.sizes["src-height"][16]))
            # Settings-checkbutton icons
            elif img in ("checkButton0.png", "checkButton1.png"):
                responsive_img.thumbnail((
                    self.sizes["src-width"][17], self.sizes["src-height"][17]))

            # Gender icons
            elif img in ("male.png", "female.png"):
                # Small icons
                responsive_img.thumbnail((
                    self.sizes["src-width"][18], self.sizes["src-height"][18]))
                responsive_img.save("%s//responsive//%s" % (
                    location, img.replace(".png", "2.png")))
                responsive_img.close()

                # Big icons
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    self.sizes["src-width"][19], self.sizes["src-height"][19]))

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
