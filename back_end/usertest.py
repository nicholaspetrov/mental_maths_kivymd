from random import randrange, randint
from loguru import logger
import sys
import operator
from datetime import datetime


class UserTest:
    # For scoring points based on difficulty - (1, 1) means a 1 digit number mathematically operated by another
    # 1 digit number
    difficulties = {
        'Easy': [(1, 1), (2, 1), (1, 2)],
        'Medium': [(2, 2), (3, 1), (1, 3)],
        'Hard': [(3, 2), (3, 3), (2, 3)],
        'Mixed': ['Easy', 'Medium', 'Hard']
    }
    questions = []
    user_results = []
    # Used to convert string of operators into their actual arithmetic operation
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }
    # Used when question answered correctly
    scores = {
        'Easy': 1,
        'Medium': 2,
        'Hard': 3
    }
    # Used when question answered incorrectly
    scores_deducted = {
        'Easy': 3,
        'Medium': 2,
        'Hard': 1
    }
    score = 0
    test_id = ''
    time_created: datetime = None

    def __init__(self, user_id, difficulty, duration, question_operator):
        self.user_id = user_id
        self.difficulty = difficulty
        self.duration = duration
        self.question_operator = question_operator
        self.total_score = None
        self.user_score = None
        self.speed = None
        self.number_incorrect = None
        self.number_correct = None

        self.mixed_mode = False
        if self.difficulty == 'Mixed':
            self.mixed_mode = True

    # Produces a random number, n digits long
    def _random_with_n_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        logger.debug(f'{range_start}, {range_end}')
        return randint(range_start, range_end)

    # If the first question is yet to be asked in Mixed mode, difficulty starts off as Easy and
    # then becomes Medium then Hard and repeats
    def _get_next_mixed_difficulty(self, current_difficulty):
        pos = self.difficulties['Mixed'].index(current_difficulty)
        if pos == len(self.difficulties['Mixed'])-1:
            return self.difficulties['Mixed'][0]
        else:
            return self.difficulties['Mixed'][pos+1]

    def get_next_question(self):
        # When Mixed selected, this method finds what difficulty the next question should be based on the sequence
        # defined in the 4th element of the difficulties dictionary
        if self.mixed_mode:
            if len(self.user_results) == 0:
                self.difficulty = 'Easy'
            else:
                self.difficulty = self._get_next_mixed_difficulty(self.user_results[-1][0])

        # Randomly selects one tuple of digits from list of tuples
        digits = self.difficulties[self.difficulty]
        pos = randrange(len(digits))
        item = digits[pos]
        # item is now tuple of how many digits each number is going to be

        def _get_2_operands(numbers):
            op_1, op_2 = (1, 1)
            # Prevents each operand equaling each other, being 1 or being repeated
            if self.question_operator == '/':
                # Program stops running if on Easy mode and struggles to find any new Easy division questions so
                # repeating questions allowed only in division
                while op_1 == op_2 or (op_1 == 1 or op_2 == 1):
                    op_1 = self._random_with_n_digits(numbers[0])
                    op_2 = self._random_with_n_digits(numbers[1])
                return op_1, op_2
            else:
                while op_1 == op_2 or (op_1 == 1 or op_2 == 1) or (op_1, op_2) in self.questions:
                    op_1 = self._random_with_n_digits(numbers[0])
                    op_2 = self._random_with_n_digits(numbers[1])
                return op_1, op_2

        operand_1, operand_2 = (1, 1)

        if self.question_operator == '/':
            # Integer Division so items in tuple swapped if 2nd one is bigger than 1st
            # since a smaller number divided by a bigger number will always be less than 1 (i.e. not an integer)
            if item[0] < item[1]:
                item = (item[1], item[0])
            operand_found = False
            while not operand_found:
                # Makes sure division returns an integer - slightly more realistic question to be asked in a non-calc
                # admissions assessment
                operand_1, operand_2 = _get_2_operands(item)
                if operand_1 % operand_2 == 0:
                    operand_found = True
        else:
            # In the other 3 (*, +, -), order doesn't matter
            operand_1, operand_2 = _get_2_operands(item)

        logger.info(f'Next {self.difficulty} question for user {self.user_id}: {operand_1} {self.question_operator} {operand_2}')
        # Used to make sure questions aren't repeated
        self.questions.append((operand_1, operand_2))

        return operand_1, self.question_operator, operand_2

    def check_answer(self, res):
        if res == 0:
            self.user_results.append((self.difficulty, res))
            return
        # Last/most recent question asked
        question_to_check = self.questions[-1]
        # https://stackoverflow.com/questions/1740726/turn-string-into-operator
        correct_answer = self.ops[self.question_operator](question_to_check[0], question_to_check[1])
        if res == correct_answer:
            # Corresponding points to difficulty added to user_results when question answered correctly
            self.user_results.append((self.difficulty, self.scores[self.difficulty]))
        else:
            # 'Inverse' relationship between points and difficulty when question answered incorrectly
            self.user_results.append((self.difficulty, -1 * self.scores_deducted[self.difficulty]))

    def calculate_score(self):
        for item in self.user_results:
            self.score += item[1]
        logger.info(f'User {self.user_id} has scored {self.score} points')

    def set_test_results(self, total_score=None, user_score=None, speed=None, number_incorrect=None, number_correct=None, time_created=None):
        self.total_score = total_score
        self.user_score = user_score
        self.speed = speed
        self.number_incorrect = number_incorrect
        self.number_correct = number_correct
        self.time_created = time_created


if __name__ == '__main__':
    test = UserTest('2', 'Hard', 120, '/')
    for i in range(4):
        result = input(f'{test.get_next_question()}: ')
        # If nothing entered, 0 is added
        test.check_answer(int(result) if len(result) > 0 else 0)
    print(test.user_results)
    test.calculate_score()
    print(test.score)
