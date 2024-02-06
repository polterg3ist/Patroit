import sys
import os
import re

file = sys.argv[1]
_, file_extension = os.path.splitext(file)


class SyntaxException(Exception):
    def __init__(self, message):
        self.message = message


def say_command(line_data):
    # TODO: Replace this with something better. RegExp below can be used.
    # exp = 'сказать "Привет", "Как дела"'
    # pattern = r'"(.*?)"'
    # res = re.findall(pattern, exp)
    #
    func_args = line_data.split(', ')
    rendered_text = ""
    for arg in func_args:
        rendered_text += translate_line(arg) + ' '
    return print(rendered_text)


def input_command(line_data):
    return input(translate_line(line_data))


COMMANDS = {'сказать': say_command, 'ввести': input_command}


def translate(file):
    with open(file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            translate_line(line)


def translate_line(line):
    split_line = line.split(' ', 1)
    cmnd = split_line[0]
    other = split_line[1] if len(split_line) > 1 else None

    if cmnd in COMMANDS:
        returned_from_command = COMMANDS[cmnd](other)
        return returned_from_command

    elif cmnd.startswith('"') or cmnd.startswith("'"):
        text_start_sym = "'" if cmnd.startswith("'") else '"'
        text = ""

        for sym in line[1:]:
            if sym != text_start_sym:
                text += sym
            else:
                return text
    else:
        raise SyntaxException('No command is recognized')


if file_extension != '.prt':
    print('This file does not supported')
else:
    translate(file)
