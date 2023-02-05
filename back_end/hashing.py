import random

'''
How my hashing algorithm works:
1. Password and salt converted to binary and stored in list value
2. Length of value is checked if even and if not, number 74 added (randomly chosen by programmer)
3. Neighbouring items in value split into pairs
4. Items in each pair XOR'ed against each other
5. Output of each comparison between pair stored in list new
6. Sum of new calculated
7. Random number chosen (last 2 digits of total) to XOR against sum of new outputting hash
8. Hash, salt, randomly chosen number stored to refer back to for user logging back in
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
    comparison = []
    xor_comparisons = []
    for i in range(start, end, step):
        comparison = (value[i:i + step])
        xor_comparison = comparison[0] ^ comparison[1]
        xor_comparisons.append(xor_comparison)

    # Number randomly generated to xor against total of numbers in xor_comparisons
    total = str(sum(xor_comparisons))
    random_number = total[len(total) - 2:]
    # print(total)
    # print(random_number)

    users[email_input][1] = random_number
    # Hash generated
    users[email_input][2] = hex(ord(chr(int(total) ^ int(random_number))))

    # print('Last 2 digits of total:', random_number)
    # print('Hash:', hex(ord(chr(int(total) ^ int(random_number)))))


def password_to_denary(password):
    value = []
    salt = create_salt()
    # print('Salt:', salt)
    users[email_input][0] = salt

    # Each character of password converted to denary and stored in list value
    for letter in password:
        number = ord(letter)
        value.append(number)

    # Each character of salt converted to denary and stored in list value
    for letter in salt:
        number = ord(letter)
        value.append(number)

    # print('Password and salt in binary:', value)
    hashing(value)


email_input = input('Email: ')
users = {email_input: ['', '', '']}
password = input('Password: ')

password_to_denary(password=password)
print(users)

# conn = sqlite3.connect('test_database.db')
# c = conn.cursor()
# c.execute('''
#           CREATE TABLE IF NOT EXISTS passwords
#           (
#               [email] TEXT PRIMARY KEY NOT NULL,
#               [hash] TEXT NOT NULL,
#               [salt] TEXT NOT NULL
#           )
#           ''')
# c.execute('INSERT INTO passwords VALUES (?, ?, ?)', (email_input, users[email_input][2], users[email_input][0]))
# conn.commit()

'''
TODO:
- When user logs back in, retrieve salt and random number used the first time, run password + salt through hashing algorithm to see that it returns the same hash, allowing user to log back in
- SQL: Prevent multiple users with same email logging in
'''