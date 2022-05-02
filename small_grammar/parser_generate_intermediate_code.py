# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import json
from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = {
        'NAME', 'NUMBER',
        }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')' , ';'}

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, token):
        print("Illegal character '%s'" % token.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.names = { }  # where we store variables
        self.computer_generated_names = [ ]  # format of individual elements is : { CG_name : "T-1", expression = "(bla bla bla)"}


    @_('block')
    def program(self, p):
        json_represention = json.dumps(p.block)
        with open("parse_tree.json", "w") as target_file:
            json.dump(p.block, target_file, indent=4)

    @_('statement block')
    def block(self, p):
        return (p[0], p[1])

    @_('statement')
    def block(self, p):
        return p.statement

    @_('NAME "=" expr ";"')
    def statement(self, p):
        self.names[p.NAME] = p.expr
        # Intermediate code stuff
        # create new CG object
        CG_name = name_generator.generate_new_name() # create a computer_generated_name and make it an alias of p.NAME
        CG_obj = { "CG_name" : CG_name, "CG_expr" : {p.NAME : p.expr} }

        # append CG_obj to the computer_generated_names array
        self.computer_generated_names.append(CG_obj)

        # print ICs
        print("ASSIGN, ", CG_name, ", ", p.expr)
        return p.expr

    # SYNTAX ERROR HANDLING for missing assignment sign.
    @_('NAME error  expr ";" ')
    def expr(self, p):
        src_file = open("Test.c")
        text = src_file.read()
        column = find_column(text, p.error)
        print("Syntax error in line " ,p.error.lineno, " : expected '=' at position ", column , " but found ", p.error.value, " instead")


    @_('expr ";" ')
    def statement(self, p):
        return p.expr

    @_('expr "+" expr')
    def expr(self, p):
        # Intermediate code stuff
        # create new CG object
        CG_name = name_generator.generate_new_name() # create a computer_generated_name and make it an alias of p.NAME
        CG_obj = { "CG_name" : CG_name, "CG_expr" : ( p[0], p[1], p[2] )}

        # append CG_obj to the computer_generated_names array
        self.computer_generated_names.append(CG_obj)

        # print ICs
        first_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr0)
        second_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr1)
        print("ADD ", CG_name, " ,", first_operand_CG_name, " ,", second_operand_CG_name )

        return ( p[0], p[1], p[2] )

    # ERROR HANDLING for missing mathematical sign.
    @_('expr error  expr')
    def expr(self, p):
        src_file = open("Test.c")
        text = src_file.read()
        column = find_column(text, p.error)
        print("Syntax error in line " ,p.error.lineno, " : expected a mathematical sign at position ", column , " but found ", p.error.value, " instead")

    @_('expr "-" expr')
    def expr(self, p):
        # Intermediate code stuff
        # create new CG object
        CG_name = name_generator.generate_new_name() # create a computer_generated_name and make it an alias of p.NAME
        CG_obj = { "CG_name" : CG_name, "CG_expr" : ( p[0], p[1], p[2] )}

        # append CG_obj to the computer_generated_names array
        self.computer_generated_names.append(CG_obj)

        # print ICs
        first_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr0)
        second_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr1)
        print("NINUS ", CG_name, " ,", first_operand_CG_name, " ,", second_operand_CG_name )

        return (p[0], p[1], p[2])

    @_('expr "*" expr')
    def expr(self, p):
        # Intermediate code stuff
        # create new CG object
        CG_name = name_generator.generate_new_name() # create a computer_generated_name and make it an alias of p.NAME
        CG_obj = { "CG_name" : CG_name, "CG_expr" : ( p[0], p[1], p[2] )}

        # append CG_obj to the computer_generated_names array
        self.computer_generated_names.append(CG_obj)

        # print ICs
        first_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr0)
        second_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr1)
        print("TIMES ", CG_name, " ,", first_operand_CG_name, " ,", second_operand_CG_name )

        return (p[0], p[1], p[2])

    @_('expr "/" expr')
    def expr(self, p):
        # Intermediate code stuff
        # create new CG object
        CG_name = name_generator.generate_new_name() # create a computer_generated_name and make it an alias of p.NAME
        CG_obj = { "CG_name" : CG_name, "CG_expr" : ( p[0], p[1], p[2] ) }

        # append CG_obj to the computer_generated_names array
        self.computer_generated_names.append(CG_obj)

        # print ICs
        first_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr0)
        second_operand_CG_name = get_CG_name(self.computer_generated_names, p.expr1)
        print("DIVIDE ", CG_name, " ,", first_operand_CG_name, " ,", second_operand_CG_name )

        return (p[0], p[1], p[2])

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        #  SEMANTIC ANALYSIS --- type-checking
        if isinstance(p.NUMBER, int):
            pass
        return {"NUMBER" : p.NUMBER }

    @_('NAME')
    def expr(self, p):
        try:
            return { p.NAME : self.names[p.NAME] }
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

# ERROR HANDLING
    def error(self, token):
        if (token == None):
            print("Syntax Error : Compiler reached end of file. The code might be incomplete")
        else:
            src_file = open("Test.c", "r")
            text = src_file.read()
            column = find_column(text, token)
            print("Syntax Error : at line ", token.lineno, " column : ", column, " ---> offending token value : ", token.value)

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

# this function generates new Computer generated variable names
# the names are in the format : T-0, T-1, T-2 ... and so on
class Name_generator():
    # non-static attributes:
    def __init__(self):
        self.segment_one = "T-"  # segment one of the new Computer Generated name.
        self.current_index = 0    # This is the index of the current new name. It begins at zero by default

    def generate_new_name(self):
        new_name = self.segment_one + str(self.current_index)
        self.current_index = self.current_index + 1
        return new_name

name_generator = Name_generator()

def get_CG_name(computer_generated_names, expr):
    # loop through the CG objects..
    for CG_obj in computer_generated_names:
        # if it has similar "expr", return_its CG_name
        if CG_obj["CG_expr"] == expr:
            return CG_obj["CG_name"]

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    with open("Test.c") as src_file:
        text = src_file.read()
        parser.parse(lexer.tokenize(text))


    # while True:
    #     try:
    #         text = input('calc > ')
    #     except EOFError:
    #         break
    #     if text:
    #         parser.parse(lexer.tokenize(text))
