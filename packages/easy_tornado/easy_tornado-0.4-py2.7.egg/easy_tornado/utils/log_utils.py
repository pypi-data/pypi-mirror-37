# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/10/30 14:29
import sys


def _add_indent(lines, space_cnt):
    """
    add blank before message

    :param lines: lines to be operated
    :type lines: Iterable of str

    :param space_cnt: space number
    :type space_cnt: int

    :return: lines with each started with space_cnt blanks
    """
    s = lines.split('\n')
    # don't do anything for single-line stuff
    if len(s) == 1:
        return lines
    first = s.pop(0)
    s = [(space_cnt * ' ') + line for line in s]
    s = '\n'.join(s)
    s = first + '\n' + s
    return s


def it_print(message=None, indent=0, device=1, newline=True):
    """
    in time print: print one line to console immediately

    :param message: the message to be printed
    :type message: str

    :param indent: number of blank to be indented, default 0
    :type indent: int

    :param device: stdout -> 1, stderr -> 2, default 1
    :type device: int

    :param newline: whether to append a new line, default True
    :type newline: bool
    """
    if message is None:
        message = ''
    message = ' ' * indent + message

    if device == 2:
        device = sys.stderr
    else:
        device = sys.stdout

    device.write(message)
    if newline:
        device.write('\n')
    device.flush()


def it_prints(message=None, indent=0, indent_inner=2, device=1, newline=True):
    """
    in time print multiple lines: first indent with indent blanks, then every line is indented with indent_inner blanks
    """
    if message is not None:
        message = _add_indent(message, indent_inner)
    it_print(message, indent=indent, device=device, newline=newline)
