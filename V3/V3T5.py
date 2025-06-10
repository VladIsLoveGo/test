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

def binary_division(bin1, bin2):
    """Деление двух двоичных чисел с нормализацией результата."""
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

    # Преобразуем в десятичные для деления
    val1 = int(num1, 2) / (2 ** point_pos1)
    val2 = int(num2, 2) / (2 ** point_pos2)
    if val2 == 0:
        raise ValueError("Division by zero")
    result_float = val1 / val2
    is_negative = is_neg1 != is_neg2

    # Преобразуем результат в двоичное
    binary_result = to_binary(abs(result_float))
    if is_negative:
        binary_result = '-' + binary_result

    return binary_result

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

def division(int_part1, float_part1, int_part2):
    """Основная функция деления с пошаговым выводом."""
    num1 = int_part1 + float_part1 / 1000
    num2 = int_part2  # Второе число всегда целое

    bin1 = to_binary(num1)
    bin2 = to_binary(num2)

    mantissa1, order1 = normalize_binary(bin1)
    mantissa2, order2 = normalize_binary(bin2)

    # Делим мантиссы
    binary_quotient = binary_division(mantissa1, mantissa2)
    binary_quotient_cleaned = clean_binary(binary_quotient)

    # Вычитаем порядки
    total_order = order1 - order2

    # Нормализуем результат
    normalized_mantissa, new_order = normalize_binary(binary_quotient_cleaned)
    final_order = total_order + new_order

    # Форматируем результат для ANSWER8_normalized
    formatted_normalized = format_normalized(normalized_mantissa, final_order)

    # Вычисляем десятичное значение
    decimal_result = binary_to_decimal(normalized_mantissa) * (2 ** final_order)

    return {
        'VAR1': num1,
        'VAR2': num2,
        'TITLE1_binary1': 'Переведите делимое в двоичный код',
        'ANSWER1_binary1': bin1,
        'TITLE2_binary2': 'Переведите делитель в двоичный код',
        'ANSWER2_binary2': bin2,
        'TITLE3_normalize1': 'Выполните нормализацию делимого (пример: 1.1101101 * 2^4).',
        'ANSWER5_align1': f"{mantissa1} * 2^{order1}",
        'TITLE4_normalize2': 'Выполните нормализацию делителя',
        'ANSWER6_align2': f"{mantissa2} * 2^{order2}",
        'TITLE7_division': 'Выполните операцию деления (ответ запишите в двоичной системе счисления)',
        'ANSWER7_division': f"{binary_quotient_cleaned} * 2^{total_order}",
        'TITLE8_normalized': 'Выполните нормализацию результата',
        'ANSWER8_normalized': formatted_normalized,
        'TITLE9_decimal': 'Переведите результат в десятичную систему счисления (целую и дробную часть разделяйте точкой).',
        'ANSWER9_decimal': decimal_result
    }

def is_adequate_result(result):
    """Проверка, что результат деления имеет дробную часть не длиннее 3 бит и не слишком велик."""
    if result >= 10:  # Ограничиваем результат до 10
        return False
    frac_part = result - int(result)
    if frac_part == 0:
        return True  # Целое число — адекватный результат
    binary_frac = to_binary(frac_part)[2:]  # Убираем '0.' из начала
    return len(binary_frac.rstrip('0')) <= 3  # Длина дробной части не более 3 бит

def generate(num_tasks=100):
    float_parts = [125, 375, 625]  # Соответствует 0.125, 0.375, 0.625
    divisors = [6, 7, 11, 10, 5]  # VAR2 выбирается из этого списка
    tasks_ret = []
    attempts = 0
    max_attempts = 10000  # Увеличиваем попытки, так как ограничения строгие
    while len(tasks_ret) < num_tasks and attempts < max_attempts:
        int_part1 = random.randint(45, 99)  # Целая часть VAR1 от 45 до 99
        float_part1 = random.choice(float_parts)
        int_part2 = random.choice(divisors)  # VAR2 из {6, 7, 11, 10, 5}
        num1 = int_part1 + float_part1 / 1000
        num2 = int_part2
        result = num1 / num2
        if is_adequate_result(result):
            tasks_ret.append(division(int_part1, float_part1, int_part2))
        attempts += 1
    if len(tasks_ret) < num_tasks:
        print(f"Warning: Only generated {len(tasks_ret)} tasks due to strict constraints.")
    return tasks_ret
