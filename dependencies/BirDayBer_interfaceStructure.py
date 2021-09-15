import dependencies.BirDayBer_setUp as BirDayBer_setUp
from tkinter import ttk
from pygame import mixer
import tkinter as tk


def src_image(image):
    return tk.PhotoImage(
        file=f"bin//system-content//visual-content//responsive//{image}")


def titlebar_button(master, img, background, activebackground="#1e5061"):
    return tk.Button(
        master, image=img, relief="flat", bd=0,
        activebackground=activebackground, bg=background)


def adder_entry(master, width, textvariable):
    return tk.Entry(
        master, relief="flat", bg="#517684", insertbackground="#d7f5ff",
        width=round(width * 0.01), selectbackground="#4a92ab",
        textvariable=textvariable, fg="#d1d1d1",
        font=("Century Gothic", round(width * 0.0093)))


def mid_entry(master, width, font, screen, textvar=None, style=""):
    return tk.Entry(
        master, relief="flat", width=round(screen * width), justify="center",
        font=("Century Gothic", round(screen * font), style), fg="#212121",
        textvariable=textvar, selectbackground="#778954", bg="#ffffff",
        insertbackground="#798a5a", disabledbackground="#ffffff",
        disabledforeground="#212121", cursor="arrow", state="disabled")


def edit_button(master, img, command=None):
    return tk.Button(
        master, image=img, bd=0, bg="#ffffff", cursor="hand2",
        activebackground="#ffffff", command=command)


def settings_label(master, width, height, text, row):
    underscore = tk.Frame(master, bg="#267b9d")
    underscore.grid(
        row=row, column=0, padx=(width * 0.05, 0),
        pady=height * 0.03, sticky="w")

    return tk.Label(
        underscore, font=("Century Gothic", round(width / 60)),
        text=text, bg="#475d66", fg="#e3e3e3")


def check_button(master, image1, image2, width, boolean, command=None):
    return tk.Checkbutton(
        master, image=image1, selectimage=image2, indicator=False,
        bd=0, variable=boolean, bg="#475d66", command=command,
        activebackground="#475d66", selectcolor="#475d66")


