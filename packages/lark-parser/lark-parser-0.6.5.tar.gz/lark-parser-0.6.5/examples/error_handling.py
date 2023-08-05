#
# This example demonstrates handling parse errors
#
from lark import Lark, UnexpectedToken, Token

from .json_parser import json_grammar   # Using the grammar from the json_parser example

def on_err(exception):
    if 'COMMA' in exception.expected:
        return Token('COMMA', ',')
    else:
        raise exception

parser = Lark(json_grammar, parser='lalr', lexer='standard', on_parse_error=on_err)

print(parser.parse('[1,2 3]'))