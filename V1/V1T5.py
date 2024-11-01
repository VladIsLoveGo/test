import random

def sum_16bit_unsigned():
    task_number = random.randint(25000, 40000)
    # task_number = f_n
    second_task_number = random.randint(35000, 50000)
    # second_task_number = s_n

    answer = -1
    summed_number = task_number + second_task_number
    if summed_number <= 65536:
        while summed_number <= 65536:
            second_task_number = random.randint(45000, 55000)
            summed_number = task_number + second_task_number

    if summed_number > 65536:
        answer = summed_number - 65536
        while answer > 65536:
            answer -= 65536

    return {
        'VAR1': task_number,
        'VAR2': second_task_number,
        'ANSWER': answer
    }

def generate_tasks():
    tasks_ret = []
    for i in range(100):
        tasks_ret.append(sum_16bit_unsigned())
    return tasks_ret

