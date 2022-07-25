def timer_decor(func):
    import time
    count = 0

    def wrapper(*args, **kwargs):
        nonlocal count
        start = time.monotonic()
        func(*args, **kwargs)
        count += 1
        print(f'{time.monotonic() - start}, count')

        return func(*args, **kwargs)    # Вот про такой момент я хотел уточнить
    return wrapper


@timer_decor
def factorial_rec(num):
    if num == 1:
        return num
    return num * factorial_rec(num-1)


@timer_decor
def factorial_cyc(num):
    res = num
    for i in range(num-1, 0, -1):
        res *= i
    return res


print(factorial_cyc(6))

print(factorial_rec(3))       # с рекурсивными функциями получается слишком много вызовов