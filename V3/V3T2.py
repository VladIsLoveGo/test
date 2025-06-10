import random


def to_binary(num):
    """Преобразование десятичного числа в двоичное с увеличенной точностью."""
    int_part = int(num)
    frac_part = num - int_part
    binary_int = bin(int_part)[2:]
    binary_frac = []
    while frac_part > 0 and len(binary_frac) < 10:  # Точность до 10 бит
        frac_part *= 2
        bit = int(frac_part)
        binary_frac.append(str(bit))
        frac_part -= bit
    return binary_int + '.' + ''.join(binary_frac) if binary_frac else binary_int


def normalize_binary(bin_num):
    """Нормализация двоичного числа: mantissa * 2^order."""
    if '.' not in bin_num:
        bin_num += '.0'
    int_part, frac_part = bin_num.split('.')
    if int_part == '0' and '1' not in frac_part:
        return '0.0', 0
    elif int_part != '0':
        order = len(int_part) - 1
        mantissa = '1.' + int_part[1:] + frac_part
    else:
        first_one = frac_part.index('1')
        order = -(first_one + 1)
        mantissa = '1.' + frac_part[first_one + 1:]
    return mantissa, order


def align_orders(mantissa1, order1, mantissa2, order2):
    """Выравнивание мантисс по одному порядку без ошибочного сдвига при равных порядках."""
    if order1 == order2:
        return mantissa1, mantissa2, order1
    elif order1 < order2:
        diff = order2 - order1
        m1 = mantissa1.split('.')
        int_part = m1[0]
        frac_part = m1[1] if len(m1) > 1 else ''
        if diff <= len(int_part):
            new_int = int_part[:-diff] if diff < len(int_part) else '0'
            new_frac = int_part[-diff:] + frac_part
        else:
            extra_zeros = diff - len(int_part)
            new_frac = '0' * extra_zeros + int_part + frac_part
            new_int = '0'
        shifted = new_int + '.' + new_frac
        return shifted, mantissa2, order2
    else:
        diff = order1 - order2
        m2 = mantissa2.split('.')
        int_part = m2[0]
        frac_part = m2[1] if len(m2) > 1 else ''
        if diff <= len(int_part):
            new_int = int_part[:-diff] if diff < len(int_part) else '0'
            new_frac = int_part[-diff:] + frac_part
        else:
            extra_zeros = diff - len(int_part)
            new_frac = '0' * extra_zeros + int_part + frac_part
            new_int = '0'
        shifted = new_int + '.' + new_frac
        return mantissa1, shifted, order1


def binary_addition(bin1, bin2):
    """Сложение двух двоичных чисел с выравниванием длины."""
    int1, frac1 = bin1.split('.') if '.' in bin1 else (bin1, '')
    int2, frac2 = bin2.split('.') if '.' in bin2 else (bin2, '')

    # Выравнивание дробных частей
    max_frac = max(len(frac1), len(frac2), 10)
    frac1 = frac1.ljust(max_frac, '0')
    frac2 = frac2.ljust(max_frac, '0')

    # Выравнивание целых частей
    max_int = max(len(int1), len(int2))
    int1 = int1.zfill(max_int)
    int2 = int2.zfill(max_int)

    # Полное число без точки
    num1 = int1 + frac1
    num2 = int2 + frac2

    # Сложение как целых чисел
    sum_int = int(num1, 2) + int(num2, 2)
    result = bin(sum_int)[2:]

    # Восстановление точки
    result = result.zfill(max_int + max_frac)
    point_pos = max_frac
    binary_sum = result[:-point_pos] + '.' + result[-point_pos:]
    return binary_sum


def clean_binary(binary_num):
    """Удаление конечных нулей в дробной части двоичного числа."""
    if '.' not in binary_num:
        return binary_num
    int_part, frac_part = binary_num.split('.')
    frac_part = frac_part.rstrip('0')
    return int_part + '.' + frac_part if frac_part else int_part


def binary_to_decimal(binary_num):
    """Перевод двоичного числа в десятичное."""
    int_part, frac_part = binary_num.split('.') if '.' in binary_num else (binary_num, '')
    decimal_int = int(int_part, 2) if int_part else 0
    decimal_frac = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(frac_part))
    return decimal_int + decimal_frac


