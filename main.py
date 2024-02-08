import sys
import os


file = sys.argv[1]
_, file_extension = os.path.splitext(file)


class SyntaxException(Exception):
    def __init__(self, message):
        self.message = message


def input_command(line_data):
    return input(translate_line(line_data))


def say_command(args):
    rendered_text = ""
    for arg in args:
        # Проверяем, является ли аргумент строковым литералом
        if isinstance(arg, str) and (arg.startswith('"') or arg.startswith("'")):
            # Убираем кавычки из строкового литерала и добавляем его к тексту
            rendered_text += arg[1:-1] + ' '
        else:
            # Обрабатываем аргумент как команду
            rendered_text += translate_line(arg) + ' '
    print(rendered_text.strip())


COMMANDS = {'сказать': say_command, 'ввести': input_command}


def translate(file):
    with open(file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            translate_line(line)


def translate_line(line):
    if isinstance(line, list):
        # Если line - список, обрабатываем каждый элемент списка
        return ' '.join([translate_line(item) for item in line])

    else:
        line = line.strip()
        if line.startswith('"') or line.startswith("'"):
            # Обработка строкового литерала
            return line[1:-1]
        # Разбор команды и её аргументов
        if '(' in line and ')' in line:
            split_line = line.split('(', 1)
            cmnd = split_line[0].strip()
            args = split_line[1].rstrip(')').strip() if len(split_line) > 1 else None
            if cmnd in COMMANDS:
                if args:
                    args = split_args(args)  # Разбиение аргументов
                return COMMANDS[cmnd](args)
            else:
                raise SyntaxException(f'No command is recognized: {cmnd}')
        else:
            # Строка не является командой и не начинается с кавычек - вероятно, это ошибка
            raise SyntaxException(f'No command is recognized: {line}')


def split_args(args):
    args_list = []
    current_arg = ""
    bracket_level = 0
    in_quotes = False
    quote_char = ''

    for char in args:
        if char in ("'", '"') and not in_quotes:
            # Начало строки в кавычках
            in_quotes = True
            quote_char = char
            current_arg += char
        elif char == quote_char and in_quotes:
            # Конец строки в кавычках
            in_quotes = False
            current_arg += char
        elif not in_quotes and char == '(':
            # Увеличиваем уровень вложенности скобок
            bracket_level += 1
            current_arg += char
        elif not in_quotes and char == ')' and bracket_level > 0:
            # Уменьшаем уровень вложенности скобок
            bracket_level -= 1
            current_arg += char
        elif not in_quotes and char == ',' and bracket_level == 0:
            # Конец текущего аргумента
            args_list.append(current_arg.strip())
            current_arg = ""
        else:
            # Добавляем символ к текущему аргументу
            current_arg += char

    # Добавляем последний аргумент, если он есть
    if current_arg:
        args_list.append(current_arg.strip())

    return args_list


if file_extension != '.prt':
    print('This file does not supported')
else:
    translate(file)