class Interface_structure(BirDayBer_setUp.Birdayber_setUp):
    """
    This class generates the frames (background) and labels
    for the user interactivity with the GUI.
    """
    def __init__(self):
        """
        Generation of the left and right side in the main body.
        """
        super().__init__()
        location = "bin//system-content//visual-content//responsive//"

        self.root.config(bg="DarkOliveGreen4")
        self.frame.config(bg="ForestGreen")

        self.left_side = tk.Frame(self.frame, bg="#436169")
        self.right_side = tk.Frame(self.frame, bg="#3B5459")

        # Source images generation
        self.load_images()

        # Generation of the title bar
        self.titlebar_init()

        # Generation of the structure of the body
        self.left_side.pack(side="left", fill="both")
        self.right_side.pack(side="left", fill="both", expand=True)

        self.left_side_structure_top(location)
        self.left_side_structure_mid(location)
        self.left_side_structure_bottom(location)
        self.right_side_structure_top(location)
        self.right_side_structure_mid(location)
        self.right_side_structure_bottom(location)

    def load_images(self):
        self.birdayber_src = src_image("BirDayBerIcon.png")
        self.minimize_src = src_image("minimize-button.png")
        self.maximize_src = src_image("maximize-button.png")
        self.close_src = src_image("close-button.png")
        self.person_icon_src = src_image("user-white.png")
        self.license_src = src_image("license.png")
        self.male_src = src_image("male.png")
        self.female_src = src_image("female.png")
        self.male_small_src = src_image("male2.png")
        self.female_small_src = src_image("female2.png")
        self.about_src = src_image("about.png")
        self.nut_src = src_image("nut.png")
        self.person_adder_src = src_image("user-black-1.png")
        self.person_default_src = src_image("user-black-2.png")
        self.accept_src = src_image("accept.png")
        self.clear_src = src_image("clear.png")
        self.skull_src = src_image("randolph.png")
        self.skull_party_src = src_image("party-randolph.png")
        self.garbage1_src = src_image("garbage1.png")
        self.garbage2_src = src_image("garbage2.png")
        self.twitter_src = src_image("twitter.png")
        self.github_src = src_image("github.png")
        self.edit_src = src_image("edit.png")
        self.update_src = src_image("update.png")
        self.radio_button_off_src = src_image("radiobutton-0.png")
        self.radio_button_on_src = src_image("radiobutton-1.png")
        self.default_big_img = src_image("image-not-found.png")
        self.check_button0 = src_image("checkButton0.png")
        self.check_button1 = src_image("checkButton1.png")
        self.default_right_img = src_image("default-right-img.png")

    def titlebar_init(self):
        """
        Generation of the new Title Bar and elimination of the previous one.
        """
        self.title_bar = tk.Frame(self.frame, bg="#316477")
        self.title_bar.pack(fill="x")

        self.minimize_button = titlebar_button(
            self.title_bar, self.minimize_src, "#2c5c6d")

        # self.maximize_button = titlebar_button(  # Change later...
        #     self.title_bar, self.maximize_src, "#295360", "#295360")

        self.maximize_button = tk.Label(
            self.title_bar, image=self.maximize_src, relief="flat",
            bd=0, activebackground="#295360", bg="#295360")

        self.close_button = titlebar_button(
            self.title_bar, self.close_src, "#2c5c6d", "#911722")

        self.close_button.pack(side="right", ipadx=14, ipady=7, fill="y")
        self.maximize_button.pack(side="right", ipadx=14, ipady=7, fill="y")
        self.minimize_button.pack(side="right", ipadx=14, ipady=7, fill="y")

        self.icon = tk.Label(
            self.title_bar, image=self.birdayber_src, bg="#316477")
        self.icon.pack(side="left")

        for label in (self.title_bar, self.icon):
            label.bind("<ButtonPress-1>", self.cursor_start_move)
            label.bind("<B1-Motion>", self.window_dragging)

    def prepare_placeholder(self, entry, text, stringvar):
        placeholder = (entry, text, stringvar)

        entry.bind(
            "<FocusOut>", lambda event: self.add_placeholder(*placeholder))
        entry.bind(
            "<FocusIn>", lambda event: self.remove_placeholder(*placeholder))

    def add_placeholder(self, entry, text, stringvar):
        if stringvar.get() == "":
            entry.config(fg="#d1d1d1")
            return stringvar.set(text)

    def remove_placeholder(self, entry, text, stringvar):
        if stringvar.get() == text:
            entry.config(fg="#dddddd")
            return stringvar.set("")

    def left_side_structure_top(self, location):
        """
        Method that generates the base for the top-left appearance of the GUI.
        """
        self.left_top = tk.Frame(self.left_side, bg="#436169")
        self.search_edge = tk.Frame(self.left_top, bg="#2A4248")
        self.search_bg = tk.Frame(self.search_edge, bg="#517684")

        self.title = tk.Label(
            self.left_top, bg="#2e4c53", text="BirDayBer", fg="#e3e3e3",
            font=("Century Gothic", round(self.screen_width / 38)))

        self.person_icon = tk.Label(
            self.search_bg, image=self.person_icon_src, bg="#4d717f")

        self.search = tk.StringVar()
        self.search.set(self.lang["data_text"][4])

        self.browser = tk.Entry(
            self.search_bg, bg="#517684", selectbackground="#4a92ab",
            relief="flat", fg="#d1d1d1", insertbackground="#d7f5ff",
            width=round(self.screen_width / 75), textvariable=self.search,
            font=("Century Gothic", round(self.screen_width / 60)))

        self.prepare_placeholder(
            self.browser, self.lang["data_text"][4], self.search)
        self.left_side_top_packing()

    def left_side_top_packing(self):
        self.left_top.pack()
        self.person_icon.pack(side="left")

        padx = (self.screen_width * 0.0162, 0)
        pady = self.screen_width * 0.015
        self.title.pack(anchor="w", padx=padx, pady=pady)

        padx = (self.screen_width * 0.0162)
        self.search_edge.pack(anchor="w", padx=padx)

        pady = (0, self.screen_height * 0.014)
        padx = (self.screen_width / 100, 0)
        self.search_bg.pack(pady=pady)
        self.browser.pack(side="left", fill="y", padx=padx)

    def left_side_structure_mid(self, location):
        """
        Method that generates the base for the mid-left appearance of the GUI.
        """
        self.left_mid = tk.Frame(self.left_side, bg="#2A4248")

        self.people_over = tk.Label(
            self.left_mid, relief="flat", text=self.lang["data_text"][5],
            font=("Century Gothic", round(self.screen_width / 64)),
            width=round(self.screen_width / 57), bg="#5f99af", fg="#e7e7e7")

        self.people_finder_section()
        self.left_mid.pack(pady=(self.screen_height * 0.017, 0))
        self.people_over.pack(side="top", fill="x")
        self.finder_frame.pack(
            fill="both", expand="yes", pady=(0, self.screen_height * 0.013))

    def people_finder_section(self):
        """
        Method that generates the scroll-able frame.
        The attribute to add widgets inside of it is: 'self.people_finder'.
        """
        self.finder_frame = tk.Frame(self.left_mid, bg="#5d8999")

        self.canvas = tk.Canvas(
            self.finder_frame, bg="#5d8999", width=self.screen_width * 0.29,
            height=self.screen_height * 0.47, highlightthickness=0)
        self.canvas.pack(
            side="left", fill="both", ipadx=self.screen_width * 0.014 / 2)

        self.yscrollbar = tk.Scrollbar(
            self.finder_frame, orient="vertical", command=self.canvas.yview)
        self.yscrollbar.pack(side="right", fill="y")

        self.canvas.config(yscrollcommand=self.yscrollbar.set)
        self.canvas.bind('<Configure>', lambda x: (
            self.canvas.config(scrollregion=self.canvas.bbox("all"))))

        self.people_finder = tk.Frame(self.canvas, bg="#5d8999")
        self.people_finder.bind('<Configure>', lambda x: (
            self.canvas.config(scrollregion=self.canvas.bbox("all"))))

        self.canvas.create_window(
            (0, 0), window=self.people_finder, anchor="nw")

        self.canvas.bind("<Enter>", self.bind_mousewheel)
        self.canvas.bind("<Leave>", self.unbind_mousewheel)

    def bind_mousewheel(self, event):
        if len(self.showed_people) >= 5:
            self.yscrollbar.bind_all("<MouseWheel>", self.mousewheel_scroll)

    def unbind_mousewheel(self, event):
        self.yscrollbar.unbind_all("<MouseWheel>")

    def mousewheel_scroll(self, event):
        """
        Method to move the scrollbar depending on the Mouse Wheel.
        """
        distance = round(-1 * (event.delta / 120))
        self.canvas.yview_scroll(distance, "units")
        self.scrollbar_at_bottom(event)

    def left_side_structure_bottom(self, location):
        """
        Method that generates the base for the bot-left appearance of the GUI.
        """
        self.left_bottom = tk.Frame(self.left_side, bg="#436169")

        self.license_icon = tk.Button(
            self.left_bottom, image=self.license_src, bg="#436169",
            cursor="hand2", bd=0, activebackground="#436169")

        pady = (self.screen_height * 0.004, 0)
        padx = (self.screen_width * 0.0162, 0)
        self.left_bottom.pack(fill="both", ipady=50)
        self.license_icon.pack(side="left", pady=pady, padx=padx)

    def right_side_structure_top(self, location):
        """
        Method that generates the base for the top-right appearance of the GUI.
        """
        self.right_top = tk.Frame(self.right_side, bg="#3B5459")
        self.people_adder_bg = tk.Frame(self.right_top, bg="#367892")

        self.people_adder = tk.Frame(self.people_adder_bg, bg="#668A97")
        bg = "#3B5459"

        self.nut_icon = tk.Button(
            self.right_top, bg=bg, image=self.nut_src,
            activebackground=bg, relief="flat", bd=0, cursor="hand2")
        self.about_icon = tk.Button(
            self.right_top, bg=bg, image=self.about_src,
            activebackground=bg, relief="flat", bd=0, cursor="hand2")

        self.right_top.pack(anchor="ne")

        pady = (self.screen_height * 0.017, 0)
        self.people_adder_bg.pack(pady=pady, side="left")

        padx = self.screen_height * 0.005
        self.people_adder.pack(padx=padx)

        padx = (self.screen_width * 0.1215, self.screen_width * 0.006)
        pady = (self.screen_height * 0.02, 0)
        self.nut_icon.pack(padx=padx, pady=pady, side="top")
        pady = (self.screen_height * 0.03, 0)
        self.about_icon.pack(padx=padx, pady=pady, side="top")

        self.people_adder_left()
        self.people_adder_right()

    def people_adder_placeholders(self):  # Add docs later...
        entries = (
            (
                self.first_name, self.lang["data_text"][0],
                self.add_name_var
                ),
            (
                self.second_name, self.lang["data_text"][1],
                self.add_surname_var
                ),
            (
                self.country, self.lang["data_text"][2],
                self.add_country_var
                ),
            (
                self.birth_date, self.lang["data_text"][3],
                self.add_birth_var
                ))

        for widget in entries:
            self.prepare_placeholder(widget[0], widget[1], widget[2])

    def people_adder_left(self):
        """
        Method that generates the LEFT structure
        (not functionality) to the "self.people_adder" widget.
        """
        self.first_name_edge = tk.Frame(self.people_adder, bg="#1D6F87")
        self.surname_edge = tk.Frame(self.people_adder, bg="#1D6F87")
        self.birth_date_edge = tk.Frame(self.people_adder, bg="#1D6F87")
        self.country_edge = tk.Frame(self.people_adder, bg="#1D6F87")

        self.add_name_var = tk.StringVar()
        self.add_surname_var = tk.StringVar()
        self.add_country_var = tk.StringVar()
        self.add_birth_var = tk.StringVar()

        self.add_name_var.set(self.lang["data_text"][0])
        self.add_surname_var.set(self.lang["data_text"][1])
        self.add_country_var.set(self.lang["data_text"][2])
        self.add_birth_var.set(self.lang["data_text"][3])

        self.first_name = adder_entry(
            self.first_name_edge, self.screen_width, self.add_name_var)
        self.second_name = adder_entry(
            self.surname_edge, self.screen_width, self.add_surname_var)
        self.country = adder_entry(
            self.country_edge, self.screen_width, self.add_country_var)
        self.birth_date = adder_entry(
            self.birth_date_edge, self.screen_width, self.add_birth_var)

        self.root.bind_all("<Button-1>", self.remove_entry_focus)
        self.people_adder_placeholders()

        padx = self.screen_width * 0.01375 + 0.0225
        pady = self.screen_height * 0.019
        self.first_name_edge.grid(row=0, column=0, pady=pady, padx=(padx, 0))
        self.surname_edge.grid(row=1, column=0, pady=pady, padx=(padx, 0))

        padx = self.screen_width * 0.01375 - 0.0225
        self.birth_date_edge.grid(row=0, column=1, pady=pady, padx=padx)
        self.country_edge.grid(row=1, column=1, pady=pady, padx=padx)

    def remove_entry_focus(self, click):
        try:
            return click.widget.focus_set()
        except AttributeError:
            pass

    def people_adder_right(self):
        """
        Method that generates the RIGHT structure
        (not functionality) to the "self.people_adder" widget.
        """
        self.male_icon = tk.Label(
            self.people_adder, image=self.male_src, bg="#668A97")
        self.female_icon = tk.Label(
            self.people_adder, image=self.female_src, bg="#668A97")

        self.gender_selector = tk.IntVar()
        self.male_button = tk.Radiobutton(
            self.people_adder, variable=self.gender_selector, value=1,
            bg="#668A97", activebackground="#668A97", indicator=False,
            image=self.radio_button_off_src, bd=0, selectcolor="#668A97",
            selectimage=self.radio_button_on_src, cursor="hand2")

        self.female_button = tk.Radiobutton(
            self.people_adder, variable=self.gender_selector, value=2,
            bg="#668A97", activebackground="#668A97", indicator=False,
            image=self.radio_button_off_src, bd=0, selectcolor="#668A97",
            selectimage=self.radio_button_on_src, cursor="hand2")

        self.file_selected = ""
        self.img_adder = tk.Button(
            self.people_adder, image=self.person_adder_src, bg="#668A97",
            bd=0, activebackground="#668A97", cursor="hand2")

        self.accept = tk.Button(
            self.people_adder, image=self.accept_src,
            bg="#668A97", activebackground="#668A97", bd=0, cursor="hand2")
        self.clear = tk.Button(
            self.people_adder, image=self.clear_src,
            bg="#668A97", activebackground="#668A97", bd=0, cursor="hand2")

        padx = (0, self.screen_width * 0.01)
        pady = (self.screen_height * 0.031, 0)
        self.male_icon.grid(pady=pady, row=0, column=2)
        self.female_icon.grid(pady=pady, row=0, column=3)
        self.male_button.grid(row=1, column=2, padx=padx)
        self.female_button.grid(row=1, column=3)

        self.img_adder.grid(row=0, column=4, rowspan=2)

        padx = (self.screen_height * 0.01, self.screen_height * 0.01)
        self.accept.grid(padx=padx, row=0, column=5)
        self.clear.grid(padx=padx, row=1, column=5)

        pady = (0, self.screen_height * 0.004)
        self.first_name.pack(pady=pady)
        self.second_name.pack(pady=pady)
        self.birth_date.pack(pady=pady)
        self.country.pack(pady=pady)

    def right_side_structure_mid(self, location):
        """
        Method that generates the base for the mid-right appearance of the GUI.
        """
        self.right_mid = tk.Frame(self.right_side, bg="#aac17b")
        self.right_mid_base()
        self.right_mid_background()

        self.fullname_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.birth_var = tk.StringVar()

        self.fullname_big = mid_entry(
            self.inner_fullname, 0.012, 0.018,
            self.screen_width, self.fullname_var)
        self.country_big = mid_entry(
            self.inner_country, 0.011, 0.014,
            self.screen_width, self.country_var)
        self.age_big = mid_entry(
            self.age_bg, 0.0035, 0.02, self.screen_width, self.age_var)
        self.birth_big = mid_entry(
            self.inner_birth, 0.01, 0.014, self.screen_width,
            self.birth_var, style="bold")

        self.edit_fullname = edit_button(self.inner_fullname, self.edit_src)
        self.edit_country = edit_button(self.inner_country, self.edit_src)
        self.edit_birth = edit_button(self.inner_birth, self.edit_src)

        pady = (self.screen_height * 0.023, 0)
        self.right_mid.pack(anchor="ne", pady=pady)

        self.right_mid_bg_packing()

    def right_mid_background(self):
        """
        The default right-mid background image.
        """
        self.default_bg = tk.Label(
            self.right_mid, image=self.default_right_img, bg="#ffffff", bd=0)

    def right_mid_base(self):
        self.right_bg = tk.Frame(self.right_mid, bg="#ffffff")

        self.fullname_bg = tk.Frame(self.right_bg, bg="#9aa881")
        self.age_bg = tk.Frame(self.right_bg, bg="#838f6b")
        self.country_bg = tk.Frame(self.right_bg, bg="#7e8967")
        self.birth_bg = tk.Frame(self.right_bg, bg="#7a8565")

        self.inner_fullname = tk.Frame(self.fullname_bg, bg="#ffffff")
        self.inner_country = tk.Frame(self.country_bg, bg="#ffffff")
        self.inner_birth = tk.Frame(self.birth_bg, bg="#ffffff")

        self.skull_icon = tk.Label(
            self.right_bg, bg="#ffffff", image=self.skull_src)

        self.gender_small_icon = tk.Label(
            self.right_bg, bg="#ffffff", image=self.male_small_src)

        self.big_photo = tk.Button(
            self.right_bg, image=self.default_big_img,
            bg="#ffffff", bd=0, activebackground="#ffffff", cursor="hand2")

        self.generate_trash_button()

    def right_mid_bg_packing(self):
        pady = (0, self.screen_height * 0.012)
        padx = (self.screen_width * 0.003, 0)
        self.default_bg.pack(fill="both", padx=padx, pady=pady)

    def right_mid_packing(self):
        padx = (self.screen_width * 0.003, 0)
        pady = (0, self.screen_height * 0.012)
        self.right_bg.pack(fill="both", padx=padx, pady=pady)

        pady = (self.screen_height * 0.008, 0)
        padx = (self.screen_width * 0.004, 0)
        self.skull_icon.grid(
            sticky="nw", row=0, column=0, padx=padx, pady=pady)

        pady = (self.screen_height * 0.004, 0)
        padx = (0, self.screen_width * 0.002)
        self.gender_small_icon.grid(
            sticky="ne", row=0, column=3, padx=padx, pady=pady)

        pady = (self.screen_height * 0.007, 0)
        padx = (self.screen_width * 0.0445, self.screen_width * 0.0732)
        self.fullname_bg.grid(
            sticky="w", row=1, column=0, pady=pady, padx=padx)

        pady = (self.screen_height * 0.08, 0)
        self.country_bg.grid(sticky="w", row=3, column=0, pady=pady, padx=padx)

        pady = (self.screen_height * 0.025, 0)
        self.age_bg.grid(sticky="w", row=4, column=0, pady=pady, padx=padx)

        padx = (0, self.screen_width * 0.025)
        self.birth_bg.grid(sticky="ne", row=5, column=2, padx=padx)

        self.big_photo.grid(sticky="ne", rowspan=5, row=0, column=2)

        padx = (self.screen_width * 0.007)
        pady = (0, self.screen_height * 0.013)
        self.trash.grid(sticky="sw", row=6, column=0, padx=padx, pady=pady)

        pady = (0, self.screen_height * 0.008)

        self.inner_fullname.pack(pady=pady)
        self.fullname_big.pack(side="left")
        self.edit_fullname.pack(side="right")

        self.inner_country.pack(pady=pady)
        self.edit_country.pack(side="right")
        self.country_big.pack(side="left")

        self.inner_birth.pack(pady=pady)
        self.birth_big.pack(side="left")
        self.edit_birth.pack(side="right")

        self.age_big.grid(row=0, column=0, pady=pady)

    def generate_trash_button(self):
        """
        Method that defines and configures the 'Trash' button.
        """
        def over_button(event):
            self.trash.config(image=self.garbage2_src)

        def out_button(event):
            self.trash.config(image=self.garbage1_src)

        self.trash = tk.Button(
            self.right_bg, image=self.garbage1_src, activebackground="#ffffff",
            bg="#ffffff", relief="flat", bd=0, cursor="hand2")

        self.trash.bind("<Enter>", over_button)
        self.trash.bind("<Leave>", out_button)

    def right_side_structure_bottom(self, location):
        """
        Method that generates the base for the bot-right appearance of the GUI.
        """
        self.right_bottom = tk.Frame(self.right_side, bg="#3B5459")
        self.birthday_counter_bg = tk.Frame(self.right_bottom, bg="#303c41")

        self.twitter_icon = tk.Button(
            self.right_bottom, bg="#3B5459", image=self.twitter_src, bd=0,
            activebackground="#3B5459", relief="flat", cursor="hand2")

        self.github_icon = tk.Button(
            self.right_bottom, bg="#3B5459", image=self.github_src, bd=0,
            activebackground="#3B5459", relief="flat", cursor="hand2")

        self.birthday_counter = tk.Label(
            self.birthday_counter_bg, text="Today is the birthday of x people",
            font=("Century Gothic", round(self.screen_width * 0.016)),
            fg="#e3e3e3", bg="#303c41")

        self.right_bottom.pack(fill="both")
        padx = (0, self.screen_width * 0.016)
        self.github_icon.pack(padx=padx, side="right")
        self.twitter_icon.pack(padx=padx, side="right")

        padx = (self.screen_width * 0.0545, 0)
        self.birthday_counter_bg.pack(padx=padx, anchor="w")
        self.birthday_counter.pack(ipady=self.screen_height)

    def open_settings(self):
        if self.settings_state:
            return
        mixer.Sound.play(self.settings_se)

        self.settings = tk.Toplevel(bg="#364349")
        self.settings_state = True

        self.settings.resizable(False, False)
        self.settings.iconbitmap(
            "bin//system-content//visual-content//BirDayBerIcon.ico")

        self.settings_window_resolution()
        self.settings_widgets()
        self.settings.protocol("WM_DELETE_WINDOW", self.close_settings)

    def close_settings(self):
        self.settings_state = False
        self.settings.destroy()

    def settings_widgets(self):
        """
        All the widgets inside of the settings window.
        """
        self.settings_bg = tk.Frame(self.settings, bg="#475d66")

        self.settings_sound = settings_label(
            self.settings_bg, self.screen_width,
            self.screen_height, self.lang["settings"][0], row=0)

        self.settings_ask_before_del = settings_label(
            self.settings_bg, self.screen_width,
            self.screen_height, self.lang["settings"][1], row=2)

        self.settings_language = settings_label(
            self.settings_bg, self.screen_width,
            self.screen_height, self.lang["settings"][2], row=4)

        self.settings_remove_people = settings_label(
            self.settings_bg, self.screen_width,
            self.screen_height, self.lang["settings"][3], row=6)

        self.settings_checkButtons()
        self.settings_language_list()
        self.button_delete_people()

        self.settings_bg.pack(fill="both")
        self.settings_sound.pack(pady=(0, self.screen_height * 0.009))
        self.settings_ask_before_del.pack(pady=(0, self.screen_height * 0.009))
        self.settings_language.pack(pady=(0, self.screen_height * 0.009))
        self.settings_remove_people.pack(pady=(0, self.screen_height * 0.009))

    def settings_checkButtons(self):
        self.sound_button = check_button(
            self.settings_bg, self.check_button0, self.check_button1,
            self.screen_width, self.sound_var, self.accept_sound)
        self.ask_before_del_button = check_button(
            self.settings_bg, self.check_button0, self.check_button1,
            self.screen_width, self.ask_before_del_var, self.accept_sound)

        self.sound_button.grid(
            row=1, column=0, padx=(self.screen_width * 0.05, 0),
            pady=(0, self.screen_height * 0.01), sticky="w")
        self.ask_before_del_button.grid(
            row=3, column=0, padx=(self.screen_width * 0.05, 0),
            pady=(0, self.screen_height * 0.01), sticky="w")

    def accept_sound(self):
        mixer.Sound.play(self.accept_se)

    def settings_language_list(self):
        self.languages = ttk.Combobox(
            self.settings_bg, height=2, state="readonly",
            font=("Century Gothic", round(self.screen_width / 75)))
        self.languages["values"] = [
            self.lang["languages"][0], self.lang["languages"][1]]
        self.languages.set(self.lang["current_lang"])

        self.languages.bind("<<ComboboxSelected>>", self.change_language)
        self.languages.grid(
            row=5, column=0, padx=(self.screen_width * 0.05, 0),
            pady=(0, self.screen_height * 0.01), sticky="w")

    def button_delete_people(self):
        self.remove_people = tk.Frame(self.settings_bg, bg="#602020")
        self.delete_button = tk.Button(
            self.remove_people, activebackground="#6d2e2e",
            bg="#863535", activeforeground="#e3e3e3",
            fg="#e3e3e3", relief="flat", text=self.lang["settings"][4],
            font=("Century Gothic", round(self.screen_width / 75)))

        self.remove_people.grid(
            row=7, column=0, padx=(self.screen_width * 0.05, 0),
            pady=(0, self.screen_height * 0.25), sticky="w")

        margins = self.screen_width * 0.002
        self.delete_button.pack(padx=margins, pady=margins)
