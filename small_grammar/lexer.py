# calclex.py

import json
from sly import Lexer

class CalcLexer(Lexer):
    # Set of reserved names (language keywords)
    reserved_words = { 'WHILE', 'IF', 'ELSE', 'PRINT' } 

    # Set of token names.   This is always required
    tokens = {
        'NUMBER',
        'ID',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ASSIGN',
        'EQ',
        'LT',
        'LE',
        'GT',
        'GE',
        'NE',
        *reserved_words,
        }

    literals = { '(', ')', '{', '}', ';' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        # Check if name matches a reserved word (change token type if true)
        if t.value.upper() in self.reserved_words:
            t.type = t.value.upper()
        return t

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, token):
        # print("\n Line " ,self.lineno ," : Bad character ",  token.value[0])
        self.index += 1

#  miscellaneous helper functions
# Find a token's column position.
#     input is the input text string
#     token is a token instance
def find_column(text, token):
    last_cr = text.rfind('\n', 0, token.index)
    if last_cr < 0:
        last_cr = 0
    column = (token.index - last_cr) + 1
    return column


# it is from here that the Lexer does its thing
src_file = open("Test.c")
out_file = open("Lexer_Output.txt","w")
lexer = CalcLexer()

# create an  many_lines_struct that will store the line_structs
many_lines_struct = []

for line_index, line in enumerate(src_file):
    # create a new line_struct that will store the tokens of a single line in a list.
    line_struct = []

    for token_position, token in enumerate(lexer.tokenize(line)):
        token_struct = [token.type, token.value]
        line_struct.append(token_struct)
        out_file.write('<%r> --> %r\t' %(token.type, token.value)) # this is going to the .txt file


        # we handle record the lexer Errors :
        if (token.type == "ERROR"):
            print("h hahahaha")
            text = src_file.read()
            token_column = find_column(text, token)
            print("Grammatical Error in line ", line_index, " , column ", token_column, " ---> Character : ", token.value[0])


    # make the file pointer in the .txt output skip to a new line
    out_file.write("\n")
    # append the newly filled line_struct to the many_lines_struct
    many_lines_struct.append(line_struct)

    # writing to the json file
    with open("token_stream.json", "w") as json_output:
        json.dump(many_lines_struct, json_output)

    # to view the json_output in a convenient format... umcomment the lines below
    # print(json.dumps(many_lines_struct, indent=2))
