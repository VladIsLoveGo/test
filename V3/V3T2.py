import random

def to_binary(num):
    int_part = int(num)
    frac_part = num - int_part
    binary_int = bin(int_part)[2:]

    binary_frac = []
    while frac_part > 0 and len(binary_frac) < 7:  # ограничение точности
        frac_part *= 2
        bit = int(frac_part)
        binary_frac.append(str(bit))
        frac_part -= bit

    return binary_int + '.' + ''.join(binary_frac) if binary_frac else binary_int

def normalize_binary(bin_num):
    if '.' not in bin_num:
        bin_num += '.0'
    int_part, frac_part = bin_num.split('.')

    if int_part == '0':
        first_one = frac_part.find('1')
        if first_one == -1:
            return '0.0', 0
        mantissa = '0.' + '0' * first_one + '1' + frac_part[first_one:]
        order = -(first_one + 1)
    else:
        mantissa = '1.' + int_part[1:] + frac_part
        order = len(int_part) - 1

    return mantissa, order

def align_orders(mantissa1, order1, mantissa2, order2):
    if order1 < order2:
        diff = order2 - order1
        m1 = mantissa1.split('.')
        shifted = '0.' + '0' * (diff - 1) + m1[0] + m1[1]
        return shifted, mantissa2, order2
    else:
        diff = order1 - order2
        m2 = mantissa2.split('.')
        shifted = '0.' + '0' * (diff - 1) + m2[0] + m2[1]
        return mantissa1, shifted, order1

def binary_addition(bin1, bin2):
    int1, frac1 = bin1.split('.')
    int2, frac2 = bin2.split('.')

    max_frac = max(len(frac1), len(frac2))
    frac1 = frac1.ljust(max_frac, '0')
    frac2 = frac2.ljust(max_frac, '0')

    num1 = int1 + frac1
    num2 = int2 + frac2

    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)

    carry = 0
    result = []
    for i in range(max_len - 1, -1, -1):
        bit_sum = int(num1[i]) + int(num2[i]) + carry
        result.append(str(bit_sum % 2))
        carry = bit_sum // 2

    if carry:
        result.append('1')

    result_str = ''.join(reversed(result))
    point_pos = max_frac
    return result_str[:-point_pos] + '.' + result_str[-point_pos:].rstrip('0')

def binary_to_decimal(binary_num):
    if '.' in binary_num:
        int_part, frac_part = binary_num.split('.')
    else:
        int_part = binary_num
        frac_part = ''

    decimal_int = int(int_part, 2) if int_part else 0
    decimal_frac = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(frac_part))
    return decimal_int + decimal_frac

def clean_binary(bin_str):
    if '.' in bin_str:
        bin_str = bin_str.rstrip('0')  # убрать лишние нули справа
        if bin_str.endswith('.'):
            bin_str = bin_str[:-1]     # убрать точку, если она осталась в конце
    return bin_str

def addition(int_part1, float_part1, int_part2, float_part2):
    num1 = int_part1 + float_part1 / 1000
    num2 = int_part2 + float_part2 / 1000

    # 1. Перевод в двоичный код
    bin1 = to_binary(num1)
    bin2 = to_binary(num2)

    # 2. Нормализация
    mantissa1, order1 = normalize_binary(bin1)
    mantissa2, order2 = normalize_binary(bin2)

    # 3. Выравнивание порядков
    aligned_m1, aligned_m2, aligned_order = align_orders(mantissa1, order1, mantissa2, order2)

    # 4. Сложение
    binary_sum = binary_addition(aligned_m1, aligned_m2)
    binary_sum = clean_binary(binary_sum)  # убираем лишние нули после точки

    # 5. Нормализация результата
    normalized_sum, sum_order = normalize_binary(binary_sum)
    final_order = aligned_order + sum_order

    # Формируем окончательный результат
    if final_order >= 0:
        combined = normalized_sum.replace('.', '')
        final_binary = combined[:final_order + 1] + '.' + combined[final_order + 1:]
    else:
        final_binary = '0.' + '0' * (-final_order - 1) + normalized_sum.replace('.', '')

    final_binary = clean_binary(final_binary)  # Удаление лишних нулей

    decimal_result = binary_to_decimal(final_binary)

    return {
        'VAR1': num1,
        'VAR': num2,
        'TITLE1_binary1': 'Переведите первое слагаемое в двоичный код',
        'ANSWER1_binary1': bin1,
        'TITLE2_binary2': 'Переведите второе слагаемое в двоичный код',
        'ANSWER2_binary2': bin2,
        'TITLE3_normalize1': 'Выполните нормализацию первого слагаемого (пример: 1.1101101 * 2^4).',
        'ANSWER3_normalize1': f"{mantissa1} * 2^{order1}",
        'TITLE4_normalize2': 'Выполните нормализацию второго слагаемого',
        'ANSWER4_normalize2': f"{mantissa2} * 2^{order2}",
        'TITLE5_align1': 'Приведите к одному порядку первое слагаемое',
        'ANSWER5_align1': f"{aligned_m1} * 2^{aligned_order}",
        'TITLE6_align2': 'Приведите к одному порядку второе слагаемое',
        'ANSWER6_align2': "{aligned_m2} * 2^{aligned_order}",
        'TITLE7_addition': 'Выполните операцию сложения (ответ запишите в двоичной системе счисления)',
        'ANSWER7_addition': f"{binary_sum} * 2^{aligned_order}",
        'TITLE8_normalized': 'Выполните нормализацию результата',
        'ANSWER8_normalized': f"{normalized_sum} * 2^{final_order}",
        'TITLE9_decimal': 'Переведите результат в десятичную систему счисления (целую и дробную часть разделяйте точкой).',
        'ANSWER9_decimal': decimal_result
    }

def generate(num_tasks=100):
    float_parts = [125, 375, 625]
    tasks_ret = []
    for _ in range(num_tasks):
        int_part1 = random.randint(1, 100)
        float_part1 = random.choice(float_parts)
        int_part2 = random.randint(1, 100)
        float_part2 = random.choice(float_parts)
        tasks_ret.append(addition(int_part1, float_part1, int_part2, float_part2))
    return tasks_ret

