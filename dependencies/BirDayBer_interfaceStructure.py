import dependencies.BirDayBer_setUp as BirDayBer_setUp
import tkinter as tk


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

        # Generation of the title bar
        self.titlebar_init()

        location = "bin//system-content//visual-content//responsive//"

        self.root.config(bg="DarkOliveGreen4")
        self.frame.config(bg="ForestGreen")

        self.left_side = tk.Frame(self.frame, bg="#43575f")
        self.right_side = tk.Frame(self.frame, bg="#3b4d54")

        self.left_side.pack(side="left", fill="both")
        self.right_side.pack(side="left", fill="both", expand=True)

        self.person_icon_src = tk.PhotoImage(file=location + "user-white.png")
        self.license_src = tk.PhotoImage(file=location + "license.png")
        self.male_src = tk.PhotoImage(file=location + "male.png")
        self.female_src = tk.PhotoImage(file=location + "female.png")
        self.male_small_src = tk.PhotoImage(file=location + "male2.png")
        self.female_small_src = tk.PhotoImage(file=location + "female2.png")
        self.people_adder_src = tk.PhotoImage(file=location + "add-person.png")
        self.about_src = tk.PhotoImage(file=location + "about.png")
        self.nut_src = tk.PhotoImage(file=location + "nut.png")
        self.img_adder_src = tk.PhotoImage(file=location + "user-black.png")
        self.accept_src = tk.PhotoImage(file=location + "accept.png")
        self.clear_src = tk.PhotoImage(file=location + "clear.png")
        self.skull_src = tk.PhotoImage(file=location + "randolph.png")
        self.radio_button_off_src = tk.PhotoImage(
            file=location + "radiobutton-0.png")
        self.radio_button_on_src = tk.PhotoImage(
            file=location + "radiobutton-1.png")

        # Generation of the structure of the body
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
        location = "bin//system-content//visual-content//responsive//"

        self.titlebar_img = []
        for img in ("close-button.png", "maximize-button.png",
                    "minimize-button.png", "BirDayBerIcon.png"):
            self.titlebar_img.append(tk.PhotoImage(file=location + img))

        self.title_bar = tk.Frame(self.frame, bg="#316477")
        self.title_bar.pack(fill="x")

        self.minimize_button = tk.Button(
            self.title_bar, image=self.titlebar_img[2], bg="#2c5c6d", bd=0,
            relief="flat", activebackground="#1e5061",
            command=self.title_bar_minimize)

        self.maximize_button = tk.Button(
            self.title_bar, image=self.titlebar_img[1], bg="#2c5c6d",
            relief="flat", bd=0, activebackground="#1e5061")

        self.close_button = tk.Button(
            self.title_bar, image=self.titlebar_img[0], bg="#2c5c6d", bd=0,
            relief="flat", activebackground="#911722",
            command=self.close_client)

        self.close_button.pack(side="right", ipadx=14, ipady=7, fill="y")
        self.maximize_button.pack(side="right", ipadx=14, ipady=7, fill="y")
        self.minimize_button.pack(side="right", ipadx=14, ipady=7, fill="y")

        self.icon = tk.Label(
            self.title_bar, image=self.titlebar_img[3], bg="#316477")
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

        self.title.pack(
            anchor="w", padx=(self.screen_width * 0.0162, 0),
            pady=self.screen_width * 0.015)

        self.search_edge.pack(
            anchor="w", padx=(self.screen_width * 0.0162))

        self.search_background.pack(pady=(0, self.screen_height * 0.014))

        self.search_entry.pack(
            side="left", fill="y", padx=(self.screen_width / 100, 0))

    def left_side_structure_mid(self, location):
        """
        Method that generates the base for the mid-left appearance of the GUI.
        """
        self.left_mid = tk.Frame(self.left_side, bg="#334248")

        self.people_over = tk.Label(
            self.left_mid, relief="flat", text="People",
            font=("Century Gothic", round(self.screen_width / 64)),
            width=round(self.screen_width / 57), bg="#5f99af", fg="#e7e7e7")

        self.people_finder = tk.Label(
            self.left_mid, bg="#5d8999",
            height=round(self.screen_height / 34))

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

        self.left_bottom.pack(fill="both", ipady=50)
        self.license_icon.pack(
            side="left", pady=(self.screen_height * 0.012, 0),
            padx=(self.screen_width * 0.0162, 0))

    def right_side_structure_top(self, location):
        """
        Method that generates the base for the top-right appearance of the GUI.
        """
        self.right_top = tk.Frame(self.right_side, bg="#3b4d54")
        self.people_adder_bg = tk.Frame(self.right_top, bg="#367892")

        self.people_adder = tk.Label(
            self.people_adder_bg, bg="#66838e",
            width=round(self.screen_width / 20),
            height=round(self.screen_height / 108.5))

        bg = "#3b4d54"
        self.people_adder_icon = tk.Label(
            self.right_top, bg=bg, image=self.people_adder_src)
        self.nut_icon = tk.Button(
            self.right_top, bg=bg, image=self.nut_src,
            activebackground=bg, relief="flat", bd=0, cursor="hand2")
        self.about_icon = tk.Button(
            self.right_top, bg=bg, image=self.about_src,
            activebackground=bg, relief="flat", bd=0, cursor="hand2")

        padx = (self.screen_width * 0.0518, 0)
        pady = (self.screen_height * 0.03, 0)
        self.right_top.pack(anchor="ne")
        self.people_adder_bg.pack(padx=padx, pady=pady, side="left")
        self.people_adder.pack(padx=self.screen_height * 0.005)

        pady = (self.screen_height * 0.132, 0)
        self.people_adder_icon.pack(pady=pady, side="left")

        padx = (self.screen_width * 0.085, 0)
        pady = (self.screen_height * 0.032, 0)
        self.nut_icon.pack(padx=padx, pady=pady, side="top")
        pady = (self.screen_height * 0.046, 0)
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
            width=round(self.screen_width * 0.01), font=font_config)

        self.second_name = tk.Entry(
            self.second_name_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config)

        self.birth_date = tk.Entry(
            self.birth_date_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config)

        self.country = tk.Entry(
            self.country_edge, relief="flat", bg="#517684", fg="#e3e3e3",
            width=round(self.screen_width * 0.01), font=font_config)

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

        self.skull_icon = tk.Label(
            self.right_bg, bg="#fdfff5", image=self.skull_src)

        self.male_small_icon = tk.Label(
            self.right_bg, bg="#fdfff5", image=self.male_small_src)
        self.female_small_icon = tk.Label(
            self.right_bg, bg="#fdfff5", image=self.female_small_src)

        pady = (self.screen_height * 0.028, 0)
        self.right_mid.pack(side="right", anchor="ne", pady=pady)
        self.right_bg.pack(fill="both")

        self.skull_icon.pack(side="left", anchor="nw")
        self.male_small_icon.pack(side="right", anchor="ne")
        # self.female_small_icon.pack(side="right", anchor="ne")

    def right_side_structure_bottom(self, location):
        """
        Method that generates the base for the bop-right appearance of the GUI.
        """
        pass
