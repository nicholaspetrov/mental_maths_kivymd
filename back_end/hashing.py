import random

'''
How my hashing algorithm works:
1. Password and salt converted to denary and stored in list value
2. Length of value is checked if even and if not, number 74 added (randomly chosen by programmer)
3. Neighbouring items in value split into pairs
4. Items in each pair XOR'ed against each other
5. Output of each comparison between pair stored in list new
6. Sum of new calculated
7. Random number chosen (last 2 digits of total) to XOR against sum of new outputting hash
8. Hash, salt stored to refer back to for user logging back in
'''


def create_salt():
    salt = ''
    # Random string of ASCII characters of length 4 created and saved to specific user
    for i in range(4):
        number = random.randint(32, 127)
        salt += chr(number)

    return salt


def hashing(value):
    # Checking if len(value) is even - important for later on where items in value are grouped in pairs
    extra = 74
    if len(value) % 2 == 0:
        pass
    else:
        value.append(extra)

    # Grouping every 2 items in list value
    start = 0
    end = len(value)
    step = 2
    xor_comparisons = []
    for i in range(start, end, step):
        comparison = (value[i:i + step])
        xor_comparison = comparison[0] ^ comparison[1]
        xor_comparisons.append(xor_comparison)

    # Number randomly generated to xor against total of numbers in xor_comparisons
    total = str(sum(xor_comparisons))
    random_number = total[len(total) - 2:]

    # Hash generated
    hashed_password = hex(ord(chr(int(total) ^ int(random_number))))
    return hashed_password


def password_to_denary(password):
    value = []
    salt = create_salt()
    # Each character of password converted to denary and stored in list value
    for letter in password:
        number = ord(letter)
        value.append(number)

    # Each character of salt converted to denary and stored in list value
    for letter in salt:
        number = ord(letter)
        value.append(number)

    # print('Password and salt in binary:', value)
    hashed_password = hashing(value)
    return salt, hashed_password


def login(password, salt):
    value = []
    for letter in password:
        number = ord(letter)
        value.append(number)

    for letter in salt:
        number = ord(letter)
        value.append(number)

    extra = 74
    if len(value) % 2 == 0:
        pass
    else:
        value.append(extra)

    # Grouping every 2 items in list value
    start = 0
    end = len(value)
    step = 2
    xor_comparisons = []

    for i in range(start, end, step):
        comparison = (value[i:i + step])
        xor_comparison = comparison[0] ^ comparison[1]
        xor_comparisons.append(xor_comparison)

    total = str(sum(xor_comparisons))
    random_number = total[len(total) - 2:]

    hashed_password = hex(ord(chr(int(total) ^ int(random_number))))
    return hashed_password
