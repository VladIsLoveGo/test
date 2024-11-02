import random
import operator

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


def log_op_OR():
    task_number = random.randint(100, 2000)
    second_task_number = random.randint(100, 2000)
    if task_number == second_task_number:
        while task_number == second_task_number:
            second_task_number = random.randint(100, 2000)

    answer = convert_10toX(operator.xor(task_number, second_task_number), 16)

    task_number = convert_10toX(task_number, 16)
    second_task_number = convert_10toX(second_task_number, 16)

    return {
        'VAR1': task_number,
        'VAR2': second_task_number,
        'ANSWER': answer
    }

def generate():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(log_op_OR())
    return tasks_ret
