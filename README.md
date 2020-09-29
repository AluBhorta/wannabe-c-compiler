# Wannabe C Compiler

A compiler that understands C-language like expressions and functions, written in python - because, why not? 🤷

## About SLY

`Wannabe C` uses [SLY](https://sly.readthedocs.io/en/latest/sly.html), a python Lex-Yacc library which is a successor to PLY. Both of them were created by [David Beazley](https://github.com/dabeaz/).

The regular expressions for the tokens used are defined in a class at `WannabeC/lexer.py`

The parser (grammar, precedence & actions) are defined in a class at `WannabeC/parser.py`

- In the Parser class in, each method corresponds to a set of productions for a particular LHS.
- the name of the methods define the LHS
- the list of strings in the `@_()` decorators refer to the RHS/productions
- the method body defines the corresponding action for the LHS

The `parser-debug.log` file is being used for debugging the parser, which will contain the entire grammar along with all parsing states, and conflicts (if any).

## Language features

NOTE: don't forget to use `;` at the end of each line/statement.
#### Printing

use `print` for printing into stdout.

```c
print 0;
```

or

```c
print(1);
```

#### Types

- [x] `int`
- [x] `void`


#### Arithmetic and Boolean

Arithmetic Operators

- [x] `%`
- [x] `*`
- [x] `+`
- [x] `-`
- [x] `/`

Try:
```c
print 2*3+4;    // 10

print 2*(3+4);  // 14
```

Boolean Operators

- [x] `&&`
- [x] `||`
- [x] `==`
- [x] `<=`
- [x] `>=`
- [x] `!=`
- [x] `<`
- [x] `>`

#### Assignments

Use the `=` operator to assin values to variables. Type safety and error checking is handled.

```c
int age = 9;

age = 3*10-1;
```

#### Conditionals

Use the familiar `if-else` c-sytax for conditionals.

```c
if (420%2==0) if (0>666/2) print 6 else print 9;
```

It supports unlimited levels of `if-else` nesting using the match-unmatch grammar. The dangling-else is resolved by pairing with the nearest/closest `if`, like in bison.


#### Functions

Use the familiar ```TYPE NAME ( ) { body }``` function definition as in c. 

For example:

```c
int foo()
{
  int a = 1;
  int b = 2;
  int tmp = a;
  
  a = b; b = tmp;
  
  return a;
}
// output: 2
```

Use `return` with `int` type functions. Type safety and error checking is handled.

#### Comments

Use `//` for comments.

## Usage

### Depencencies

Make sure you have:

- python 3.6 (or above)
- pip

Check whether you have the correct version of python installed with:

```bash
python --version
```

### Installation

Install virtualenv:

```bash
pip install virtualenv
```

Initialize and activate a new python environment with virtualenv:

```bash
# For Linux/Unix
virtualenv .venv
source .venv/bin/activate

# For Windows
python -m virtualenv .venv
.venv\Scripts\activate
```

Install required modules using pip:

```bash
pip install -r requirements.txt
```

### Execution

There are 2 main ways to use WannabeC

##### 1. As an interactive interpreter in cli

To use as an interpreter, run

```sh
python main.py
```

And the magical interpreter genie shall appear...

```sh
⊃(ᴗ ͜ʖ ᴗ)⊃━☆*✨ >
```

Now you can execute expressions that are allowed by its grammar.

For example:

```c
2*3+4;

print 2*3+4;
```

Or even:

```sh
if(1==1) if(2==2) if(3==3) print 4 else print 5;
```


NOTE: Press `CTRL+c` to exit.

##### 2. For displaying results of a parsed input file

For parsing files and displaying the results, use this signature:

```sh
python main.py --file <file>
```

There are a few test files in the `data/` dir (affectionately named with the `.wanna` extension). To run the 7th test, execute:

```sh
python main.py --file data/example7.wanna
```
It should return `0`.

For help or synopsis:

```bash
python main.py --help
```
