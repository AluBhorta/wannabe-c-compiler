
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
        'print_expression',
        'arithmetic_expression',
        'boolean_expression'
    )
    def expression(self, p):
        return p[0]

    @_(
        'PRINT expression',
    )
    def print_expression(self, p):
        print(p.expression)
        return None

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

    @_('arithmetic_expression boolean_operator arithmetic_expression')
    def boolean_expression(self, p):
        return {
            '&&': p.arithmetic_expression0 and p.arithmetic_expression1,
            '||': p.arithmetic_expression0 or p.arithmetic_expression1,
            '==': p.arithmetic_expression0 == p.arithmetic_expression1,
            '<=': p.arithmetic_expression0 <= p.arithmetic_expression1,
            '>=': p.arithmetic_expression0 >= p.arithmetic_expression1,
            '!=': p.arithmetic_expression0 != p.arithmetic_expression1,
            '<':  p.arithmetic_expression0 < p.arithmetic_expression1,
            '>':  p.arithmetic_expression0 > p.arithmetic_expression1,
        }[p.boolean_operator]

    @_("AND", "OR", "EQUALS", "LTOE", "GTOE", "NOTEQ", "LT", "GT")
    def boolean_operator(self, p):
        return p[0]

    """  """
    # @_('_RHS')
    # def _LHS(self, p):
    #     pass
