documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]
directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}
def p():
    print('Поиск имени по номеру документа')
    num = input('введите номер документа ')
    for num1 in documents:
        if num1['number'] == num:
            print('Имя:', num1['name'])
def s():
    print('Поиск полки документа')
    num = input('введите номер документа ')
    for num1 in documents:
        if num1['number'] == num:
            for nkey, nvalue in directories.items():
                if num in nvalue:
                    print('полка номер:', nkey)
fun = {
    'p': p,
    's': s,
}
def proverka():
    print(
        "\np - Показать имя человека по номеру документа, "
        "\ns - Показать номер полки по номеру документа"
       )
    a = input('\nвведите команду: ')
    if a.lower().strip() in {'p','s'}:
        return a.lower().strip()
def asd():
    while True:
        print('Команды:')
        qwe = proverka()
        if qwe:
            print('')
            fun[qwe]()
            break
asd()