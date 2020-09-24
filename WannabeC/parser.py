
from sly import Parser

from .lexer import WannabeCLexer

class WannabeCParser(Parser):
    debugfile = "parser.debug.log"

    # Get the token list from the lexer (required)
    tokens = WannabeCLexer.tokens

    # Grammar rules and actions
    @_(
        'type_specifier ID "(" declarator_list ")" block_body',
    )
    def function_definition(self, p):
        print(p._stack)
        if p.type_specifier == 'INT':
            return print(p.block_body)
        return
    
    @_(
        'declarator_list "," declarator', 
        'declarator'
    )
    def declarator_list(self, p):
        pass
        
    @_('type_specifier ID', 'empty')
    def declarator(self, p):
        pass

    @_('')
    def empty(self, p):
        pass
    
    @_('INT', 'VOID')
    def type_specifier(self, p):
        pass
    
    @_(
        '"{" "}"', 
        '"{" block_item_list "}"'
    )
    def block_body(self, p):
        pass
        
    @_(
        'block_item', 
        'block_item_list block_item'
    )
    def block_item_list(self, p):
        pass
    
    @_('";"', 'expression ";"')
    def block_item(self, p):
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
        pass
    
    @_(
        'arithmetic_expression "+" arithmetic_term', 
        'arithmetic_expression "-" arithmetic_term',
        'arithmetic_term'
    )
    def arithmetic_expression(self, p):
        print("arithmetic_expression", p)
        return (p[1], p.arithmetic_expression, p.arithmetic_term)

    @_(
        'arithmetic_term "%" arithmetic_factor',
        'arithmetic_term "/" arithmetic_factor',
        'arithmetic_term "*" arithmetic_factor',
        'arithmetic_factor',
    )
    def arithmetic_term(self, p):
        print("arithmetic_term",p)
        return (p[1], p.arithmetic_term, p.arithmetic_factor)

    @_('NUMBER', '"(" arithmetic_expression ")"')
    def arithmetic_factor(self, p):
        print("arithmetic_factor", p)
        return p[0]
    
    @_(
        'declarator assignment_operator expression',
        'ID assignment_operator expression',
        'assignment_expression "," assignment_expression',
    )
    def assignment_expression(self, p):
        pass
    
    @_(
        'ADDASSIGN',
        'SUBTASSIGN',
        'MULTASSIGN',
        'DIVASSIGN',
        'MODASSIGN',
    )
    def assignment_operator(self, p):
        pass
    
    @_(
        'RETURN expression',
        'RETURN',
    )
    def return_expression(self, p):
        pass
    
    @_(
        'unary_operator ID',
        'ID unary_operator',
        'ID',
    )
    def unary_expression(self, p):
        pass

    
    @_('INCR', 'DECR')
    def unary_operator(self, p):
        pass
    
    @_(
        'expression boolean_operator expression',
        'unary_expression',
    )
    def boolean_expression(self, p):
        pass
    
    @_(
        'AND',
        'OR',
        'EQUALS',
        'LTOE',
        'GTOE',
        'NOTEQ',
    )
    def boolean_operator(self, p):
        pass
    
    @_(
        'IF "(" boolean_expression ")" expression ELSE expression',
        'IF "(" boolean_expression ")" expression',
    )
    def conditional_expression(self, p):
        pass
    
