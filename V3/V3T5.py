import random


def random_numbers():
    num1 = round(random.uniform(1, 100), random.randint(0, 4))
    num2 = round(random.uniform(1, 100), random.randint(0, 4))
    return num1, num2


def to_binary(num):  # перевод числа в двоичный код
    int_part = int(num)
    frac_part = num - int_part
    binary_int = bin(int_part)[2:]

    binary_frac = []  # Перевод дробной части
    while frac_part > 0 and len(binary_frac) < 8:
        frac_part *= 2
        bit = int(frac_part)
        binary_frac.append(str(bit))
        frac_part -= bit

    return binary_int + '.' + ''.join(binary_frac) if binary_frac else binary_int


def normalize_binary(bin_num):  # нормализация чисел
    int_part, frac_part = bin_num.split('.')

    # Нормализация целой части
    if int_part == '0':
        first_significant_index = next((i for i, bit in enumerate(frac_part) if bit == '1'), len(frac_part))
        if first_significant_index < len(frac_part):
            mantissa = '0.' + frac_part[first_significant_index + 1:]  # 0.1xxxx
            order = - (first_significant_index + 1)
        else:
            return '0.0', 0
    else:
        normalized_int = int_part.lstrip('0')
        mantissa = normalized_int + frac_part  # Убираем точку для дальнейшей нормализации
        order = len(normalized_int) - 1
        mantissa = '1.' + mantissa[1:]

    return mantissa, order


def division(is_random=True):
    if is_random:
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

    num1 = int_part1 + float_part1 / 1000
    num2 = int_part2 + float_part2 / 1000
    answer = round(num1 / num2, 5)
    bin1 = to_binary(num1)
    bin2 = to_binary(num2)

    # Нормализация без приведения к одинаковому порядку
    normalized_bin1, order1 = normalize_binary(bin1)
    normalized_bin2, order2 = normalize_binary(bin2)

    normalized_result1 = f"{normalized_bin1} * 2^{order1}"
    normalized_result2 = f"{normalized_bin2} * 2^{order2}"

    return {
        'VAR1': num1,
        'VAR2': num2,
        'ANSWER_binary1': bin1,
        'ANSWER_binary2': bin2,
        'ANSWER_normalized1': normalized_result1,
        'ANSWER_normalized2': normalized_result2,
        'ANSWER': answer
    }


def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(division())
    return tasks_ret
