import sys
import os

file = sys.argv[1]
_, file_extension = os.path.splitext(file)


class MissingQuoteException(Exception):
    def __init__(self, message):
        self.message = message


def say_command(line_data):
    line_data = " ".join(line_data)
    if line_data[0] == "'" and line_data[-1] == "'" or line_data[0] == '"' and line_data[-1] == '"':
        return print(line_data[1:-1])
    else:
        return print(translate_line(line_data))


def input_command(line_data):
    line_data = " ".join(line_data)
    if line_data[0] == "'" and line_data[-1] == "'" or line_data[0] == '"' and line_data[-1] == '"':
        user_input = input(line_data[1:-1])
        return user_input
    else:
        return print(translate_line(line_data))


COMMANDS = {'сказать': say_command, 'ввести': input_command}


def translate(file):
    with open(file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            translate_line(line)


def translate_line(line):
    operands = line.split()
    for ind, operand in enumerate(operands):
        if operand in COMMANDS:
            returned_from_command = COMMANDS[operand](operands[ind + 1:])
            return returned_from_command

        #if operand.startswith('"') or operand.startswith("'"):
        #    text_start, text_end = ind,


if file_extension != '.prt':
    print('This file does not supported')
else:
    translate(file)
