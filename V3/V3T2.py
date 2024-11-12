import random

def to_binary(num):
    int_part = int(num)
    frac_part = num - int_part
    binary_int = bin(int_part)[2:]

    binary_frac = []
    while frac_part > 0 and len(binary_frac) < 8:
        frac_part *= 2
        bit = int(frac_part)
        binary_frac.append(str(bit))
        frac_part -= bit

    return binary_int + '.' + ''.join(binary_frac) if binary_frac else binary_int

def binary_to_decimal(binary_num):
    int_part, frac_part = binary_num.split('.') if '.' in binary_num else (binary_num, '')
    decimal_int = int(int_part, 2)
    decimal_frac = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(frac_part))

    return decimal_int + decimal_frac

def normalize_binary(bin_num):
    if '.' in bin_num:
        int_part, frac_part = bin_num.split('.')
    else:
        int_part, frac_part = bin_num, ''

    if int_part == '0':
        first_significant_index = next((i for i, bit in enumerate(frac_part) if bit == '1'), len(frac_part))
        if first_significant_index < len(frac_part):
            mantissa = '0.' + frac_part[first_significant_index + 1:]
            order = - (first_significant_index + 1)
        else:
            return '0.0', 0
    else:
        normalized_int = int_part.lstrip('0')
        mantissa = normalized_int + frac_part
        order = len(normalized_int) - 1
        mantissa = '1.' + mantissa[1:]

    return mantissa, order

def align_binary(bin1, bin2):
    int_part1, frac_part1 = bin1.split('.') if '.' in bin1 else (bin1, '')
    int_part2, frac_part2 = bin2.split('.') if '.' in bin2 else (bin2, '')

    max_frac_len = max(len(frac_part1), len(frac_part2))
    frac_part1 = frac_part1.ljust(max_frac_len, '0')
    frac_part2 = frac_part2.ljust(max_frac_len, '0')

    return f"{int_part1}.{frac_part1}", f"{int_part2}.{frac_part2}"

def binary_addition(bin1, bin2):
    decimal1 = binary_to_decimal(bin1)
    decimal2 = binary_to_decimal(bin2)
    decimal_sum = decimal1 + decimal2
    return to_binary(decimal_sum)

def addition(is_random=True):
    float_number_part_array = [5, 25, 75, 125, 375, 625, 875]
    float_part1 = random.choice(float_number_part_array)
    int_part1 = random.randint(10, 126)
    float_part2 = random.choice(float_number_part_array)
    int_part2 = random.randint(10, 126)

    num1 = int_part1 + float_part1 / 1000
    num2 = int_part2 + float_part2 / 1000
    answer = round(num1 + num2, 3)

    bin1 = to_binary(num1)
    bin2 = to_binary(num2)

    normalized_bin1, order1 = normalize_binary(bin1)
    normalized_bin2, order2 = normalize_binary(bin2)

    aligned_bin1, aligned_bin2 = align_binary(bin1, bin2)
    binary_sum = binary_addition(aligned_bin1, aligned_bin2)

    normalized_sum, sum_order = normalize_binary(binary_sum)
    decimal_sum = binary_to_decimal(binary_sum)

    return {
        'VAR1': num1,
        'VAR2': num2,
        'TITLE1_binary1': 'Переведите первое слагаемое в двоичный код',
        'ANSWER1_binary1': bin1,
        'TITLE2_binary2': 'Переведите второе слагаемое в двоичный код',
        'ANSWER2_binary2': bin2,
        'TITLE3_normalize1': 'Выполните нормализацию первого слагаемого',
        'ANSWER3_normalize1': f"{normalized_bin1} * 2^{order1}",
        'TITLE4_normalize2': 'Выполните нормализацию второго слагаемого',
        'ANSWER4_normalize2': f"{normalized_bin2} * 2^{order2}",
        'TITLE5_align1': 'Приведите к одному порядку первое слагаемое',
        'ANSWER5_align1': aligned_bin1,
        'TITLE6_align2': 'Приведите к одному порядку второе слагаемое',
        'ANSWER6_align2': aligned_bin2,
        'TITLE7_addition': 'Выполните операцию сложения (ответ запишите в двоичной системе счисления)',
        'ANSWER7_addition': binary_sum,
        'TITLE8_normalized': 'Выполните нормализацию результата',
        'ANSWER8_normalized': f"{normalized_sum} * 2^{sum_order}",
        'TITLE9_decimal': 'Переведите результат в десятичную систему счисления',
        'ANSWER9_decimal': decimal_sum,
        'FINAL_ANSWER': answer
    }

def generate():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(addition())
    return tasks_ret
