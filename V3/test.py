import random

def sum_binary_numbers(f_num, s_num):
    if len(f_num) != len(s_num):
        return "The input data has not been normalized"

def convertFloatPart_10to2(number, order):
    len_int_part = order
    float_res = ""
    number_len = len(f"{number}")
    for i in range(len_int_part, 23):
        number = number * 2
        temp_str = len(f"{number}")
        if number_len < temp_str:
            float_res += '1'
            number -= 10 ** number_len
        else:
            float_res += '0'

    if order == 0:
        float_res += '0'
    return float_res
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


# Перевод из любой системы счисления в X
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


def plusFloat32(is_random=True, int_p1=7, float_p1=25, int_p2=1, float_p2=75):
    if is_random:
        sign = random.randint(0, 1)  # 1 - minus, 0 - plus
        float_number_part_array = [5, 25, 75, 125, 375, 625, 875]
        float_part1 = random.choice(float_number_part_array)
        int_part1 = random.randint(10, 126)
        float_part2 = random.choice(float_number_part_array)
        int_part2 = random.randint(10, 126)
    else:
        int_part1 = int_p1
        float_part1 = float_p1
        int_part2 = int_p2
        float_part2 = float_p2

    answer_end = float(f"{int_part1}.{float_part1}") + float(f"{int_part2}.{float_part2}")
    task_text = f"Покажите все этапы выполнения операции сложения чисел " \
                f"{int_part1}.{float_part1} и {int_part2}.{float_part2}"


    int_part1 = convert_10toX(int_part1, 2)
    float_part1 = str(int(convertFloatPart_10to2(float_part1, 0)[::-1]))[::-1]
    int_part2 = convert_10toX(int_part2, 2)
    float_part2 = str(int(convertFloatPart_10to2(float_part2, 0)[::-1]))[::-1]

    order1 = len(int_part1) - 1
    order2 = len(int_part2) - 1
    converted_order1 = convert_10toX(order1, 2)
    converted_order2 = convert_10toX(order2, 2)

    if converted_order1 == '':
        converted_order1 = '0'
    if converted_order2 == '':
        converted_order2 = '0'

    float_part1 = int_part1[1:] + float_part1
    float_part2 = int_part2[1:] + float_part2
    int_part1 = int_part1[:1]
    int_part2 = int_part2[:1]

    answer_normalized1 = f"{int_part1}.{float_part1} * 2^{converted_order1}"
    answer_normalized2 = f"{int_part2}.{float_part2} * 2^{converted_order2}"


    order_difference = order1 - order2
    max_order = ''
    if order_difference < 0:
        order_difference *= -1
    more_ordered_float = ""
    less_ordered_float = ""
    if order1 > order2:
        for i in range(0, order_difference):
            less_ordered_float += '0'
        less_ordered_float += int_part2 + float_part2
        more_ordered_float += int_part1 + float_part1
        max_order = order1
    elif order2 > order1:
        for i in range(0, order_difference):
            less_ordered_float += '0'
        less_ordered_float += int_part1 + float_part1
        more_ordered_float += int_part2 + float_part2
        max_order = order2
    else:
        less_ordered_float += int_part1 + float_part1
        more_ordered_float += int_part2 + float_part2
        max_order = order1

    if len(more_ordered_float) > len(less_ordered_float):
        len_difference = len(more_ordered_float) - len(less_ordered_float)
        for i in range(len_difference):
            less_ordered_float += '0'
    else:
        len_difference = len(less_ordered_float) - len(more_ordered_float)
        for i in range(len_difference):
            more_ordered_float += '0'

    answer_same_order1 = f"{less_ordered_float[0]}.{less_ordered_float[1:]} * 2^{max_order}"
    answer_same_order2 = f"{more_ordered_float[0]}.{more_ordered_float[1:]} * 2^{max_order}"

    summed_float = sum_binary_numbers(more_ordered_float[::-1], less_ordered_float[::-1])

    answer_sum = f"{summed_float} * 2^{convert_10toX(order_difference, 2)}"

    # return {
    #     'task': task_text,
    #     'answer1': answer_normalized1,
    #     'answer2': answer_normalized2,
    #     'answer3': answer_same_order1,
    #     'answer4': answer_same_order2,
    #     'answer5': answer_sum,
    #     'answer6': answer_end,
    # }

    return {
        'task': task_text,
        'answers': [
            answer_normalized1,
            answer_normalized2,
            answer_same_order1,
            answer_same_order2,
            answer_sum,
            answer_end,
        ]
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(plusFloat32())
    return tasks_ret

tasks = generate_tasks()
for task in tasks:
    print(task)