
import argparse
import os

from WannabeC.lexer import WannabeCLexer


def get_filepath():
    my_parser = argparse.ArgumentParser(
        description='Compile a given file'
    )
    my_parser.add_argument(
        'Path',
        metavar='path',
        type=str,
        help='the path to the file')

    args = my_parser.parse_args()
    input_path = args.Path

    return os.path.join(os.getcwd(), input_path)

def run_lexer(text):
    lexer = WannabeCLexer()
    print("\nThe tokens:")
    for tok in lexer.tokenize(text):
        print("\t", tok)

if __name__ == "__main__":
    filepath = get_filepath()

    with open(filepath) as f:
        text = f.read()
        run_lexer(text)
