
from pprint import pprint
from sly import Parser

from .lexer import WannabeCLexer

class WannabeCParser(Parser):
    debugfile = "parser-debug.log"

    _variables = dict()

    tokens = WannabeCLexer.tokens

    @_('type_specifier ID "(" declarator_list ")" block_body')
    def function_definition(self, p):
        if p.type_specifier == 'int':
            return p.block_body
        return
    
    @_('declarator_list "," declarator', 'declarator')
    def declarator_list(self, p):
        try:
            if p.declarator_list:
                return (*p.declarator_list, p.declarator)
        except AttributeError:
            return (p.declarator,)

    @_('type_specifier ID')
    def declarator(self, p):
        return (p.type_specifier, p.ID)

    @_('empty')
    def declarator(self, p):
        pass

    @_('')
    def empty(self, p):
        pass
    
    @_('INT', 'VOID')
    def type_specifier(self, p):
        return p[0]
    
    @_(
        '"{" "}"', 
        '"{" block_item_list "}"'
    )
    def block_body(self, p):
        try:
            if p.block_item_list:
                for bi in p.block_item_list:
                    if bi[0] == 'RETURN':
                        return bi[1]
            return
        except AttributeError:
            return
        
    @_(
        'block_item', 
        'block_item_list block_item'
    )
    def block_item_list(self, p):
        try:
            if p.block_item_list:
                return (*p.block_item_list, p.block_item)
        except AttributeError:
            return (p.block_item,)
    
    @_('";"', 'expression ";"')
    def block_item(self, p):
        try:
            if p.expression:
                # print(p.expression)
                return p.expression
        except AttributeError:
            pass
    
    @_(
        'arithmetic_expression',
        'assignment_expression',
        'unary_expression',
        'boolean_expression',
        'conditional_expression',
        'return_expression',
    )
    def expression(self, p):
        return p[0]
    
    @_(
        'arithmetic_expression "+" arithmetic_term', 
        'arithmetic_expression "-" arithmetic_term',
        'arithmetic_term'
    )
    def arithmetic_expression(self, p):
        try:
            if p.arithmetic_expression:
                if p[1] == '+':
                    return p.arithmetic_expression + p.arithmetic_term
                elif p[1] == '-':
                    return p.arithmetic_expression - p.arithmetic_term
                else:
                    raise Exception(f"Invalid arithmetic_expression operator {p[1]}")
        except AttributeError:
            return (p.arithmetic_term)

    # @_(
    #     'ID "+" ID', 
    #     'ID "-" ID', 
    # )
    # def arithmetic_expression(self, p):
    #     if p[1] == '+':
    #         return self._variables[p[0]] + self._variables[p[2]]
    #     else:
    #         return self._variables[p[0]] - self._variables[p[2]]

    @_(
        'arithmetic_term "%" arithmetic_factor',
        'arithmetic_term "/" arithmetic_factor',
        'arithmetic_term "*" arithmetic_factor',
        'arithmetic_factor',
    )
    def arithmetic_term(self, p):
        try:
            if p.arithmetic_term:
                return (p[1], p.arithmetic_term, p.arithmetic_factor)
        except AttributeError:
            return (p.arithmetic_factor)

    # @_(
    #     'ID "%" ID',
    #     'ID "/" ID',
    #     'ID "*" ID',
    # )
    # def arithmetic_term(self, p):
    #     if p[1] == '%':
    #         return self._variables[p[0]] % self._variables[p[2]]
    #     elif p[1] == '/':
    #         return self._variables[p[0]] / self._variables[p[2]]
    #     elif p[1] == '*':
    #         return self._variables[p[0]] * self._variables[p[2]]
    #     else:
    #         raise Exception(f"Invalid operator {p[1]}!")


    @_(
        'NUMBER',
        'ID',
        '"(" arithmetic_expression ")"'
    )
    def arithmetic_factor(self, p):
        try:
            return p.arithmetic_expression
        except AttributeError:
            return int(p.NUMBER)
        else:
            return self._variables[p.ID]

    @_(
        'declarator assignment_operator expression',
        'ID assignment_operator expression',
    )
    def assignment_expression(self, p):
        try:
            self._variables[p.declarator[1]] = p.expression
            if p.declarator:
                return (p.declarator, p.assignment_operator, p.expression)
        except AttributeError:
            self._variables[p.ID] = p.expression
            return (p.ID, p.assignment_operator, p.expression)
    
    @_(
        '"="',
        'ADDASSIGN',
        'SUBTASSIGN',
        'MULTASSIGN',
        'DIVASSIGN',
        'MODASSIGN',
    )
    def assignment_operator(self, p):
        return p[0]
    
    @_(
        'RETURN arithmetic_expression',
        'RETURN unary_expression',
        'RETURN',
    )
    def return_expression(self, p):
        try:
            return ('RETURN', p[1])
        except AttributeError:
            return
    
    @_(
        'unary_operator ID',
        'ID unary_operator',
        'ID',
    )
    def unary_expression(self, p):
        try:
            if p.unary_operator:
                return (p[0], p[1])
        except AttributeError:
            return p.ID
    
    @_('INCR', 'DECR')
    def unary_operator(self, p):
        return p[0]
    
    @_(
        'expression boolean_operator expression',
    )
    def boolean_expression(self, p):
        return (p[0], p[1], p[2])
    
    @_(
        'AND',
        'OR',
        'EQUALS',
        'LTOE',
        'GTOE',
        'NOTEQ',
    )
    def boolean_operator(self, p):
        return p[0]
    
    @_(
        'IF "(" boolean_expression ")" expression ELSE expression',
        'IF "(" boolean_expression ")" expression',
    )
    def conditional_expression(self, p):
        try:
            if p.ELSE:
                return ('IF "(" boolean_expression ")" expression ELSE expression')
        except AttributeError:
            return ('IF "(" boolean_expression ")" expression')
    
