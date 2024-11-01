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


# Перевод из X системы счисления в X

def convert_XtoX(number, from_system, to_system):
    return convert_10toX(convert_Xto10(number, from_system), to_system)

def logic_op_and_mask_toZero():
    first_bit = random.randint(0, 15)
    second_bit = random.randint(0, 15)
    if second_bit == first_bit:
        while second_bit == first_bit:
            second_bit = random.randint(0, 15)
    third_bit = random.randint(0, 15)
    if third_bit == second_bit or third_bit == first_bit:
        while third_bit == second_bit or third_bit == first_bit:
            third_bit = random.randint(0, 15)

    answer = ""
    for i in range(0, 16):
        if i == first_bit or i == second_bit or i == third_bit:
            answer += "0"
        else:
            answer += "1"
    answer = f"AND {convert_XtoX(answer[::-1], 2, 16)}"

    return {
        'VAR1': first_bit,
        'VAR2': second_bit,
        'VAR3': third_bit,
        'ANSWER': answer
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(logic_op_and_mask_toZero())
    return tasks_ret

