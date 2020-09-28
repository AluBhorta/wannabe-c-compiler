
from pprint import pprint
from sly import Parser

from .lexer import WannabeCLexer

class WannabeCParser(Parser):
    debugfile = "parser-debug2.log"
    # start = 'start'

    tokens = WannabeCLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
    )

    @_('expression')
    def start(self, p):
        return p.expression

    @_(
        'PRINT arithmetic_expression',
        'arithmetic_expression'
    )
    def expression(self, p):
        return p.arithmetic_expression


    @_(
        'arithmetic_expression "+" arithmetic_term',
        'arithmetic_expression "-" arithmetic_term',
        'arithmetic_term',
    )
    def arithmetic_expression(self, p):
        try:
            if p[1] == '+':
                return p.arithmetic_expression + p.arithmetic_term
            elif p[1] == '-':
                return p.arithmetic_expression - p.arithmetic_term
            else:
                raise Exception("Invalid Operator!")
        except IndexError or AttributeError:
            return p.arithmetic_term

    @_(
        'arithmetic_term "%" arithmetic_factor',
        'arithmetic_term "/" arithmetic_factor',
        'arithmetic_term "*" arithmetic_factor',
        'arithmetic_factor',
    )
    def arithmetic_term(self, p):
        try:
            if p[1] == '*':
                return p.arithmetic_term * p.arithmetic_factor
            elif p[1] == '/':
                return p.arithmetic_term / p.arithmetic_factor
            elif p[1] == '%':
                return p.arithmetic_term % p.arithmetic_factor
            else:
                raise Exception("Invalid Operator!")
        except IndexError or AttributeError:
            return p.arithmetic_factor

    @_(
        'NUMBER',
        '"(" arithmetic_expression ")"',
    )
    def arithmetic_factor(self, p):
        try:
            return p.NUMBER
        except AttributeError:
            return p.arithmetic_expression

    """  """
    # @_('_RHS')
    # def _LHS(self, p):
    #     pass
