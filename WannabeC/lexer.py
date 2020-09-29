
from sly import Lexer


class WannabeCLexer(Lexer):
    tokens = {
        NUMBER, PRINT, ID, IF, ELSE,
        AND, OR, EQUALS, LTOE, GTOE, 
        NOTEQ, LT, GT, INT, VOID,
    }

    literals = {
        '+', '-', '*', '/', '%', 
        '(', ')', ';', '=', '{', '}'
    }
    
    AND             = r'&&'
    OR              = r'\|\|'
    EQUALS          = r'=='
    LTOE            = r'<='
    GTOE            = r'>='
    NOTEQ           = r'!='
    LT              = r'<'
    GT              = r'>'

    ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if']        = IF
    ID['else']      = ELSE
    ID['print']     = PRINT
    ID['int']       = INT
    ID['void']      = VOID

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    ignore = ' \t'
    ignore_comment = r'//.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
