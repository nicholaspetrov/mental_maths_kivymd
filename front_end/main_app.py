import re, os, sys
from pathlib import Path

from kivy.metrics import dp, sp
from kivymd.uix.datatables import MDDataTable
from loguru import logger
from kivy.clock import Clock

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

from back_end import utils
from back_end.db.firebase_manager import FirebaseManager
from back_end.merge_sort import run_merge

from back_end.user import User
from back_end.usertest import UserTest

p = Path(__file__).resolve().parent.parent
# print(os.path.dirname(os.path.realpath(__file__).))
# print(p)
sys.path.append(str(p))


class AppLayout(MDBoxLayout):
    email = StringProperty()
    password = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(MDApp):
    test_settings = {}
    user_test = None
    active = True
    user = None
    user_name = StringProperty()
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbm = FirebaseManager()
        self.dbm.create_tables()
        self.user = User('', '')
        Builder.load_file('pages/home.kv')
        Builder.load_file('pages/account.kv')
        Builder.load_file('pages/about.kv')
        Builder.load_file('pages/quiz.kv')
        Builder.load_file('pages/test_results.kv')
        self.screen = Builder.load_file('pages/main_app.kv')

        # For generating dropdown listbox for 3 test parameters (difficulty, duration, operator) on test construction
        # page
        difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
        difficulty_items = [
            {
                "text": difficulty,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'Difficulty: {difficulty}': self.menu_callback('Difficulty', x.split(' ')[1]),
            } for difficulty in difficulties
        ]
        self.difficulty_menu = MDDropdownMenu(
            caller=self.screen.ids.difficulty_button,
            items=difficulty_items,
            position="auto",
            width_mult=2.5,
            max_height=200
        )

        operators = ['Addition +', 'Subtraction -', 'Division /', 'Multiplication *']
        operator_items = [
            {
                "text": operator,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'Operator: {operator}': self.menu_callback_operator('Operator', x.split(' ')[2]),
            } for operator in operators
        ]
        self.operator_menu = MDDropdownMenu(
            caller=self.screen.ids.operator_button,
            items=operator_items,
            position="auto",
            width_mult=2.5,
            max_height=200
        )

        durations = ['1 min', '2 min', '5 min', '10 min']
        duration_items = [
            {
                "text": duration,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'Duration: {duration}': self.menu_callback('Duration', x),
            } for duration in durations
        ]
        self.duration_menu = MDDropdownMenu(
            caller=self.screen.ids.duration_button,
            items=duration_items,
            position="top",
            width_mult=2.5,
            max_height=200
        )

    def reset_test_page(self):
        # Sets page to what it was before test started
        self.root.ids.app_screen_manager.screens[3].ids.user_test_progress_bar.stop()
        self.root.ids.app_screen_manager.screens[3].ids.question_label.text = "Click 'Next question' to start"
        self.root.ids.app_screen_manager.screens[3].ids.question_label.font_style = 'H4'
        self.root.ids.app_screen_manager.screens[3].ids.answer_input.text = ''
        self.root.ids.app_screen_manager.screens[3].ids.correct_progress_bar.value = 0
        self.root.ids.app_screen_manager.screens[3].ids.incorrect_progress_bar.value = 0
        self.root.ids.app_screen_manager.screens[3].ids.question_label.bold = False
        # self.active = False

    def reset_dropdown(self):
        self.test_settings = {}
        self.screen.ids.difficulty_button.set_item('Difficulty')
        self.screen.ids.operator_button.set_item('Operator')
        self.screen.ids.duration_button.set_item('Duration')

    # def plot_graph(self):

    def stop_user_test(self, dt):
        self.reset_test_page()
        total_possible_points = 0
        correct_answers = 0
        logger.debug('Stopping the test')
        self.active = False
        self.root.ids.app_screen_manager.current = 'Test_results'
        self.user_test.calculate_score()
        # User's score is calculated
        for result in self.user_test.user_results:
            if result[1] > 0:
                correct_answers += 1
            if result[0] == 'Easy':
                total_possible_points += 1
            elif result[0] == 'Medium':
                total_possible_points += 2
            else:
                total_possible_points += 3
        # Total points that the user could have scored is calculated as well as the points they actually scored

        questions_answered = len(self.user_test.user_results)

        time = '{:g}'.format(int(self.test_settings["Duration"])/60)
        # Formats 60s, 120s, etc. into 1 min, 2 min etc.
        number_of_seconds = int(self.test_settings['Duration'])
        # Used for calculating speed
        # https://stackoverflow.com/questions/13097099/how-to-make-python-print-1-as-opposed-to-1-0

        self.root.ids.app_screen_manager.screens[4].ids.difficulty_label.text = self.test_settings['Difficulty']
        self.root.ids.app_screen_manager.screens[4].ids.operator_label.text = self.test_settings['Operator']
        self.root.ids.app_screen_manager.screens[4].ids.duration_label.text = f'{time} min'
        # Displaying what the settings of the test that just finished were
        speed = round((self.user_test.score / number_of_seconds) * 60, 2)
        # Speed = points scored by User per minute

        # If not questions were answered
        if questions_answered == 0:
            self.root.ids.app_screen_manager.screens[4].ids.correct_answers_label.text = '0'
            self.root.ids.app_screen_manager.screens[4].ids.speed_label.text = '0'
            self.root.ids.app_screen_manager.screens[4].ids.score_label.text = '0'
        else:
            # If user got a negative score (since questions are subtractive if answered incorrectly)
            if self.user_test.score < 0 or self.user_test.score == 0:
                self.user_test.score = 0
                speed = 0
                self.root.ids.app_screen_manager.screens[4].ids.score_label.text = '0'
                self.root.ids.app_screen_manager.screens[4].ids.correct_answers_label.text = '0'
                self.root.ids.app_screen_manager.screens[4].ids.speed_label.text = '0'
            else:
                # Speed, points scored out of total possible, correct out of total questions calculated
                self.root.ids.app_screen_manager.screens[4].ids.score_label.text = f'{str(self.user_test.score)}/{str(total_possible_points)}'
                self.root.ids.app_screen_manager.screens[4].ids.correct_answers_label.text = f'{correct_answers}/{questions_answered}'
                self.root.ids.app_screen_manager.screens[4].ids.speed_label.text = f'{str(speed)} points per minute'

        user_test = UserTest(
            user_id=self.user.email,
            difficulty=self.test_settings['Difficulty'],
            duration=f'{time} min',
            question_operator=self.test_settings['Operator']
        )
        user_test.set_test_results(
            total_score=total_possible_points,
            user_score=self.user_test.score,
            speed=speed,
            number_correct=correct_answers,
            number_incorrect=questions_answered - correct_answers
        )
        # Test is submitted in tests collection under the User's userid (i.e. email)
        self.dbm.insert_user_test(user_test)

        test_history = self.dbm.get_user_tests_for_operator(email=self.user.email, operator=self.test_settings['Operator'])
        dates = [utils.get_date_string_for_datetime(user_test.time_created) for user_test in test_history]
        # x = timestamps of when the operator-specific test was taken
        y = [user_test.speed for user_test in test_history]
        x = []
        for i in range(1, len(dates) + 1):
            x.append(i)
        # y = speeds that the user was answering the questions correctly at

        # Graph is plotted in the test results page
        fix, ax = plt.subplots()
        ax.bar(x, y)
        plt.ylabel('Points per minute')
        plt.xticks(rotation=20, ha="right")
        plt.xlabel("Date", labelpad=40)
        plt.tight_layout()
        toast('Please maximise screen to view graph fully')
        self.root.ids.app_screen_manager.screens[4].ids.graph_card.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        # Leaderboard is updated (for new user entry/possible overtake)
        self.update_leaderboard()

    def menu_callback(self, param_name, param_value):
        # For the duration and difficulty dropdown listboxes
        if param_name == 'Duration':
            self.test_settings[param_name] = int(param_value.split(' ')[1])*60
            self.screen.ids.duration_button.set_item(param_value)
            self.duration_menu.dismiss()
        else:
            self.test_settings[param_name] = param_value
            if param_name == 'Difficulty':
                self.screen.ids.difficulty_button.set_item(f'Difficulty: {param_value}')
                self.difficulty_menu.dismiss()

        print(self.test_settings)

    def menu_callback_operator(self, param_name, param_value):
        # Listbox label set to what was selected by user
        self.root.ids.history_graph.clear_widgets()
        self.test_settings[param_name] = param_value
        self.screen.ids.operator_button.set_item(f'Operator: {param_value}')
        self.operator_menu.dismiss()

        # When specific operator is selected, graph is generated showing historical performances on that specific
        # operator
        test_history = self.dbm.get_user_tests_for_operator(email=self.user.email, operator=param_value)
        dates = [utils.get_date_string_for_datetime(user_test.time_created) for user_test in test_history]
        y = [user_test.speed for user_test in test_history]
        x = []
        for i in range(1, len(dates)+1):
            x.append(i)
        # Instead of dates (unlike graph in results page), x-axis is attempt number

        fix, ax = plt.subplots()
        ax.bar(x, y)
        plt.ylabel('Points per minute')
        plt.xticks(rotation=20, ha="right")
        plt.xlabel("Attempt no.", labelpad=40)
        plt.tight_layout()
        toast('Please maximise screen to view graph fully')
        self.root.ids.history_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        # Graph is plotted below 3 dropdown listboxes in test construction page once operator is selected

    def build(self):
        return self.screen

    def open_menu(self):
        # For side menu
        self.root.ids.nav_drawer.set_state("open")

    def refocus_ti(self, *args):
        # Maintains focus on answer input box - user doesn't have to constantly click on box to answer with mouse
        # (inconvenient)
        self.root.ids.app_screen_manager.screens[3].ids.answer_input.focus = True

    def get_next_question(self):
        # User now able to type answer into text box
        self.root.ids.app_screen_manager.screens[3].ids.answer_input.disabled = False
        if len(self.user_test.questions) > 0:
            # If this isn't the first question asked
            answer = self.root.ids.app_screen_manager.screens[3].ids.answer_input.text
            # Answer retrieved from text box
            if answer.lstrip("-").isdigit() or answer == '':
                # Validates answer input - prevents strings of letters from being inputted whilst allowing negative sign
                logger.debug(f'Storing answer: {answer}')
                # If nothing is entered (i.e. question skipped), 0 is added to result
                self.user_test.check_answer(int(answer) if len(answer) > 0 else 0)
            else:
                toast('Invalid answer')
                self.root.ids.app_screen_manager.screens[3].ids.answer_input.text = ''
                return
        else:
            # Label that displays question now made bold and increases in size
            self.root.ids.app_screen_manager.screens[3].ids.question_label.font_style = 'H3'
            self.root.ids.app_screen_manager.screens[3].ids.question_label.bold = True
            # Sets the duration of the horizontal timer progress bar on top of screen based on what was inputted in the
            # prior test construction page
            self.root.ids.app_screen_manager.screens[3].ids.user_test_progress_bar.running_duration = self.test_settings['Duration']
            # self.root.ids.app_screen_manager.screens[3].ids.user_test_progress_bar.running_duration = 10
            # Timer + progress bar started
            self.root.ids.app_screen_manager.screens[3].ids.user_test_progress_bar.start()
            Clock.schedule_once(self.stop_user_test, self.user_test.duration)
            # Clock.schedule_once(self.stop_user_test, 10)

        # Values for points gained or lost after answering the question correctly or incorrectly stored - later used for
        # displaying green and red progress bars
        current_correct = self.root.ids.app_screen_manager.screens[3].ids.correct_progress_bar.value
        current_incorrect = self.root.ids.app_screen_manager.screens[3].ids.incorrect_progress_bar.value
        if len(self.user_test.questions) > 0:
            if self.user_test.user_results[-1][1] > 0:
                # If points scored are positive, then question has been answered correctly (back in class UserTest)
                current_correct += self.user_test.user_results[-1][1]
                # Green progress bar increases accordingly by how many points was just gained
                self.root.ids.app_screen_manager.screens[3].ids.correct_progress_bar.value = current_correct
            else:
                if self.user_test.user_results[-1][1] == 0:
                    # If nothing was inputted (i.e. User has skipped question) - no points lost or gained
                    pass
                else:
                    # Red progress bar increases accordingly by how many points was just lost
                    current_incorrect += -(self.user_test.user_results[-1][1])
                    self.root.ids.app_screen_manager.screens[3].ids.incorrect_progress_bar.value = current_incorrect
        else:
            pass

        # If either progress bar fills completely, progress bar resets
        if current_correct >= 100:
            self.root.ids.app_screen_manager.screens[3].ids.correct_progress_bar.value = 0
        if current_incorrect >= 100:
            self.root.ids.app_screen_manager.screens[3].ids.incorrect_progress_bar.value = 0

        # After user submitted answer, text in input box emptied
        self.root.ids.app_screen_manager.screens[3].ids.answer_input.text = ''
        # Next question retrieved using same very method
        question = self.user_test.get_next_question()
        # Keeps focus on enter button - User essentially never has to use the mouse (just type answer and enter, then repeat)
        Clock.schedule_once(self.refocus_ti)
        logger.debug(f'Generating next question: {question}')
        # Tuple (question) replaces the "Click 'Next question' to start" in visually appealing format
        self.root.ids.app_screen_manager.screens[3].ids.question_label.text = ' '.join(map(str, question))

    def clear_leaderboards(self):
        # Clears the leaderboards since if this doesn't take place, the graphs will generate in the same layout -
        # eventually, the graphs become cluttered and uninterpretable
        self.root.ids.app_screen_manager.screens[0].ids.addition_table.clear_widgets()
        self.root.ids.app_screen_manager.screens[0].ids.subtraction_table.clear_widgets()
        self.root.ids.app_screen_manager.screens[0].ids.division_table.clear_widgets()
        self.root.ids.app_screen_manager.screens[0].ids.multiplication_table.clear_widgets()

    def start_new_test(self):
        toast('Good luck!')
        self.reset_test_page()
        self.root.ids.app_screen_manager.screens[3].ids.answer_input.disabled = True
        # Prevents user from typing into enter box - enabled once test has officially started
        self.root.ids.app_screen_manager.screens[3].ids.question_label.font_style = 'H4'
        self.root.ids.app_screen_manager.screens[3].ids.user_test_progress_bar.value = 0

        if len(self.test_settings) < 3:
            # Making sure all test settings has been filled in
            toast('Please fill in all required fields')
            return
        else:
            logger.debug(f'Starting new test: {self.test_settings}')
            # UserTest object created based on the inputs used as attributes
            self.user_test = UserTest(
                user_id=1,
                difficulty=self.test_settings['Difficulty'],
                duration=self.test_settings['Duration'],
                question_operator=self.test_settings['Operator']
            )
            # Resets what questions were asked and results - when test is restarted/new one made and tried
            self.user_test.questions = []
            self.user_test.user_results = []

            # Directs user to actual quiz page
            self.root.ids.app_screen_manager.current = "Quiz"
            self.root.ids.app_screen_manager.transition.direction = "right"
            self.root.ids.app_screen_manager.screens[4].ids.graph_card.clear_widgets()
            self.clear_leaderboards()

    def update_leaderboard(self):
        # Each of the 4 leaderboards created
        addition_leaderboard = self.dbm.get_leaderboard(operator='+')
        subtraction_leaderboard = self.dbm.get_leaderboard(operator='-')
        division_leaderboard = self.dbm.get_leaderboard(operator='/')
        multiplication_leaderboard = self.dbm.get_leaderboard(operator='*')

        # print(run_merge(addition_leaderboard))
        addition_table = MDDataTable(
            column_data=[
                ("", sp(3)),
                ("Name", sp(15)),
                ("Speed", sp(15))
            ],
            # Merge sort ran on the speeds achieved by the users - sorts them in descending order
            row_data=run_merge(addition_leaderboard)
        )

        subtraction_table = MDDataTable(
            column_data=[
                ("", sp(3)),
                ("Name", sp(15)),
                ("Speed", sp(15))
            ],
            row_data=run_merge(subtraction_leaderboard)
        )

        division_table = MDDataTable(
            column_data=[
                ("", sp(3)),
                ("Name", sp(15)),
                ("Speed", sp(15))
            ],
            row_data=run_merge(division_leaderboard)
        )

        multiplication_table = MDDataTable(
            column_data=[
                ("", sp(3)),
                ("Name", sp(15)),
                ("Speed", sp(15))
            ],
            row_data=run_merge(multiplication_leaderboard)
        )

        # The 4 leaderboards added to their corresponding card in the Home page
        self.root.ids.app_screen_manager.screens[0].ids.addition_table.add_widget(addition_table)
        self.root.ids.app_screen_manager.screens[0].ids.subtraction_table.add_widget(subtraction_table)
        self.root.ids.app_screen_manager.screens[0].ids.division_table.add_widget(division_table)
        self.root.ids.app_screen_manager.screens[0].ids.multiplication_table.add_widget(multiplication_table)

    def on_menu_click(self, item_name):
        # When item in menu clicked, menu closes
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.app_screen_manager.current = item_name

    def exit_app(self):
        # User redirected to login when top-right exit button clicked
        self.user = None
        self.root.ids.login_screen_manager.current = "Login"
        self.root.ids.login_screen_manager.transition.direction = "right"
        self.reset_test_page()
        self.reset_dropdown()
        self.root.ids.history_graph.clear_widgets()
        self.clear_leaderboards()

    def clear_register_fields(self):
        # Empties all input fields
        self.root.ids.reg_name.text = ""
        self.root.ids.reg_email.text = ""
        self.root.ids.reg_password.text = ""
        self.root.ids.reg_confirm_password.text = ""

    def register(self, name, email, password, confirm_password):

        # Making sure all input login fields are filled
        if name.text == '':
            toast('Name required')
            # Returning nothing prevents user advancing from current page (i.e. user has to check their inputs)
            return

        if email.text == '':
            toast('Email required')
            return

        if not re.fullmatch(self.regex, email.text):
            # Regular expression used to make sure email is in a correct format e.g. text@text.com
            toast('Invalid email')
            self.root.ids.reg_email.text = ""
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

        user = self.dbm.insert_user(name.text, email.text, password.text)
        # Password fed into hashing algorithm
        if user is not None:
            # User has successfully logged in
            self.user = user
            self.root.ids.login_screen_manager.current = "Application"
            self.root.ids.app_screen_manager.transition.direction = "left"
            self.user_name = self.user.name
            self.update_leaderboard()
            self.clear_register_fields()
        else:
            # Checks if inputted email has already been used to register
            toast("Email already registered")

    def clear_login_fields(self):
        # Method that clears login fields used in several scenarios (i.e. wrong password etc.)
        self.root.ids.email.text = ""
        self.root.ids.password.text = ""

    def login(self):

        # Input from text boxes assigned to individual variables
        email = self.root.ids.email.text
        password = self.root.ids.password.text

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
            self.user = User('admin', 'admin')
            self.root.ids.login_screen_manager.current = "Application"
            self.root.ids.app_screen_manager.transition.direction = "right"
            self.user_name = 'admin'
            self.clear_login_fields()
        else:
            # Runs inputted password and salt through same hashing algorithm
            self.user = self.dbm.check_login(email, password)

            if self.user is not None:
                # If hash of inputted password and hash of password in table equal
                self.root.ids.login_screen_manager.current = "Application"
                self.root.ids.app_screen_manager.current = "Home"
                self.root.ids.app_screen_manager.transition.direction = "right"
                self.user_name = self.user.name
                self.update_leaderboard()
                self.clear_login_fields()
            else:
                toast("Wrong email or password")
                self.clear_login_fields()

    def settings(self):
        # Old password retrieved and fed into hashing algorithm to check that the password inputted is correct
        old_password = self.root.ids.app_screen_manager.screens[1].ids.old_password.text
        new_password = self.root.ids.app_screen_manager.screens[1].ids.new_password.text
        confirm_new_password = self.root.ids.app_screen_manager.screens[1].ids.confirm_new_password.text
        check_password = self.dbm.check_password(self.user.email, old_password)
        if old_password == '' or new_password == '' or confirm_new_password == '':
            toast('Password(s) required')
            return
        if new_password != confirm_new_password:
            return
        if len(new_password) < 6 or len(confirm_new_password) < 6:
            return
        else:
            if check_password:
                # Password is reset only if current password is correct
                self.dbm.reset_password(self.user.email, new_password)
                toast('Password successfully updated')
                self.root.ids.app_screen_manager.current = "Home"
                self.root.ids.app_screen_manager.screens[1].ids.old_password.text = ''
                self.root.ids.app_screen_manager.screens[1].ids.new_password.text = ''
                self.root.ids.app_screen_manager.screens[1].ids.confirm_new_password.text = ''
            else:
                toast('Incorrect password')
                self.root.ids.app_screen_manager.screens[1].ids.old_password.text = ''

    def hide_show_password_login(self):
        # Hides/show password while also changing the icon of the button
        if self.root.ids.password.password:
            self.root.ids.hide_button.icon = 'eye-outline'
            self.root.ids.password.password = False
        else:
            self.root.ids.hide_button.icon = 'eye-off-outline'
            self.root.ids.password.password = True

    def hide_show_password_settings(self):
        # Hides/show password while also changing the icon of the button
        if self.root.ids.app_screen_manager.screens[1].ids.old_password.password:
            self.root.ids.app_screen_manager.screens[1].ids.hide_button.icon = 'eye-outline'
            self.root.ids.app_screen_manager.screens[1].ids.old_password.password = False
        else:
            self.root.ids.app_screen_manager.screens[1].ids.hide_button.icon = 'eye-off-outline'
            self.root.ids.app_screen_manager.screens[1].ids.old_password.password = True


MainApp().run()

'''
TODO:
- Enable update button once something has been changed in settings page
- Animation for switching screens
- https://stackoverflow.com/questions/44617793/image-size-on-kivy example of background picture
- fix exiting app before test ends
'''