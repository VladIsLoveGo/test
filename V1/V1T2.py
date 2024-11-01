import random

def add_insignificant_zeros(line, bit):
    if len(line) < bit:
        line = line[::-1]
        for i in range(bit - len(line)):
            line += '0'
        line = line[::-1]
    return line


def convert_NegativeNumberXto2(number):
    number = convert_10toX(number, 2)[::-1]
    for i in range(len(number), 8):
        number += ''.join('0')
    number = number[::-1]
    # print(number)
    inverse_number = ""
    for i in range(len(number)):
        if number[i] == '0':
            inverse_number += '1'
        elif number[i] == '1':
            inverse_number += '0'
    inverse_number = inverse_number[::-1]
    # print(inverse_number)
    number = ''
    # + 1
    if inverse_number[0] == '0':
        number += ('1' + inverse_number[1:])[::-1]
    else:
        index = -1
        for i in range(len(inverse_number)):
            if inverse_number[i] == '0':
                index = i
                break
        if index != -1:
            for i in range(0, index):
                number += '0'
            number += ('1' + inverse_number[index+1:])
            number = number[::-1]
        else:
            for i in range(len(inverse_number) - 1):
                number += '0'
            number += '1'
            for i in range(len(inverse_number)):
                number += '0'
            number = number[::-1]

    return number



def int_in_mem():
    task_number = random.randint(20, 128)
    answer_number = convert_NegativeNumberXto2(task_number)
    answer_number = add_insignificant_zeros(answer_number, 8)
    task_number *= -1

    return {
        'VAR1': task_number,
        'VAR2': second_task_number,
        'ANSWER': answer
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(int_in_mem())
    return tasks_ret