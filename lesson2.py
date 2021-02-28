import json
import re

where_looking = ('info_1.txt', 'info_2.txt', 'info_3.txt')


def write_to_csv(where):
    content = get_data(where_looking, 'Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')
    with open(where, 'w') as FD:
        count = 0
        FD.write(';'.join(content[0]))
        while count < len(content[1]):
            data = []
            for item in range(4):
                data.append(content[item + 1][count])
            FD.write(';'.join(data))
            count += 1


def get_data(where, *args):
    main_data = [*args]
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    for source in where:
        with open(source, encoding='cp1251') as FD:
            for line in FD:
                for find_literal in main_data:
                    # из считанных данных извлекаем значения параметров
                    match = re.findall(find_literal, line)
                    if match:
                        key, value = re.split(':', line)
                        if key == main_data[0]:
                            os_prod_list.append(value.strip())
                        if key == main_data[1]:
                            os_name_list.append(value.strip())
                        if key == main_data[2]:
                            os_code_list.append(value.strip())
                        if key == main_data[3]:
                            os_type_list.append(value.strip())
        # with open(source+'.csv', 'w') as FD:

    return main_data, os_prod_list, os_name_list, os_code_list, os_type_list


def write_order_to_json(item, quantity, price, buyer, date):
    # {"orders": []}
    with open('orders.json') as FD:
        content = json.load(FD)
    content["orders"].append({"item": item, "quantity": quantity, "price": price, "buyer": buyer, "date": date})
    print(content)
    with open('orders.json', 'w') as FD:
        FD.write(json.dumps(content, indent=4))


# write_to_csv('main_data.csv')
# write_order_to_json('Mouse', '5', '1500', 'Alex Byuer', '23.02.2021')
# write_order_to_json('Notebook', '1', '15000', 'Mr. Black', '03.02.2021')
# write_order_to_json('Lamp', '10', '10', 'Bob Charley', '20.01.2021')
# write_order_to_json('Red Rose', '500', '35', 'Angelica Smith', '11.01.2021')