def normalize_result(binary_sum, order):
    """Нормализация результата сложения."""
    if '.' not in binary_sum:
        binary_sum += '.0'
    int_part, frac_part = binary_sum.split('.')
    if int_part == '0' and '1' not in frac_part:
        return '0.0', 0
    elif len(int_part) > 1:
        shift = len(int_part) - 1
        mantissa = '1.' + int_part[1:] + frac_part
        new_order = order + shift
    else:
        mantissa = int_part + '.' + frac_part
        new_order = order
    return mantissa, new_order


def format_normalized(mantissa, order):
    """Форматирование нормализованного результата в вид xxxx.x с удалением лишних нулей."""
    if mantissa == '0.0':
        return '0.0'
    # Разделяем мантиссу на целую и дробную части
    int_part, frac_part = mantissa.split('.')
    # Удаляем конечные нули из дробной части
    frac_part = frac_part.rstrip('0')
    # Сдвигаем мантиссу на order позиций
    combined = int_part + frac_part
    if order >= 0:
        # Сдвиг влево: умножаем на 2^order
        shifted = bin(int(combined, 2) << order)[2:]
        # Восстанавливаем дробную часть
        if len(frac_part) > 0:
            shifted = shifted.zfill(len(shifted) + len(frac_part))
            point_pos = len(frac_part)
            result = shifted[:-point_pos] + '.' + shifted[-point_pos:]
        else:
            result = shifted + '.0'
    else:
        # Сдвиг вправо: делим на 2^(-order)
        result = '0' * (-order) + combined
        point_pos = len(frac_part) - order
        result = result[:-point_pos] + '.' + result[-point_pos:]
    # Удаляем ведущие нули в целой части и конечные в дробной
    int_part, frac_part = result.split('.')
    int_part = int_part.lstrip('0') or '0'
    frac_part = frac_part.rstrip('0')
    return int_part + '.' + frac_part if frac_part else int_part


def addition(int_part1, float_part1, int_part2, float_part2):
    """Основная функция сложения с пошаговым выводом."""
    num1 = int_part1 + float_part1 / 1000
    num2 = int_part2 + float_part2 / 1000

    bin1 = to_binary(num1)
    bin2 = to_binary(num2)

    mantissa1, order1 = normalize_binary(bin1)
    mantissa2, order2 = normalize_binary(bin2)

    aligned_m1, aligned_m2, aligned_order = align_orders(mantissa1, order1, mantissa2, order2)

    binary_sum = binary_addition(aligned_m1, aligned_m2)
    binary_sum_cleaned = clean_binary(binary_sum)  # Очищаем лишние нули

    normalized_sum, final_order = normalize_result(binary_sum, aligned_order)

    formatted_normalized = format_normalized(normalized_sum, final_order)

    decimal_result = binary_to_decimal(normalized_sum) * (2 ** final_order)

    return {
        'VAR1': num1,
        'VAR2': num2,
        'TITLE1_binary1': 'Переведите первое слагаемое в двоичный код',
        'ANSWER1_binary1': bin1,
        'TITLE2_binary2': 'Переведите второе слагаемое в двоичный код',
        'ANSWER2_binary2': bin2,
        'TITLE3_normalize1': 'Выполните нормализацию и приведите к одному порядку первое слагаемое (пример: 1.1101101 * 2^4)',
        'ANSWER5_align1': f"{aligned_m1} * 2^{aligned_order}",
        'TITLE4_normalize2': 'Выполните нормализацию и приведите к одному порядку второе слагаемое',
        'ANSWER6_align2': f"{aligned_m2} * 2^{aligned_order}",
        'TITLE7_addition': 'Выполните операцию сложения (ответ запишите в двоичной системе счисления)',
        'ANSWER7_addition': f"{binary_sum_cleaned} * 2^{aligned_order}",
        'TITLE8_normalized': 'Выполните нормализацию результата (пример: 1001001.11)',
        'ANSWER8_normalized': formatted_normalized,
        'TITLE9_decimal': 'Переведите результат в десятичную систему счисления (целую и дробную часть разделяйте точкой).',
        'ANSWER9_decimal': decimal_result
    }


def generate(num_tasks=100):
    float_parts = [125, 375, 625]  # возможные дробные части (в тысячных)
    tasks_ret = []
    for _ in range(num_tasks):
        int_part1 = random.randint(1, 100)
        float_part1 = random.choice(float_parts)
        int_part2 = random.randint(1, 100)
        float_part2 = random.choice(float_parts)
        tasks_ret.append(addition(int_part1, float_part1, int_part2, float_part2))
    return tasks_ret
