import csv
with open('C:/PyProject/visit_log (2).csv', 'r') as f:
    reader = csv.DictReader(f)
    with open('C:/PyProject/funnel.csv', 'w') as f:
        header = ["user_id", "source", "products"]
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for i in reader:
            if "context" in i["source"]:
                writer.writerow(i)
                print(i)
