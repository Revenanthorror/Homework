x = int(input("Введите номер билета:  "))
if 100_000 <= x <= 999_999:
    a1 = x // 100_000
    a2 = x // 10_000 % 10
    a3 = x // 1_000 % 10
    sum_a = a1+a2+a3
    b1 = x % 10
    b2 = x % 100 // 10
    b3 = x % 1000 // 100
    sum_b = b1+b2+b3
    if sum_a == sum_b:
        print("number = ",x)
        print("Результат:  ")
        print("Счастливый билет")
    else:
        print("number = ",x)
        print("Результат:  ")
        print("Несчастливый билет")