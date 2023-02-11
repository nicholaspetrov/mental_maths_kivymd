from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast

from back_end.database_creation import create_password_table
from back_end.database_creation import insert_into_password_table
from back_end.database_creation import check_login
from back_end.database_creation import check_user_exists

from back_end.hashing import password_to_denary


class AppLayout(MDBoxLayout):

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
            if not check_user_exists(email, password):
                # If email not in database (i.e. account not registered under this email)
                self.clear_login_fields()
                toast("Wrong email or password")
            else:
                # Runs inputted password and salt through same hashing algorithm
                if check_login(email, password):
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
        create_password_table()

        # Password fed into hashing algorithm
        salt, hash_password = password_to_denary(password.text)
        if insert_into_password_table(email.text, salt, hash_password):
            # Checks if inputted email has already been used to register
            toast("Account already registered under email")
        else:
            # User has successfully logged in
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "left"
            self.clear_register_fields()


class NavDrawer(MDApp):

    def build(self):
        # Loads kv file
        return Builder.load_file("nav_drawer.kv")

    def open_menu(self):
        # For side menu
        self.root.ids.nav_drawer.set_state("open")

    def on_menu_click(self, item_name):
        # When item in menu clicked, menu closes
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.app_screen_manager.current = item_name

    def exit_app(self):
        # User redirected to login when top-right exit button clicked
        self.root.ids.login_screen_manager.current = "Login"
        self.root.ids.login_screen_manager.transition.direction = "right"


class Test:
    def __init__(self):
        pass


class User:
    def __init__(self, acd, lts):
        self.AccountCreationDate = acd
        self.LoginTimeStamps = lts


    def attach_test(self, __test):
        self.__test = __test

    def get_test(self) -> Test:
        return self.__test


u = User("", "")
u.attach_test(Test())

u.get_test()


NavDrawer().run()

'''
TODO:
- Change TopAppBar title with username or page name when logged in
- "Save db file into backend python package"
- Enable update button once something has been changed in settings page
- Position update button to middle
'''
