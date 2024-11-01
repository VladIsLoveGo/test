import random

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


def add_insignificant_zeros(line, bit):
    if len(line) < bit:
        line = line[::-1]
        for i in range(bit - len(line)):
            line += '0'
        line = line[::-1]
    return line


def unsigned_int_in_mem():
    task_number = random.randint(20, 255)
    answer_number = convert_10toX(task_number, 2)
    answer_number = add_insignificant_zeros(answer_number, 8)

    return {
        'VAR1': task_number,
        'ANSWER': answer
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(unsigned_int_in_mem())
    return tasks_ret
