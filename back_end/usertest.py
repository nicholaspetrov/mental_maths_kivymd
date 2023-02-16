from random import randrange, randint
from loguru import logger
import sys
import operator


# logger.remove()
# logger.add(sys.stderr, level="DEBUG")
# logger.add(sys.stderr, level="ERROR")


class UserTest:
    difficulties = {
        'Easy': [(1, 1), (2, 1), (1, 2)],
        'Medium': [(2, 2), (3, 1), (1, 3)],
        'Hard': [(3, 2), (3, 3), (2, 3)],
        'Mixed': ['Easy', 'Medium', 'Hard']
    }
    questions = []
    user_results = []
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }
    scores = {
        'Easy': 1,
        'Medium': 2,
        'Hard': 3
    }
    score = 0
    test_id = 0
    time_created = ''

    def __init__(self, user_id, difficulty, duration, question_operator):
        self.user_id = user_id
        self.difficulty = difficulty
        self.duration = duration
        self.question_operator = question_operator
        self.mixed_mode = False
        if self.difficulty == 'Mixed':
            self.mixed_mode = True

    def _random_with_n_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        logger.debug(f'{range_start}, {range_end}')
        return randint(range_start, range_end)

    def _get_next_mixed_difficulty(self, current_difficulty):
        pos = self.difficulties['Mixed'].index(current_difficulty)
        if pos == len(self.difficulties['Mixed'])-1:
            return self.difficulties['Mixed'][0]
        else:
            return self.difficulties['Mixed'][pos+1]

    def get_next_question(self):
        # Randomly select tuple of digit numbers based on given difficulty
        if self.mixed_mode:
            if len(self.user_results) == 0:
                self.difficulty = 'Easy'
            else:
                self.difficulty = self._get_next_mixed_difficulty(self.user_results[-1][0])

        digits = self.difficulties[self.difficulty]
        pos = randrange(len(digits))
        item = digits[pos]

        def _get_2_operands(numbers):
            op_1, op_2 = (1, 1)
            while op_1 == op_2 or (op_1 == 1 or op_2 == 1) or (op_1, op_2) in self.questions:
                op_1 = self._random_with_n_digits(numbers[0])
                op_2 = self._random_with_n_digits(numbers[1])
            return op_1, op_2

        operand_1, operand_2 = (1, 1)

        if self.question_operator == '/':
            if item[0] < item[1]:
                item = (item[1], item[0])
            operand_found = False
            while not operand_found:
                operand_1, operand_2 = _get_2_operands(item)
                if operand_1 % operand_2 == 0:
                    operand_found = True
        else:
            operand_1, operand_2 = _get_2_operands(item)

        logger.info(f'Next {self.difficulty} question for user {self.user_id}: {operand_1} {self.question_operator} {operand_2}')
        self.questions.append((operand_1, operand_2))

        return operand_1, self.question_operator, operand_2

    def check_answer(self, res):
        if res == 0:
            self.user_results.append((self.difficulty, res))
            return
        question_to_check = self.questions[-1]
        # https://stackoverflow.com/questions/1740726/turn-string-into-operator
        correct_answer = self.ops[self.question_operator](question_to_check[0], question_to_check[1])
        if res == correct_answer:
            self.user_results.append((self.difficulty, self.scores[self.difficulty]))
        else:
            self.user_results.append((self.difficulty, -1 * self.scores[self.difficulty]))

    def calculate_score(self):
        for item in self.user_results:
            self.score += item[1]
        logger.info(f'User {self.user_id} has scored {self.score} points')


# for diff in ['Easy', 'Medium', 'Hard']:
#     for op in ['+', '-', '/', '*']:
#         for i in range(10):
#             test = Test('2', diff, 120, op)
#             test.get_next_question()

if __name__ == '__main__':
    test = UserTest('2', 'Hard', 120, '/')
    for i in range(4):
        result = input(f'{test.get_next_question()}: ')
        test.check_answer(int(result) if len(result) > 0 else 0)
    print(test.user_results)
    test.calculate_score()
    print(test.score)
