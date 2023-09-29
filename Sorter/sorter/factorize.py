from time import time
from multiprocessing import Pool, cpu_count

numbers = [128, 255, 99999, 10651060]


def factorize(number):
    return [i for i in range(1, number + 1) if number % i == 0]


start = time()
results = list(map(factorize, numbers))
print(f"Синхронний час виконання: {time() - start} секунд")

with Pool(cpu_count()) as pool:
    start = time()
    results = pool.map(factorize, numbers)
print(f"Параллельний час виконання: {time() - start} секунд")

# Проверка результатов
assert results[0] == [1, 2, 4, 8, 16, 32, 64, 128]
assert results[1] == [1, 3, 5, 15, 17, 51, 85, 255]
assert results[2] == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert results[3] == [
    1,
    2,
    4,
    5,
    7,
    10,
    14,
    20,
    28,
    35,
    70,
    140,
    76079,
    152158,
    304316,
    380395,
    532553,
    760790,
    1065106,
    1521580,
    2130212,
    2662765,
    5325530,
    10651060,
]
