import re

main_data = ('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')
where_looking = ('info_1.txt', 'info_2.txt', 'info_3.txt')
os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []


def write_to_csv():
    for source in where_looking:
        get_data(main_data, source)
    

def get_data(what, where):
    with open(where, encoding='cp1251') as FD:
        for line in FD:
            for find_literal in what:
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


def write_order_to_json():
    pass


write_to_csv()
