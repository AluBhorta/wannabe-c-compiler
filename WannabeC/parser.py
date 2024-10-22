
from sly import Parser

from .lexer import WannabeCLexer


class WannabeCParser(Parser):
    tokens = WannabeCLexer.tokens
    precedence = (
        ('right', 'THEN'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
    )
    _variables = dict()
    debugfile = "parser-debug.log"

    @_('function_definition', 'line_list')
    def start(self, p):
        return p[0]

    @_(
        'type_specifier ID "(" ")" "{" line_list "}"',
        'type_specifier ID "(" ")" "{" "}"',
    )
    def function_definition(self, p):
        try:
            return_vals = []
            if p.type_specifier == 'int':
                for item in p.line_list:
                    if isinstance(item, tuple) and item[0] == 'RETURN':
                        if isinstance(item[1], int):
                            return_vals.append(item[1])
                        else:
                            return_vals.append(
                                "ERROR! Invalid return type for 'int'!")
                        break
                    else:
                        return_vals.append(item)
                return return_vals

            if p.type_specifier == 'void':
                for item in p.line_list:
                    if isinstance(item, tuple) and item[0] == 'RETURN':
                        if len(item) > 1:
                            return ["ERROR! Type 'void' cannot have return values!"]
                        break
                    else:
                        return_vals.append(item)
                return return_vals
        except AttributeError:
            return []

    @_(
        'line_list line_item',
        'line_item',
    )
    def line_list(self, p):
        try:
            return [*p.line_list, p.line_item]
        except AttributeError:
            return [p.line_item]

    @_(
        'print_expression ";"',
        'conditional_expression ";"',
        'assignment_expression ";"',
        'arithmetic_expression ";"',
        'return_expression ";"',
    )
    def line_item(self, p):
        return p[0]

    @_(
        'RETURN',
        'RETURN arithmetic_expression',
    )
    def return_expression(self, p):
        try:
            return ('RETURN', p[1])
        except IndexError:
            return ('RETURN',)

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
        '"{" other_conditional "}"',
        'other_conditional',
    )
    def matched_conditional(self, p):
        try:
            if p.boolean_expression == True:
                return p.matched_conditional0
            return p.matched_conditional1
        except AttributeError:
            return p.other_conditional

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
        'print_expression %prec THEN',
        'return_expression %prec THEN',
        'assignment_expression %prec THEN',
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
            if not hasattr(p, 'type_specifier') and p.ID not in self._variables.keys():
                return f"ERROR! Type required for '{p.ID}'. (Not really, but let's just pretend it's C 🤷)"
            if p.type_specifier == 'void':
                return "ERROR! Invalid type 'void' for assignment"
            if hasattr(p, 'type_specifier') and p.ID in self._variables.keys():
                return f"ERROR! Variable '{p.ID}' already defined"
            self._variables[p.ID] = p.arithmetic_expression
        except AttributeError:
            pass

    @_('"="')
    def assignment_operator(self, p):
        return p[0]
