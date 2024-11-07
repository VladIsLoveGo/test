import numpy as np


def check_strategy_optimality(A, strategy, is_row_player=True):
    """Проверяет, является ли стратегия оптимальной"""
    if is_row_player:
        payoff = np.min(np.dot(A.T, strategy))
    else:
        payoff = np.max(np.dot(A, strategy))

    # Проверяем все чистые стратегии
    for i in range(len(strategy)):
        pure_strategy = np.zeros(len(strategy))
        pure_strategy[i] = 1
        if is_row_player:
            pure_payoff = np.min(np.dot(A.T, pure_strategy))
            if pure_payoff > payoff + 1e-10:
                return False
        else:
            pure_payoff = np.max(np.dot(A, pure_strategy))
            if pure_payoff < payoff - 1e-10:
                return False
    return True


def find_game_value(A, strategy1, strategy2):
    """Находит цену игры для данной пары стратегий"""
    return np.dot(np.dot(strategy1, A), strategy2)


def find_optimal_strategies(A):
    n = len(A)
    optimal_T1 = []
    optimal_T2 = []

    # Проверяем все возможные пары базисных векторов
    for i in range(n):
        for j in range(i + 1, n):
            # Проверяем подматрицы 2x2
            for k in range(n):
                for l in range(k + 1, n):
                    sub_indices_row = [i, j]
                    sub_indices_col = [k, l]
                    sub_matrix = A[np.ix_(sub_indices_row, sub_indices_col)]

                    try:
                        # Решаем систему уравнений
                        B = np.linalg.inv(sub_matrix)
                        e = np.ones(2)
                        y = np.dot(B, e) / np.dot(np.dot(e, B), e)
                        x = np.dot(e, B) / np.dot(np.dot(e, B), e)

                        # Проверяем допустимость решения для первого игрока
                        if all(y >= -1e-10) and abs(sum(y) - 1) < 1e-10:
                            full_y = np.zeros(n)
                            full_y[sub_indices_row] = y
                            if check_strategy_optimality(A, full_y, True):
                                optimal_T1.append(full_y)

                        # Проверяем допустимость решения для второго игрока
                        if all(x >= -1e-10) and abs(sum(x) - 1) < 1e-10:
                            full_x = np.zeros(n)
                            full_x[sub_indices_col] = x
                            if check_strategy_optimality(A, full_x, False):
                                optimal_T2.append(full_x)

                    except np.linalg.LinAlgError:
                        continue

    # Удаляем дубликаты и округляем близкие к нулю значения
    optimal_T1 = [np.where(abs(p) < 1e-10, 0, p) for p in optimal_T1]
    optimal_T2 = [np.where(abs(p) < 1e-10, 0, p) for p in optimal_T2]

    optimal_T1 = [tuple(p) for p in optimal_T1]
    optimal_T2 = [tuple(p) for p in optimal_T2]

    optimal_T1 = [np.array(p) for p in set(optimal_T1)]
    optimal_T2 = [np.array(p) for p in set(optimal_T2)]

    return optimal_T1, optimal_T2


def solve_game(A):
    print("1. Исходная матрица игры:")
    print(A)
    print()

    T1_points, T2_points = find_optimal_strategies(A)

    if T1_points and T2_points:
        # Находим цену игры
        v = find_game_value(A, T1_points[0], T2_points[0])
        print(f"Цена игры: {v}")
        print()

        print("2. Оптимальные стратегии:")
        print("\nМножество T1 (для первого игрока):")
        for point in T1_points:
            print(f"({', '.join(f'{x:.3f}' for x in point)})")

        print("\nМножество T2 (для второго игрока):")
        for point in T2_points:
            print(f"({', '.join(f'{x:.3f}' for x in point)})")

        print("\n3. Аналитическое представление множеств:")
        if len(T1_points) == 2:
            print(f"Множество T1: α{tuple(T1_points[0])} + (1-α){tuple(T1_points[1])}, где 0 ≤ α ≤ 1")
        if len(T2_points) == 2:
            print(f"Множество T2: β{tuple(T2_points[0])} + (1-β){tuple(T2_points[1])}, где 0 ≤ β ≤ 1")
    else:
        print("Оптимальные стратегии не найдены")


# Пример использования
A = np.array([[3, 5, 3],
              [4, -3, 2],
              [3, 2, 3]])

solve_game(A)