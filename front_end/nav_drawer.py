from kivy.lang import Builder

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast

from back_end.user_service import user_login
from back_end.database_creation import create_connection
from back_end.database_creation import insert_into_password_table
import back_end.user_service as user_service


class AppLayout(MDBoxLayout):

    def check_data_login(self):

        username = self.ids['username'].text
        password = self.ids['password'].text
        user_login(username, password)

        if username == '' and password == '':
            toast("Username and password are required")
            return

        if username == '':
            toast("Username is required ")
            return

        if password == '':
            toast("Password is required")
            return

        if username == "admin" and password == "admin":
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "right"

            self.ids['username'].text = ""
            self.ids['password'].text = ""
        else:
            toast("Wrong username or password")

    def validate_reg(self, name, email, password):

        print(f"Name: {name.text}, Email: {email.text}, Password: {password.text}")
        user_service.insert_user(name, email, password)
        self.ids.login_screen_manager.current = "Application"
        self.ids.app_screen_manager.transition.direction = "left"


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
- Insert new user
- Implement hashing algorithm successfully
- Check if user has already registered
- Change TopAppBar title with username when logged in
- Save db file into backend python package
'''
