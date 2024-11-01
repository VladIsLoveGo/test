import random

def sum_8bit_unsigned():
    task_number = random.randint(20, 255)
    # task_number = f_n
    second_task_number = random.randint(150, 300)
    # second_task_number = s_n

    answer = -1
    summed_number = task_number + second_task_number
    if summed_number <= 256:
        while summed_number <= 256:
            task_number = random.randint(117, 255)
            summed_number = task_number + second_task_number

    if summed_number > 256:
        answer = summed_number - 256
        while answer > 256:
            answer -= 256


    return {
        'VAR1': task_number,
        'VAR2': second_task_number,
        'ANSWER': answer
    }


def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(sum_8bit_unsigned())
    return tasks_ret
