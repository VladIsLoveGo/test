import random

def sum_8bit_signed():
    task_number = random.randint(40, 127)
    # task_number = f_n
    second_task_number = random.randint(88, 250)
    # second_task_number = s_n

    summed_number = task_number + second_task_number
    answer = -1
    is_negative = False
    if summed_number > 127:
        answer = summed_number - 256
        while answer > 127:
            answer -= 256
    return {
        'VAR1': task_number,
        'VAR2': second_task_number,
        'ANSWER': answer
    }

def generate():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(sum_8bit_signed())
    return tasks_ret

