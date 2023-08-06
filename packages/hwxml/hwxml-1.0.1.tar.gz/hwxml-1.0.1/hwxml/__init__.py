# -*- coding: utf-8 -*-

from . import parser

def parse(str_input):
    return parser.parser(str_input).parse()
