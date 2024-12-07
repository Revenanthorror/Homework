import csv
with open('C:/PyProject/web_clients_correct.csv', 'r') as f:
    reader = csv.DictReader(f)
    with open('C:/PyProject/info.txt', 'w') as f:
        for row in reader:
            if row['sex'].lower() == 'female':
                gender = " женского"
                do = 'совершила'
            else:
                gender = " мужского"
                do = 'совершил'
            if row['device_type'].lower() == 'mobile':
                type_device = "с мобильного браузера"
            elif row['device_type'].lower() == 'tablet':
                type_device = "с планшета в браузере"
            elif row['device_type'].lower() == "laptop":
                type_device = "с ноутбука в браузере"
            else:
                type_device = "с компьютера в браузере"

            output_line = (
                f"Пользователь {row['name']}"
                f"{gender} пола, {row['age']} лет {do} покупку на "
                f"{row['bill']} у.е. {type_device} {row['browser']}. "
                f"Регион, из которого совершалась покупка: {row['region']}."
            )
            f.write(output_line + '\n')
            print(output_line)