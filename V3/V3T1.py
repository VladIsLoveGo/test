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

def convertFloatPart_10to2(number, order):
    len_int_part = order
    float_res = ""
    number_len = len(f"{number}")
    for i in range(len_int_part, 23):
        number = number * 2
        temp_str = len(f"{number}")
        if number_len < temp_str:
            float_res += '1'
            number -= 10**number_len
        else:
            float_res += '0'

    if order == 0:
        float_res += '0'
    return float_res
def float_10to2(is_random=True, sig=0, int_p=7, float_p=25):
    if is_random:
        sign = random.randint(0, 1)  # 1 - minus, 0 - plus
        float_number_part_array = [5, 25, 75, 125, 375, 625, 875]
        float_part = random.choice(float_number_part_array)
        int_part = random.randint(10, 126)
    else:
        sign = sig
        int_part = int_p
        float_part = float_p
    answer = ""
    if sign == 1:
        task_text = f"-{int_part}.{float_part}"
        answer += '1'
    else:
        task_text = f"{int_part}.{float_part}"
        answer += '0'

    int_part = convert_10toX(int_part, 2)
    order = len(int_part) - 1
    float_part = convertFloatPart_10to2(float_part, order)
    order = convert_10toX(order + 127, 2)

    answer += order
    answer += int_part[1:]
    answer += float_part

    return {
        'VAR1': task_text,
        'ANSWER': answer
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(float_10to2())
    return tasks_ret

tasks = generate_tasks()
for task in tasks:
    print(task)