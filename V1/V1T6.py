import random

def sum_16bit_signed():
    task_number = random.randint(10000, 24000)
    # task_number = f_n
    second_task_number = random.randint(22768, 25000)
    # second_task_number = s_n

    summed_number = task_number + second_task_number
    answer = -1
    is_negative = False
    if summed_number > 32767:
        answer = summed_number - 65536
        while answer > 32767:
            answer -= 65536

    return {
        'VAR1': task_number,
        'VAR2': second_task_number,
        'ANSWER': answer
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(sum_16bit_signed())
    return tasks_ret
