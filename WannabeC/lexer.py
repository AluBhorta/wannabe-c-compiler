
from sly import Lexer


class WannabeCLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { 
        NUMBER, ID, IF, ELSE, EQUALS, 
        LTOE, GTOE, NOTEQ, INCR, DECR,
        AND, OR, ADDASSIGN, SUBTASSIGN, 
        MULTASSIGN, DIVASSIGN, MODASSIGN, 
        RETURN, INT, VOID
    }

    literals = {
        '(', ')', '{', '}', ';', 
        '+', '-', '*', '/', '%', 
        '<', '>', '='
    }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    INCR            = r'\+\+' 
    DECR            = r'--' 
    AND             = r'&&' 
    OR              = r'\|\|' 
    ADDASSIGN       = r'\+=' 
    SUBTASSIGN      = r'-=' 
    MULTASSIGN      = r'\*='
    DIVASSIGN       = r'/=' 
    MODASSIGN       = r'%='
    EQUALS          = r'=='
    LTOE            = r'<='
    GTOE            = r'>='
    NOTEQ           = r'!='


    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if']        = IF
    ID['else']      = ELSE
    ID['return']    = RETURN
    ID['int']       = INT
    ID['void']      = VOID

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
