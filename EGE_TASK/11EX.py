import random
import math

def generate_id_task():
    # Генерация случайных параметров
    alphabet_size = random.randint(10, 30)
    id_length = random.randint(8, 12)
    num_letters_start = random.randint(1, 2)
    num_letters_end = random.randint(1, 2)
    num_digits = id_length - num_letters_start - num_letters_end
    num_ids = random.randint(20, 50)

    if num_digits < 0:
        num_digits = 0
        id_length = num_letters_start + num_letters_end
        num_digits = id_length - num_letters_start - num_letters_end

    bits_per_letter = math.ceil(math.log2(alphabet_size)) if alphabet_size > 1 else 1

    bits_per_digit = math.ceil(math.log2(10))  # 4 бита, так как 2^3 < 10 < 2^4

    total_bits = (num_letters_start + num_letters_end) * bits_per_letter + num_digits * bits_per_digit

    total_bytes = math.ceil(total_bits / 8)

    answer = total_bytes * num_ids

    return {
        'ALPHABET_SIZE': alphabet_size,
        'ID_LENGTH': id_length,
        'NUM_LETTERS_START': num_letters_start,
        'NUM_LETTERS_END': num_letters_end,
        'NUM_DIGITS': num_digits,
        'NUM_IDS': num_ids,
        'ANSWER': answer
    }


def generate():
    tasks_ret = []
    for _ in range(100):
        tasks_ret.append(generate_id_task())
    return tasks_ret
