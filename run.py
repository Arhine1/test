import sys
import csv
import argparse
import field_class
import time
from random import getrandbits


# Обработка параметров командной строки
def create_parser():
    pars = argparse.ArgumentParser()
    subparsers = pars.add_subparsers(dest='command')

    random_parser = subparsers.add_parser('random')
    random_parser.add_argument('-m', default=30, type=int)
    random_parser.add_argument('-n', default=30, type=int)

    file_parser = subparsers.add_parser('file')
    file_parser.add_argument('file_name', type=argparse.FileType())

    return pars


# Случайное заполнение доски
def create_random(m, n):
    life_list = [[bool(getrandbits(1)) for j in range(n)] for i in range(m)]
    return life_list


# Заполнение доски из csv файла
def create_from_file(f):
    reader = csv.reader(f)
    life_list = list()
    c = 0
    for row in reader:
        life_list.append([])
        c += 1
        for column in row:
            if column == '1':
                life_list[c - 1].append(True)
            elif column == '0':
                life_list[c - 1].append(False)
            else:
                print('Unknown file contents')
                sys.exit(1)
    return life_list


# Логика изменения состояния
# Возвращает новое состояние доски
def action(state):
    new_state = list()
    count = 0
    for i in range(len(state)):
        new_state.append([])
        for j in range(len(state[i])):

            for n in range(3):
                for k in range(3):
                    if ((i - 1 + n) in range(len(state))) and ((j - 1 + k) in range(len(state[i]))):
                        if state[i - 1 + n][j - 1 + k] and not (n == 1 and k == 1):
                            count += 1

            if not state[i][j] and count == 3:
                new_state[i].append(True)
            elif not state[i][j] and count != 3:
                new_state[i].append(False)
            elif state[i][j] and (count < 2 or count > 3):
                new_state[i].append(False)
            elif state[i][j] and (count == 2 or count == 3):
                new_state[i].append(True)
            count = 0
    return new_state


#  Точка входа в программу
if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    if namespace.command == 'random':
        field = field_class.Field(create_random(namespace.m, namespace.n))
    elif namespace.command == 'file':
        with namespace.file_name as file:
            field = field_class.Field(create_from_file(file))
    else:
        print('Please enter command line arguments')
        print('-h for help')
        sys.exit(1)

    # Вывод состояния доски в консоль с паузой в 1 секунду
    while True:
        new_field = action(field.state)
        field.set(new_field)

        for line in field.state:
            print(line)
        print('\n')
        time.sleep(1)
