from math import floor

import numpy as np


def create_matrix(n):
    matrix = 0
    while np.sum(matrix) != 1:
        matrix = np.random.randint(0, 101, size=(n, n)).astype(float) / 100
        matrix /= np.sum(matrix)
        matrix = np.round(matrix, 2)
    np.set_printoptions(suppress=True)
    return matrix


def print_matrix(matrix, n):
    # вивести матрицю + суму по лініях
    for i in range(n):
        print(f"{matrix[i]} | {np.round(np.sum(matrix[i]), 2)}")
    # вивести суму по стовбцям
    print('_' * 5 * n)
    print(' ', end='')
    for i in range(n):
        value = np.round(np.sum(matrix[:, i]), 2)
        separator = ' ' if value * 100 % 10 == 0 else ''
        print(f'{value}{separator}', end=' ')


def compute_entropy(arr, size):
    # Підсумовуємо стовбці та рядки
    y_arr = np.sum(arr, axis=1)
    x_arr = np.sum(arr, axis=0)

    # Обчислюємо безумовну ентропію
    H_X = -np.sum(x_arr * np.log2(x_arr[x_arr != 0]))
    H_Y = -np.sum(y_arr * np.log2(y_arr[y_arr != 0]))

    # Обчислюємо взаємну ентропію
    non_zero_values = arr[arr != 0]
    H_XY = -np.sum(non_zero_values * np.log2(non_zero_values))

    # Обчислюємо умовну ентропію H(X|Y) та (Y|X)
    H_X_Y = 0
    H_Y_X = 0
    p_yx_arr = np.zeros((size, size))
    p_xy_arr = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if y_arr[i] != 0 and arr[i, j] != 0:
                p_yx = arr[i, j] / y_arr[i]
                p_yx_arr[i, j] = p_yx
                H_X_Y -= y_arr[i] * p_yx * np.log2(p_yx)
            if x_arr[i] != 0 and arr[i, j] != 0:
                p_xy = arr[i, j] / x_arr[j]
                p_xy_arr[i, j] = p_xy
                H_Y_X -= x_arr[j] * p_xy * np.log2(p_xy)

    return x_arr, y_arr, p_xy_arr, p_yx_arr, H_X, H_Y, H_XY, H_X_Y, H_Y_X


if __name__ == "__main__":
    n = 10
    start_alphxyet = create_matrix(n)  # стартовий алфавіт
    # Вивід алфавітів
    print("Стартовий алфавіт:")
    print_matrix(start_alphxyet, n)
    x_arr, y_arr, p_xy_arr, p_yx_arr, H_X, H_Y, H_XY, H_X_Y, H_Y_X = compute_entropy(start_alphxyet, n)

    print(f"\n\n\t\t\t\tp(X)\n{np.round(x_arr, 2)}\n")
    print(f"\n\t\t\t\tp(Y)\n{np.round(y_arr, 2)}\n")
    print(f"\n\t\t\t\tp(X/Y)\n{np.round(p_xy_arr, 2)}\n")
    print(f"\n\t\t\t\tp(Y/X)\n{np.round(p_yx_arr, 2)}\n")

    H_X = floor(round(H_X, 1) * 10) / 10
    H_Y = floor(round(H_Y, 1) * 10) / 10
    H_XY = floor(round(H_XY, 1) * 10) / 10
    H_X_Y = floor(round(H_X_Y, 1) * 10) / 10
    H_Y_X = floor(round(H_Y_X, 1) * 10) / 10
    # Вивід результатів обчислень на екран
    print()
    print(f"H(X):\t{H_X} біт")
    print(f"H(Y):\t{H_Y} біт")
    print(f"H(X,Y):\t{H_XY} біт")
    print(f"H(X|Y):\t{H_X_Y} біт")
    print(f"H(Y|X):\t{H_Y_X} біт")
    print("\t\t\t\t****Проверка****")
    print(f"H(X,Y) = H(X) + H(X/Y) = H(Y) + H(Y/X) \n"
          f"{np.round(H_XY, 1)} біт = {H_X} + {H_X_Y} = {H_Y} + {H_Y_X}")
    print(f"H(X/Y) = H(X, Y) - H(Y)\n{floor((H_XY - H_Y) * 10) / 10} біт = {H_XY} - {H_Y}")
    print(f"H(Y/X) = H(X, Y) - H(X)\n{floor((H_XY - H_X) * 10) / 10} біт = {H_XY} - {H_X}")
