
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

    _variables = dict()

    @_('line_list')
    def start(self, p):
        return p.line_list

    @_(
        'line_list line_item ";"',
        'line_item ";"',
    )
    def line_list(self, p):
        try:
            return [*p.line_list, p.line_item]
        except AttributeError:
            return [p.line_item]

    @_(
        'print_expression',
        'conditional_expression',
        'assignment_expression',
        'arithmetic_expression',
    )
    def line_item(self, p):
        return p[0]

    @_(
        'PRINT arithmetic_expression',
        'PRINT boolean_expression',
    )
    def print_expression(self, p):
        return p[1]

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
        'ID',
        'NUMBER',
        '"(" arithmetic_expression ")"',
    )
    def arithmetic_factor(self, p):
        try:
            if hasattr(p, 'NUMBER'):
                return p.NUMBER
            else:
                return self._variables[p.ID]
        except AttributeError:
            return p.arithmetic_expression
        except KeyError:
            return f"ERROR! No variables named: {p.ID}"

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

    @_('matched_conditional', 'unmatched_conditional')
    def conditional_expression(self, p):
        return p[0]

    @_(
        'IF "(" boolean_expression ")" matched_conditional ELSE matched_conditional',
        'other_conditional',
    )
    def matched_conditional(self, p):
        try:
            if p.boolean_expression == True:
                return p.matched_conditional0
            return p.matched_conditional1
        except AttributeError:
            return p[0]

    @_(
        'IF "(" boolean_expression ")" conditional_expression',
        'IF "(" boolean_expression ")" matched_conditional ELSE unmatched_conditional',
    )
    def unmatched_conditional(self, p):
        try:
            return p.matched_conditional if p.boolean_expression else p.unmatched_conditional
        except AttributeError:
            if p.boolean_expression:
                return p.conditional_expression

    @_(
        'print_expression'
    )
    def other_conditional(self, p):
        return p[0]

    @_('INT', 'VOID')
    def type_specifier(self, p):
        return p[0]

    @_(
        'type_specifier ID assignment_operator arithmetic_expression',
        'ID assignment_operator arithmetic_expression',
    )
    def assignment_expression(self, p):
        try:
            if p.type_specifier == 'void':
                return "ERROR! Invalid type 'void' for assignment"
        except AttributeError:
            pass
        self._variables[p.ID] = p.arithmetic_expression

    @_('"="')
    def assignment_operator(self, p):
        return p[0]

    """  """
    #     pass
    # @_('_RHS')
    # def _LHS(self, p):
    #     pass
