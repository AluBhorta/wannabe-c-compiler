import readline
from pprint import pprint

from WannabeC.lexer import WannabeCLexer
from WannabeC.parser import WannabeCParser


class WannabeCCompiler:
    def _file_to_tokens(self, filename):
        with open(filename) as f:
            text = f.read()

            lexer = WannabeCLexer()
            return lexer.tokenize(text)

    def tokenize_file(self, filename):
        tokens = self._file_to_tokens(filename)
        for tok in tokenrun_lexers:
            print("\t", tok)

    def parse_file(self, filename):
        tokens = self._file_to_tokens(filename)
        tokens = list(tokens)

        print("\nTokens")
        pprint(tokens)
        print()

        parser = WannabeCParser()
        result = parser.parse(iter(tokens))
        print("\nParse result: ", result)

    def interpreter(self):
        lexer = WannabeCLexer()
        parser = WannabeCParser()

        while True:
            try:
                text = input('⊃( ͡° ͜ʖ ͡°)⊃━☆*・ﾟ > ')
                if text:
                    result = parser.parse(lexer.tokenize(text))
                    print(result)
            except KeyboardInterrupt:
                print("Bye 👋...")
                break
