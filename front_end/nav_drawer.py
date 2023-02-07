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
        self.ids['email'].text = ""
        self.ids['password'].text = ""

    def check_data_login(self):

        email = self.ids['email'].text
        password = self.ids['password'].text

        if email == '' and password == '':
            toast("Email and password are required")
            return

        if email == '':
            toast("Email is required ")
            return

        if password == '':
            toast("Password is required")
            return

        if email == "admin" and password == "admin":
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "right"

            self.clear_login_fields()
        else:
            if not check_user_exists(email, password):
                toast("Wrong email or password")
            else:
                if check_login(email, password):
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

    def validate_reg(self, name, email, password):

        print(f"Name: {name.text}, Email: {email.text}, Password: {password.text}")
        create_password_table()

        salt, hash_password = password_to_denary(password.text)
        if insert_into_password_table(email.text, salt, hash_password):
            toast("Account already registered under email")
        else:
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "left"
            self.clear_register_fields()


class NavDrawer(MDApp):

    def build(self):
        return Builder.load_file("nav_drawer.kv")

    def open_menu(self):
        self.root.ids.nav_drawer.set_state("open")

    def on_menu_click(self, item_name):
        # toast(f"You clicked on {item_name}")
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.app_screen_manager.current = item_name

    def exit_app(self):
        self.root.ids.login_screen_manager.current = "Login"
        self.root.ids.login_screen_manager.transition.direction = "right"


NavDrawer().run()

'''
TODO:
- Feed accessed salt and RUN IT THROUGH HASHING algorithm with inputted password to see if same hash is given 
letting user log in
- Change TopAppBar title with username when logged in
- "Save db file into backend python package"
'''
