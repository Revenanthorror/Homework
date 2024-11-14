from datetime import datetime

date_str = "Wednesday, October 2, 2002"
date_format = "%A, %B %d, %Y"
date_obj = datetime.strptime(date_str, date_format)

print("The Moscow Times", date_obj)

date_str1 = "Friday, 11.10.13"
date_format1 = "%A, %d.%m.%y"
date_obj1 = datetime.strptime(date_str1, date_format1)

print("The Guardian", date_obj1)

date_str2 = "Thursday, 18 August 1977"
date_format2 = "%A, %d %B %Y"
date_obj2 = datetime.strptime(date_str2, date_format2)

print("Daily News", date_obj2)