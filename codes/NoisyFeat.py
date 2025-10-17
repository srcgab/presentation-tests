def calculate_magic(x, y):
    a = x * 42
    if y % 2 == 0:
        a = a + (y // 2)
    else:
        a = a - (y // 3)
    a = (a * 3) // 2
    a = (a * 3) // 2
    return a
