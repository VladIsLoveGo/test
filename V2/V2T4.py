import random

def convert_Xto10(number, system):
    result = 0
    order = 0
    if system <= 10:
        number_int = int(number)
        while number_int > 0:
            temp = (number_int % 10) * system ** order
            order += 1
            number_int //= 10
            result += temp
    elif system > 10:
        number_str = str(number)
        while number_str != '':
            if number_str[-1] == 'A':
                temp = 10 * system ** order
            elif number_str[-1] == 'B':
                temp = 11 * system ** order
            elif number_str[-1] == 'C':
                temp = 12 * system ** order
            elif number_str[-1] == 'D':
                temp = 13 * system ** order
            elif number_str[-1] == 'E':
                temp = 14 * system ** order
            elif number_str[-1] == 'F':
                temp = 15 * system ** order
            else:
                temp = (int(number_str[-1]) % 10) * system ** order
            order += 1
            number_str = number_str[:-1]
            result += temp

    return result

def convert_10toX(number, system):
    result = []
    number_int = int(number)
    if system <= 10:
        while number_int > 0:
            temp = number_int % system
            number_int //= system
            result.append(str(temp))
    elif system > 10:
        while number_int > 0:
            temp = number_int % system
            number_int //= system
            if temp == 10:
                result.append('A')
            elif temp == 11:
                result.append('B')
            elif temp == 12:
                result.append('C')
            elif temp == 13:
                result.append('D')
            elif temp == 14:
                result.append('E')
            elif temp == 15:
                result.append('F')
            else:
                result.append(str(temp))

    return ''.join(result[::-1])


# Перевод из X системы счисления в X

def convert_XtoX(number, from_system, to_system):
    return convert_10toX(convert_Xto10(number, from_system), to_system)

def shift_16bit():
    first_bit = random.randint(0, 15)
    second_bit = random.randint(0, 15)
    if first_bit == second_bit:
        while first_bit == second_bit:
            second_bit = random.randint(0, 15)
    if first_bit > second_bit:
        first_bit, second_bit = second_bit, first_bit

    mask = ""
    for i in range(0, 16):
        if first_bit <= i <= second_bit:
            mask += "1"
        else:
            mask += "0"

    mask = convert_XtoX(mask[::-1], 2, 16)
    first_answer_python = f"(N & 0x{mask}) >> {first_bit}"
    first_answer_cpp = f"(N && 0x{mask} >> {first_bit})"

    mask = ""
    bit_len = second_bit - first_bit + 1
    for i in range(0, 16):
        if i < bit_len:
            mask += "1"
        else:
            mask += "0"
    mask = convert_XtoX(mask[::-1], 2, 16)
    second_answer_python = f"(N >> {first_bit}) & 0x{mask}"
    second_answer_cpp = f"(N >> {first_bit}) && 0x{mask}"

    return {
        'VAR1': first_bit,
        'VAR2': second_bit,
        'ANSWER1_python': first_answer_python,
        'ANSWER2_python': second_answer_python,
        'ANSWER1_cpp': first_answer_cpp,
        'ANSWER2_cpp': second_answer_cpp
    }

def generate():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(shift_16bit())
    return tasks_ret

tasks = generate()
for task in tasks:
    print(task)
