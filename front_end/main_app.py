from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty

# from back_end.database_manager import create_password_table
# from back_end.database_manager import insert_into_password_table
# from back_end.database_manager import check_login
# from back_end.database_manager import check_user_exists

from back_end.database_manager import DatabaseManager

from back_end.hashing import password_to_denary


class AppLayout(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbm = DatabaseManager()
        self.dbm.create_tables()
        self.user = None

    def clear_login_fields(self):
        # Method that clears login fields used in several scenarios (i.e. wrong password etc.)
        self.ids['email'].text = ""
        self.ids['password'].text = ""

    def check_data_login(self):

        # Input from text boxes assigned to individual variables
        email = self.ids['email'].text
        password = self.ids['password'].text

        # Making sure all input login fields are filled
        if email == '' and password == '':
            toast("Email and password are required")
            return

        if email == '':
            toast("Email is required ")
            return

        if password == '':
            toast("Password is required")
            return

        # Allows admin to login - privileges to be determined
        if email == "admin" and password == "admin":
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "right"

            self.clear_login_fields()
        else:
            # Checks if email inputted into login field is in database
            if not self.dbm.check_user_exists(email, password):
                # If email not in database (i.e. account not registered under this email)
                self.clear_login_fields()
                toast("Wrong email or password")
            else:
                # TODO: Make self.user = self.dbm.check_login(email, password)
                # Runs inputted password and salt through same hashing algorithm
                if self.dbm.check_login(email, password):
                    # If hash of inputted password and hash of password in table equal
                    self.ids.login_screen_manager.current = "Application"
                    self.ids.app_screen_manager.transition.direction = "right"

                    self.clear_login_fields()
                else:
                    toast("Wrong email or password")

    def clear_register_fields(self):
        self.ids['reg_name'].text = ""
        self.ids['reg_email'].text = ""
        self.ids['reg_password'].text = ""
        self.ids['reg_confirm_password'].text = ""

    def validate_reg(self, name, email, password, confirm_password):

        # Making sure all input login fields are filled
        if name.text == '':
            toast('Name required')
            # Returning nothing prevents user advancing from current page (i.e. user has to check their inputs)
            return

        if email.text == '':
            toast('Email required')
            return

        if password.text == '' or confirm_password.text == '':
            toast('Password(s) required')
            return

        if password.text != confirm_password.text:
            # No toast since message (passwords not the same) is already displayed under textfield dynamically
            return

        if len(password.text) < 6:
            # No toast since message (passwords length less than 6) is already displayed under textfield dynamically
            return

        # Passwords table created in database

        self.user = self.dbm.insert_user(name.text, email.text, password.text)
        # Password fed into hashing algorithm
        if self.user is None:
            # Checks if inputted email has already been used to register
            toast("Account already registered under email")
        else:
            # User has successfully logged in
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "left"
            self.clear_register_fields()


class MainApp(MDApp):
    state = StringProperty("stop")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main_app.kv')

        difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
        difficulty_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in difficulties
        ]
        self.difficulty_menu = MDDropdownMenu(
            caller=self.screen.ids.difficulty_button,
            items=difficulty_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

        types = ['+', '-', '/', '*']
        type_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in types
        ]
        self.type_menu = MDDropdownMenu(
            caller=self.screen.ids.type_button,
            items=type_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

        durations = ['1:00', '2:00', '5:00', '10:00']
        duration_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in durations
        ]
        self.duration_menu = MDDropdownMenu(
            caller=self.screen.ids.duration_button,
            items=duration_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

    test = []

    def menu_callback(self, text_item):
        self.test.append(text_item)
        output = ', '.join(self.test)
        self.screen.ids.test_label.text = output

        self.duration_menu.dismiss()
        self.type_menu.dismiss()
        self.difficulty_menu.dismiss()

    def build(self):
        return self.screen

    # def build(self):
    #     # Loads kv file
    #     return Builder.load_file("main_app.kv")

    def open_menu(self):
        # For side menu
        self.root.ids.nav_drawer.set_state("open")

    def start_test(self):
        toast('Button clicked')
        self.root.ids.progress_bar.start()

    # def on_state(self, instance, value):
        # {
        #     "start": self.root.ids.app_screen_manager.current_screen.ids.progress_bar.start,
        #     "stop": self.root.ids.app_screen_manager.current_screen.ids.progress_bar.stop,
        # }.get(value)()

    def on_menu_click(self, item_name):
        # When item in menu clicked, menu closes
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.app_screen_manager.current = item_name

    def exit_app(self):
        # User redirected to login when top-right exit button clicked
        self.root.ids.login_screen_manager.current = "Login"
        self.root.ids.login_screen_manager.transition.direction = "right"


MainApp().run()

'''
TODO:
- Change TopAppBar title with username or page name when logged in
- "Save db file into backend python package"
- Enable update button once something has been changed in settings page
- Position update button to middle
'''
