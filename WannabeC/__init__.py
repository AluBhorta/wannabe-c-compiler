from pprint import pprint

from WannabeC.lexer import WannabeCLexer
from WannabeC.parser import WannabeCParser

class WannabeCCompiler:
    def _file_to_tokens(self, filename):
        with open(filename) as f:
            text = f.read()
            
            lexer = WannabeCLexer()
            return lexer.tokenize(text)

    def run_lexer(self, filename):
        tokens = self._file_to_tokens(filename)
        for tok in tokens:
            print("\t", tok)

    def run_parser(self):
        lexer = WannabeCLexer()
        parser = WannabeCParser()

        while True:
            try:
                text = input('wanna > ')
                result = parser.parse(lexer.tokenize(text))
                print(result)
            except EOFError:
                break

    def parse_file(self, filename):
        tokens = self._file_to_tokens(filename)
        tokens = list(tokens)

        print("\nTokens")
        pprint(tokens)
        print()

        parser = WannabeCParser()
        result = parser.parse(iter(tokens))
        print("\nParse result: ", result)


