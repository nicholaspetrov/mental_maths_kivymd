from random import randrange, randint
from loguru import logger
import sys
import operator


logger.remove()
# logger.add(sys.stderr, level="DEBUG")
logger.add(sys.stderr, level="ERROR")


class Test:
    difficulties = {
        'Easy': [(1, 1), (2, 1), (1, 2)],
        'Medium': [(2, 2), (3, 1), (1, 3)],
        'Hard': [(3, 2), (3, 3), (2, 3)]
    }
    questions = []
    user_results = []
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }

    def __init__(self, user_id, difficulty, duration, question_operator):
        self.user_id = user_id
        self.difficulty = difficulty
        self.duration = duration
        self.question_operator = question_operator
        self.number_q = None
        self.number_correct_a = None

    def set_test_results(self, number_q, number_correct_a):
        self.number_q = number_q
        self.number_correct_a = number_correct_a

    def _random_with_n_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        logger.debug(f'{range_start}, {range_end}')
        return randint(range_start, range_end)

    def get_next_question(self):
        digits = self.difficulties[self.difficulty]
        i = randrange(len(digits))
        item = digits[i]

        def get_2_operands(numbers):
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
                operand_1, operand_2 = get_2_operands(item)
                if operand_1 % operand_2 == 0:
                    operand_found = True
        else:
            operand_1, operand_2 = get_2_operands(item)

        logger.info(f'Next {self.difficulty} question for user {self.user_id}: {operand_1} {self.question_operator} {operand_2}')
        self.questions.append((operand_1, operand_2))

        return operand_1, self.question_operator, operand_2

    def check_answer(self, res):
        question_to_check = self.questions[-1]
        # https://stackoverflow.com/questions/1740726/turn-string-into-operator
        correct_answer = self.ops[self.question_operator](question_to_check[0], question_to_check[1])
        if res == correct_answer:
            self.user_results.append(True)
        else:
            self.user_results.append(False)

    def calculate_score(self):
        # TODO: Implement this method...
        pass


# for diff in ['Easy', 'Medium', 'Hard']:
#     for op in ['+', '-', '/', '*']:
#         for i in range(10):
#             test = Test('2', diff, 120, op)
#             test.get_next_question()

if __name__ == '__main__':
    test = Test('2', 'Hard', 120, '/')
    for i in range(4):
        result = int(input(f'{test.get_next_question()}: '))
        test.check_answer(result)
    print(test.user_results)



