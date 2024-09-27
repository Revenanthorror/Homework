b = input("Парни: ")
b = b.split()
g = input("Девушки: ")
g = g.split()
b = sorted(b)
g = sorted(g)
if b and g:
    print("Идеальные пары: ")
    for i in range(min(len(g), len(b))):
        print(b[i] + " и " + g[i])
