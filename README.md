
# Wannabe C Compiler

A compiler that parses limited c-language like functions.

Written in python using the [SLY](https://sly.readthedocs.io/en/latest/sly.html) library.

## Usage

Requires Python >= 3.6


## Notes

#### operators to handle
```
arithmetic  : '+' '-' '*' '/' '%'
if-else     : 'if' 'else'
empty blocks: '{ }'
assignment  : '=' '+=' '-=' '*=' '/=' '%='
logical     : '==' '&&' '||' '!=' '=<' '>=' '<' '>' 
unary       : '++' '--'
brackets    : '(' ')' '{' '}'
return      : 'return'
```

#### if-else

```
E           : matched
            | unmatched

matched     : if matched else matched
            | a
            | b
            | c

unmatched   : if E
            | if matched else unmatched
```

```
expression
    : arithmetic_expression     [+ - * / %]
    | assignment_expression     ['int a = 2' 'a = b+c' 'a += 2+b/3']
    | unary_expression          ['a++' '++a' 'a' 'b']
    | boolean_expression        ['_ boolean_operator _' ]
    | conditional_expression    []
    | return_expression         []
```


```
boolean_expression
    a == b
    a > b

    a > b+3*c
    a+3*b  < 23

    a > b++     a++ > ++b

    a++
    a % 2 == 0
```