
from sly import Lexer


class WannabeCLexer(Lexer):
    tokens = {
        NUMBER, PRINT
    }

    literals = {
        '+', '-', '*', '/', '%', '(', ')'
    }

    PRINT = 'print'

    ignore = ' \t\n'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t