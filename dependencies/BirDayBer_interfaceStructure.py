import dependencies.BirDayBer_setUp as BirDayBer_setUp
import tkinter as tk


def src_image(image):
    return tk.PhotoImage(
        file=f"bin//system-content//visual-content//responsive//{image}")


def titlebar_button(master, img, activebackground="#1e5061"):
    return tk.Button(
        master, image=img, relief="flat", bd=0,
        activebackground=activebackground, bg="#2c5c6d")


def mid_entry(master, width, font, screen, style=""):
    """
    Function that generates the structure of the right-mid entries.
    """
    return tk.Entry(
        master, relief="flat", width=round(screen * width), fg="#212121",
        font=("Century Gothic", round(screen * font), style), justify="center",
        selectbackground="#778954", insertbackground="#798a5a", bg="#fdfff5")


class Interface_structure(BirDayBer_setUp.Birdayber_setUp):
    """
    This class generates the frames (background) and labels
    for the user interactivity with the GUI.
    """
    def __init__(self, db_connection):
        """
        Generation of the left and right side in the main body.
        """
        super().__init__(db_connection)

        location = "bin//system-content//visual-content//responsive//"

        self.root.config(bg="DarkOliveGreen4")
        self.frame.config(bg="ForestGreen")

        self.left_side = tk.Frame(self.frame, bg="#43575f")
        self.right_side = tk.Frame(self.frame, bg="#3b4d54")

        # Source images generation
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
        self.people_adder_src = src_image("add-person.png")
        self.about_src = src_image("about.png")
        self.nut_src = src_image("nut.png")
        self.img_adder_src = src_image("user-black.png")
        self.accept_src = src_image("accept.png")
        self.clear_src = src_image("clear.png")
        self.skull_src = src_image("randolph.png")
        self.garbage1_src = src_image("garbage1.png")
        self.garbage2_src = src_image("garbage2.png")
        self.twitter_src = src_image("twitter.png")
        self.github_src = src_image("github.png")
        self.edit_src = src_image("edit.png")
        self.radio_button_off_src = src_image("radiobutton-0.png")
        self.radio_button_on_src = src_image("radiobutton-1.png")
        self.img_not_found_src = src_image("image-not-found.png")

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

    def titlebar_init(self):
        """
        Generation of the new Title Bar and elimination of the previous one.
        """
        self.title_bar = tk.Frame(self.frame, bg="#316477")
        self.title_bar.pack(fill="x")

        self.minimize_button = titlebar_button(
            self.title_bar, self.minimize_src)

        self.maximize_button = titlebar_button(
            self.title_bar, self.maximize_src)

        self.close_button = titlebar_button(
            self.title_bar, self.close_src, "#911722")

        self.close_button.pack(side="right", ipadx=14, ipady=7, fill="y")
        self.maximize_button.pack(side="right", ipadx=14, ipady=7, fill="y")
        self.minimize_button.pack(side="right", ipadx=14, ipady=7, fill="y")

        self.icon = tk.Label(
            self.title_bar, image=self.birdayber_src, bg="#316477")
        self.icon.pack(side="left")

        for label in (self.title_bar, self.icon):
            label.bind("<ButtonPress-1>", self.cursor_start_move)
            label.bind("<B1-Motion>", self.window_dragging)

    def left_side_structure_top(self, location):
        """
        Method that generates the base for the top-left appearance of the GUI.
        """
        self.left_top = tk.Frame(self.left_side, bg="#43575f")
        self.search_edge = tk.Frame(self.left_top, bg="#334248")
        self.search_background = tk.Frame(self.search_edge, bg="#517684")

        self.title = tk.Label(
            self.left_top, bg="#334248", text="BirDayBer", fg="#e3e3e3",
            font=("Century Gothic", round(self.screen_width / 38)))

        self.person_icon = tk.Label(
            self.search_background, image=self.person_icon_src, bg="#4d717f")

        self.search_entry = tk.Entry(
            self.search_background, bg="#517684", selectbackground="#4a92ab",
            relief="flat", fg="#e3e3e3", insertbackground="#d7f5ff",
            width=round(self.screen_width / 75),
            font=("Century Gothic", round(self.screen_width / 60)))
        self.search_entry.insert(0, "Search")  # Remove from here later

        self.left_top.pack()
        self.person_icon.pack(side="left")

        padx = (self.screen_width * 0.0162, 0)
        pady = self.screen_width * 0.015
        self.title.pack(anchor="w", padx=padx, pady=pady)

        padx = (self.screen_width * 0.0162)
        self.search_edge.pack(anchor="w", padx=padx)

        pady = (0, self.screen_height * 0.014)
        padx = (self.screen_width / 100, 0)
        self.search_background.pack(pady=pady)
        self.search_entry.pack(side="left", fill="y", padx=padx)

    def left_side_structure_mid(self, location):
        """
        Method that generates the base for the mid-left appearance of the GUI.
        """
        self.left_mid = tk.Frame(self.left_side, bg="#334248")

        self.people_over = tk.Label(
            self.left_mid, relief="flat", text="People",
            font=("Century Gothic", round(self.screen_width / 64)),
            width=round(self.screen_width / 57), bg="#5f99af", fg="#e7e7e7")

        self.people_finder = tk.Frame(
            self.left_mid, bg="#5d8999", height=self.screen_height * 0.47)

        self.left_mid.pack(pady=(self.screen_height * 0.017, 0))
        self.people_over.pack(side="top")

        self.people_finder.pack(fill="x", pady=(0, self.screen_height * 0.013))

    def left_side_structure_bottom(self, location):
        """
        Method that generates the base for the bot-left appearance of the GUI.
        """
        self.left_bottom = tk.Frame(self.left_side, bg="#43575f")

        self.license_icon = tk.Button(
            self.left_bottom, image=self.license_src, bg="#43575f",
            cursor="hand2", bd=0, activebackground="#43575f")

        pady = (self.screen_height * 0.004, 0)
        padx = (self.screen_width * 0.0162, 0)
        self.left_bottom.pack(fill="both", ipady=50)
        self.license_icon.pack(side="left", pady=pady, padx=padx)

    def right_side_structure_top(self, location):
        """
        Method that generates the base for the top-right appearance of the GUI.
        """
        self.right_top = tk.Frame(self.right_side, bg="#3b4d54")
        self.people_adder_bg = tk.Frame(self.right_top, bg="#367892")

        self.people_adder = tk.Frame(self.people_adder_bg, bg="#66838e")
        bg = "#3b4d54"

        self.people_adder_icon = tk.Label(
            self.right_top, bg=bg, image=self.people_adder_src)
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

        pady = (self.screen_height * 0.114, 0)
        self.people_adder_icon.pack(pady=pady, side="left")

        padx = (self.screen_width * 0.075, self.screen_width * 0.006)
        pady = (self.screen_height * 0.02, 0)
        self.nut_icon.pack(padx=padx, pady=pady, side="top")
        pady = (self.screen_height * 0.03, 0)
        self.about_icon.pack(padx=padx, pady=pady, side="top")

        self.people_adder_left()
        self.people_adder_right()

    def people_adder_left(self):
        """
        Method that generates the LEFT structure
        (not functionality) to the "self.people_adder" widget.
        """
        self.first_name_edge = tk.Frame(self.people_adder, bg="#136687")
        self.second_name_edge = tk.Frame(self.people_adder, bg="#136687")
        self.birth_date_edge = tk.Frame(self.people_adder, bg="#136687")
        self.country_edge = tk.Frame(self.people_adder, bg="#136687")

        font_config = ("Century Gothic", round(self.screen_width * 0.0093))

        self.first_name = tk.Entry(
            self.first_name_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config,
            selectbackground="#4a92ab", insertbackground="#d7f5ff")

        self.second_name = tk.Entry(
            self.second_name_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config,
            selectbackground="#4a92ab", insertbackground="#d7f5ff")

        self.birth_date = tk.Entry(
            self.birth_date_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config,
            selectbackground="#4a92ab", insertbackground="#d7f5ff")

        self.country = tk.Entry(
            self.country_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config,
            selectbackground="#4a92ab", insertbackground="#d7f5ff")

        padx = self.screen_width * 0.01375 + 0.0225
        pady = self.screen_height * 0.019
        self.first_name_edge.grid(row=0, column=0, pady=pady, padx=(padx, 0))
        self.second_name_edge.grid(row=1, column=0, pady=pady, padx=(padx, 0))

        padx = self.screen_width * 0.01375 - 0.0225
        self.birth_date_edge.grid(row=0, column=1, pady=pady, padx=padx)
        self.country_edge.grid(row=1, column=1, pady=pady, padx=padx)

    def people_adder_right(self):
        """
        Method that generates the RIGHT structure
        (not functionality) to the "self.people_adder" widget.
        """
        self.male_icon = tk.Label(
            self.people_adder, image=self.male_src, bg="#66838e")
        self.female_icon = tk.Label(
            self.people_adder, image=self.female_src, bg="#66838e")

        self.gender_selector = tk.IntVar()

        self.male_button = tk.Radiobutton(
            self.people_adder, variable=self.gender_selector, value=1,
            bg="#66838e", activebackground="#66838e", indicator=False,
            image=self.radio_button_off_src, bd=0, selectcolor="#66838e",
            selectimage=self.radio_button_on_src, cursor="hand2")

        self.female_button = tk.Radiobutton(
            self.people_adder, variable=self.gender_selector, value=2,
            bg="#66838e", activebackground="#66838e", indicator=False,
            image=self.radio_button_off_src, bd=0, selectcolor="#66838e",
            selectimage=self.radio_button_on_src, cursor="hand2")

        self.img_adder = tk.Button(
            self.people_adder, image=self.img_adder_src, bg="#66838e",
            bd=0, activebackground="#66838e", cursor="hand2")

        self.accept = tk.Button(
            self.people_adder, image=self.accept_src,
            bg="#66838e", activebackground="#66838e", bd=0, cursor="hand2")
        self.clear = tk.Button(
            self.people_adder, image=self.clear_src,
            bg="#66838e", activebackground="#66838e", bd=0, cursor="hand2")

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
        self.right_bg = tk.Frame(self.right_mid, bg="#fdfff5")

        self.full_name_bg = tk.Frame(self.right_bg, bg="#9aa881")
        self.birth_bg = tk.Frame(self.right_bg, bg="#88966c")
        self.age_bg = tk.Frame(self.right_bg, bg="#838f6b")
        self.country_bg = tk.Frame(self.right_bg, bg="#7e8967")
        self.birthday_bg = tk.Frame(self.right_bg, bg="#7a8565")

        self.skull_icon = tk.Label(
            self.right_bg, bg="#fdfff5", image=self.skull_src)

        self.gender_small_icon = tk.Label(
            self.right_bg, bg="#fdfff5", image=self.male_small_src)

        self.full_name_big = mid_entry(
            self.full_name_bg, 0.012, 0.018, self.screen_width)
        self.birth_big = mid_entry(
            self.birth_bg, 0.01, 0.014, self.screen_width)
        self.age_big = mid_entry(
            self.age_bg, 0.0025, 0.02, self.screen_width)
        self.country_big = mid_entry(
            self.country_bg, 0.006, 0.014, self.screen_width)
        self.birthday_big = mid_entry(
            self.birthday_bg, 0.01, 0.014, self.screen_width, "bold")

        self.img_not_found = tk.Label(
            self.right_bg, image=self.img_not_found_src, bg="#fdfff5")
        self.trash_declaration()

        pady = (self.screen_height * 0.023, 0)
        padx = (self.screen_width * 0.003, 0)
        self.right_mid.pack(anchor="ne", pady=pady)

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

        pady = (self.screen_height * 0.007, self.screen_height * 0.045)
        padx = (self.screen_width * 0.0445, self.screen_width * 0.0245)
        self.full_name_bg.grid(
            sticky="w", row=1, column=0, pady=pady, padx=padx)

        pady = (self.screen_height * 0.015, 0)
        self.birth_bg.grid(sticky="w", row=2, column=0, pady=pady, padx=padx)
        self.age_bg.grid(sticky="e", row=3, column=1, pady=pady)
        self.country_bg.grid(sticky="w", row=4, column=0, padx=padx)

        padx = (0, self.screen_width * 0.024)
        self.birthday_bg.grid(sticky="ne", row=5, column=2, padx=padx)
        self.img_not_found.grid(sticky="ne", rowspan=5, row=0, column=2)

        padx = (self.screen_width * 0.007)
        pady = (0, self.screen_height * 0.013)
        self.trash.grid(sticky="sw", row=6, column=0, padx=padx, pady=pady)

        pady = (0, self.screen_height * 0.008)
        self.full_name_big.pack(pady=pady)
        self.birth_big.pack(pady=pady)
        self.age_big.pack(pady=pady)
        self.country_big.pack(pady=pady)
        self.birthday_big.pack(pady=pady)

        self.full_name_big.insert(0, "Name SurName")  # Remove from here later
        self.birth_big.insert(0, "Birth Date")  # Remove from here later
        self.age_big.insert(0, "Age")  # Remove from here later
        self.country_big.insert(0, "Country")  # Remove from here later
        self.birthday_big.insert(0, "BirthDay")  # Remove from here later

    def trash_declaration(self):
        """
        Method that defines and configures the 'Trash' button.
        """
        def over_button(event):
            self.trash.config(image=self.garbage2_src)

        def out_button(event):
            self.trash.config(image=self.garbage1_src)

        self.trash = tk.Button(
            self.right_bg, image=self.garbage1_src, activebackground="#fdfff5",
            bg="#fdfff5", relief="flat", bd=0, cursor="hand2")

        self.trash.bind("<Enter>", over_button)
        self.trash.bind("<Leave>", out_button)

    def right_side_structure_bottom(self, location):
        """
        Method that generates the base for the bot-right appearance of the GUI.
        """
        self.right_bottom = tk.Frame(self.right_side, bg="#3b4d54")
        self.today_birthdays_bg = tk.Frame(self.right_bottom, bg="#303c41")

        self.twitter_icon = tk.Button(
            self.right_bottom, bg="#3b4d54", image=self.twitter_src, bd=0,
            activebackground="#3b4d54", relief="flat", cursor="hand2")

        self.github_icon = tk.Button(
            self.right_bottom, bg="#3b4d54", image=self.github_src, bd=0,
            activebackground="#3b4d54", relief="flat", cursor="hand2")

        self.today_birthdays = tk.Label(
            self.today_birthdays_bg, text="Today is the birthday of x people",
            fg="#e3e3e3", bg="#303c41", width=round(self.screen_width * 0.018),
            font=("Century Gothic", round(self.screen_width * 0.016)))

        self.right_bottom.pack(fill="both")
        padx = (0, self.screen_width * 0.016)
        self.github_icon.pack(padx=padx, side="right")
        self.twitter_icon.pack(padx=padx, side="right")

        padx = (self.screen_width * 0.051, 0)
        self.today_birthdays_bg.pack(padx=padx, anchor="w")
        self.today_birthdays.pack(ipady=self.screen_height)
