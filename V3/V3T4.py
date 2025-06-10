import random

def to_binary(num):
    """Преобразование десятичного числа в двоичное с увеличенной точностью."""
    int_part = int(num)
    frac_part = num - int_part
    binary_int = bin(abs(int_part))[2:]
    binary_frac = []
    while frac_part > 0 and len(binary_frac) < 10:  # Точность до 10 бит
        frac_part *= 2
        bit = int(frac_part)
        binary_frac.append(str(bit))
        frac_part -= bit
    binary = binary_int + '.' + ''.join(binary_frac) if binary_frac else binary_int
    return '-' + binary if num < 0 else binary

def normalize_binary(bin_num):
    """Нормализация двоичного числа: mantissa * 2^order."""
    is_negative = bin_num.startswith('-')
    if is_negative:
        bin_num = bin_num[1:]
    if '.' not in bin_num:
        bin_num += '.0'
    int_part, frac_part = bin_num.split('.')
    if int_part == '0' and '1' not in frac_part:
        return '0.0', 0
    elif int_part != '0':
        order = len(int_part) - 1
        mantissa = '1.' + int_part[1:] + frac_part
    else:
        first_one = frac_part.index('1') if '1' in frac_part else -1
        if first_one == -1:
            return '0.0', 0
        order = -(first_one + 1)
        mantissa = '1.' + frac_part[first_one + 1:]
    if is_negative:
        mantissa = '-' + mantissa
    return mantissa, order

def binary_multiplication(bin1, bin2):
    """Умножение двух двоичных чисел с нормализацией результата."""
    is_neg1 = bin1.startswith('-')
    is_neg2 = bin2.startswith('-')
    num1 = bin1[1:] if is_neg1 else bin1
    num2 = bin2[1:] if is_neg2 else bin2

    # Удаляем точки и запоминаем их позиции
    if '.' in num1:
        int_part1, frac_part1 = num1.split('.')
        point_pos1 = len(frac_part1)
        num1 = int_part1 + frac_part1
    else:
        point_pos1 = 0
        num1 = num1

    if '.' in num2:
        int_part2, frac_part2 = num2.split('.')
        point_pos2 = len(frac_part2)
        num2 = int_part2 + frac_part2
    else:
        point_pos2 = 0
        num2 = num2

    # Умножаем как целые числа
    val1 = int(num1, 2)
    val2 = int(num2, 2)
    result_int = val1 * val2
    is_negative = is_neg1 != is_neg2

    # Преобразуем результат обратно в двоичное с учётом точки
    result = bin(abs(result_int))[2:]
    total_point_pos = point_pos1 + point_pos2

    if total_point_pos > 0:
        if len(result) > total_point_pos:
            binary_product = result[:-total_point_pos] + '.' + result[-total_point_pos:]
        else:
            binary_product = '0.' + '0' * (total_point_pos - len(result)) + result
    else:
        binary_product = result

    if is_negative:
        binary_product = '-' + binary_product

    return binary_product

def clean_binary(binary_num):
    """Удаление конечных и ведущих нулей в двоичном числе."""
    is_negative = binary_num.startswith('-')
    num = binary_num[1:] if is_negative else binary_num
    if '.' not in num:
        num = num.lstrip('0') or '0'
        return '-' + num if is_negative else num
    int_part, frac_part = num.split('.')
    int_part = int_part.lstrip('0') or '0'
    frac_part = frac_part.rstrip('0')
    result = int_part + '.' + frac_part if frac_part else int_part
    return '-' + result if is_negative else result

def binary_to_decimal(binary_num):
    """Перевод двоичного числа в десятичное."""
    is_negative = binary_num.startswith('-')
    num = binary_num[1:] if is_negative else binary_num
    int_part, frac_part = num.split('.') if '.' in num else (num, '')
    decimal_int = int(int_part, 2) if int_part else 0
    decimal_frac = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(frac_part)) if frac_part else 0
    result = decimal_int + decimal_frac
    return -result if is_negative else result

def format_normalized(mantissa, order):
    """Форматирование нормализованного результата в вид xxxx.x с удалением лишних нулей."""
    if mantissa == '0.0':
        return '0.0'
    is_negative = mantissa.startswith('-')
    m = mantissa[1:] if is_negative else mantissa
    int_part, frac_part = m.split('.')
    frac_part = frac_part.rstrip('0')
    combined = int_part + frac_part
    if order >= 0:
        shifted = bin(int(combined, 2) << order)[2:]
        if len(frac_part) > 0:
            point_pos = len(frac_part)
            shifted = shifted.zfill(len(shifted) + point_pos)
            result = shifted[:-point_pos] + '.' + shifted[-point_pos:]
        else:
            result = shifted + '.0'
    else:
        result = '0' * (-order) + combined
        point_pos = len(frac_part) - order
        result = result[:-point_pos] + '.' + result[-point_pos:]
    int_part, frac_part = result.split('.')
    int_part = int_part.lstrip('0') or '0'
    frac_part = frac_part.rstrip('0')
    result = int_part + '.' + frac_part if frac_part else int_part
    return '-' + result if is_negative else result

def multiplication(int_part1, float_part1, int_part2):
    """Основная функция умножения с пошаговым выводом."""
    num1 = int_part1 + float_part1 / 1000
    num2 = int_part2  # Второе число теперь всегда целое

    bin1 = to_binary(num1)
    bin2 = to_binary(num2)

    mantissa1, order1 = normalize_binary(bin1)
    mantissa2, order2 = normalize_binary(bin2)

    # Умножаем мантиссы
    binary_product = binary_multiplication(mantissa1, mantissa2)
    binary_product_cleaned = clean_binary(binary_product)

    # Суммируем порядки
    total_order = order1 + order2

    # Нормализуем результат
    normalized_mantissa, new_order = normalize_binary(binary_product_cleaned)
    final_order = total_order + new_order

    # Форматируем результат для ANSWER8_normalized
    formatted_normalized = format_normalized(normalized_mantissa, final_order)

    # Вычисляем десятичное значение
    decimal_result = binary_to_decimal(normalized_mantissa) * (2 ** final_order)

    return {
        'VAR1': num1,
        'VAR2': num2,
        'TITLE1_binary1': 'Переведите первый множитель в двоичный код',
        'ANSWER1_binary1': bin1,
        'TITLE2_binary2': 'Переведите второй множитель в двоичный код',
        'ANSWER2_binary2': bin2,
        'TITLE3_normalize1': 'Выполните нормализацию первого множителя (пример: 1.1101101 * 2^4).',
        'ANSWER5_align1': f"{mantissa1} * 2^{order1}",
        'TITLE4_normalize2': 'Выполните нормализацию второго множителя',
        'ANSWER6_align2': f"{mantissa2} * 2^{order2}",
        'TITLE7_multiplication': 'Выполните операцию умножения (ответ запишите в двоичной системе счисления)',
        'ANSWER7_multiplication': f"{binary_product_cleaned} * 2^{total_order}",
        'TITLE8_normalized': 'Выполните нормализацию результата',
        'ANSWER8_normalized': formatted_normalized,
        'TITLE9_decimal': 'Переведите результат в десятичную систему счисления (целую и дробную часть разделяйте точкой).',
        'ANSWER9_decimal': decimal_result
    }

def generate(num_tasks=100):
    float_parts = [125, 375, 625]
    tasks_ret = []
    for _ in range(num_tasks):
        int_part1 = random.randint(1, 100)
        float_part1 = random.choice(float_parts)
        int_part2 = random.randint(1, 100)  # Второе число теперь всегда целое
        tasks_ret.append(multiplication(int_part1, float_part1, int_part2))
    return tasks_ret

