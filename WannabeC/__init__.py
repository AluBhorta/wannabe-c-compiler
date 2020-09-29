import readline
from pprint import pprint

from WannabeC.lexer import WannabeCLexer
from WannabeC.parser import WannabeCParser


class WannabeCCompiler:
    def __init__(self, file=None):
        if file:
            self.parse_file(file)
        else:
            self.interpreter()
        exit(0)

    def _file_to_tokens(self, filename):
        with open(filename) as f:
            text = f.read()

            lexer = WannabeCLexer()
            return lexer.tokenize(text)

    def _print_tokens(self, tokens):
        print("\nTokens 🎟️")
        pprint(tokens)
        print()

    def tokenize_file(self, filename):
        tokens = self._file_to_tokens(filename)
        for tok in tokenrun_lexers:
            print("\t", tok)

    def parse_file(self, filename):
        tokens = self._file_to_tokens(filename)
        tokens = list(tokens)

        # self._print_tokens(tokens) # you can uncomment this to view the tokens being generated

        parser = WannabeCParser()
        result = parser.parse(iter(tokens))

        if hasattr(result, '__len__') and len(result) > 0:
            print("👇")
            [print(r) for r in result if r != None]

    def interpreter(self):
        lexer = WannabeCLexer()
        parser = WannabeCParser()

        while True:
            try:
                text = input('⊃(ᴗ ͜ʖ ᴗ)⊃━☆*✨ > ')
                if text:
                    result = parser.parse(lexer.tokenize(text))
                    if result != None:
                        [print("👉 ", r) for r in result if r]
            except KeyboardInterrupt:
                print("Bye 👋...")
                break
