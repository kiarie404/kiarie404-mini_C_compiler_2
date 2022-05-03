


from sly import Lexer
import json

class CalcLexer(Lexer):
    tokens = { IDENTIFIER, RETURN_KEYWORD, VOID_KEYWORD, BOOL_KEYWORD, FLOAT_KEYWORD, INT_KEYWORD,
               IF_KEYWORD, ELSE_KEYWORD, WHILE_KEYWORD, BREAK_KEYWORD,
               FLOAT_CONSTANT, INT_CONSTANT, BOOL_CONSTANT,
               ADD, MINUS, TIMES, MODULUS, DIVIDE, ASSIGN,
               EQUIVALENT_TO, LESS_OR_EQUAL, LESS_THAN, GREATER_OR_EQUAL, GREATER_THAN, INEQUIVALENT_TO,
               LOGICAL_NOT, LOGICAL_OR, LOGICAL_AND,
               LPAREN, RPAREN, LCURLY, RCURLY, SCOLON, COMMA}

    # String containing ignored characters between tokens
    ignore = '\t'
    ignore_whitespace = '\s+'
    ignore_comment = r'\/\/.*'  # meant to ignore comments

    # literals
    # we have chosen to use literals for the sake of readability



    # Regular expression rules for tokens
    FLOAT_CONSTANT = r'\d*\.{1}\d+'
    INT_CONSTANT  = r'\d+'
    BOOL_CONSTANT = r'(true|TRUE|false|FALSE)'
    ADD    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    MODULUS = r'%'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    EQUIVALENT_TO = r'=='
    LESS_OR_EQUAL = r'<='
    LESS_THAN = r'<'
    GREATER_OR_EQUAL = r'>='
    GREATER_THAN = r'>'
    INEQUIVALENT_TO = r'!='
    LOGICAL_NOT = r'!'
    LOGICAL_OR = r'\|\|'
    LOGICAL_AND = r'&&'


    # Tokens for keywords
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['return'] = RETURN_KEYWORD
    IDENTIFIER['void'] = VOID_KEYWORD
    IDENTIFIER['bool'] = BOOL_KEYWORD
    IDENTIFIER['float'] = FLOAT_KEYWORD
    IDENTIFIER['int'] = INT_KEYWORD
    IDENTIFIER['if'] = IF_KEYWORD
    IDENTIFIER['else'] = ELSE_KEYWORD
    IDENTIFIER['while'] = WHILE_KEYWORD
    IDENTIFIER['break'] = BREAK_KEYWORD

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.index += 1
        return t

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

# if __name__ == '__main__':
src_file = open("Test.c")
out_file = open("Lexer_Output_token_stream.txt","w")

# create the error output file.
with open("Lexer_Output_error_logs.txt","w") as error_out_file:
    error_out_file.write("") # If it already exists, clear it. We dont need past errors

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
            text = ""
            with open("Test.c") as src:
                text = src.read()
            token_column = find_column(text, token)
            # write the error to the the error output file.
            with open("Lexer_Output_error_logs.txt","a") as error_out_file:
                # we write line_index+1 because the array un-intuitively began at 0 instead of 1-- humans count lines from 1...not zero
                error_msg = "Grammatical Error in line {} , column {} ---> Character :  {} \n".format(line_index+1, token_column, token.value[0])
                error_out_file.write(error_msg)


    # make the file pointer in the .txt output skip to a new line
    out_file.write("\n")
    # append the newly filled line_struct to the many_lines_struct
    many_lines_struct.append(line_struct)

    # writing to the json file
    with open("token_stream.json", "w") as json_output:
        json.dump(many_lines_struct, json_output)

    # to view the json_output in a convenient format... umcomment the lines below
    # print(json.dumps(many_lines_struct, indent=2))
