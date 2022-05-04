# -----------------------------------------------------------------------------
# calc.py
# ------------------ -----------------------------------------------------------

import json
from sly import Lexer, Parser

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
    ignore_whitespace = '[ \t]+'
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
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LCURLY = r'\{'
    RCURLY = r'\}'
    SCOLON = ';'
    COMMA = ','


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
    # @_(r'\n+')
    # def newline(self, t):
    #     self.lineno += t.value.count('\n')

    # Define a rule so we can track line numbers
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\d+')
    def INT_CONSTANT(self, t):
        t.value = int(t.value)
        return t

    @_(r'\d*\.{1}\d+')
    def FLOAT_CONSTANT(self, t):
        t.value = int(t.value)
        return t

    def error(self, value):
        print('Line %d: Bad character %r' % (self.lineno, value))
        self.index += 1



class CalcParser(Parser):
    tokens = CalcLexer.tokens


    precedence = (
        ('left', 'ADD', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULUS')
        )

    def __init__(self):
        self.names = { }  # where we store variables
                          # in the format : { variable_name : "num", variable_type : int, variable_value : 2}

    @_('function_definition')
    def program(self, p):
        print("Found program")
        with open("parse_tree.json", "w") as target_file:
            json.dump(p.function_definition, target_file, indent=4)

    @_('type_specifier identifier LPAREN function_parameters RPAREN  compound_statement')
    def function_definition(self, p):
        return get_an_array_of_all_tokens(p)

    @_('type_specifier identifier LPAREN  RPAREN  compound_statement')
    def function_definition(self, p):
        return get_an_array_of_all_tokens(p)

    # <function_parameters> ::= <parameter_list>
    @_('parameter_list')
    def function_parameters(self, p):
        return get_an_array_of_all_tokens(p)

    # <parameter_list> ::= <parameter> comma_delimiter <parameter_list>
    #     	          | <parameter>
    @_('parameter COMMA parameter_list',
       'parameter')
    def parameter_list(self, p):
        return get_an_array_of_all_tokens(p)

    @_('parameter')
    def function_parameters(self, p):
        return get_an_array_of_all_tokens(p)

    # <parameter> ::= <type_specifier> <identifier>
    @_('type_specifier identifier')
    def parameter(self, p):
        return get_an_array_of_all_tokens(p)

    # <identifier> ::= constant_identifier
    @_('IDENTIFIER')
    def identifier(self, p):
        return get_an_array_of_all_tokens(p)

    # <type_specifier> ::=      key_word_void
    #   	                | key_word_bool
    #   	                | key_word_int
    #   	                | key_word_float
    @_('VOID_KEYWORD',
       'BOOL_KEYWORD',
       'INT_KEYWORD',
       'FLOAT_KEYWORD')
    def type_specifier(self, p):
        return get_an_array_of_all_tokens(p)

    # <compound_statement> ::= left_curly_bracket <stmt_list> right_curly_bracket
    @_('LCURLY stmt_list RCURLY')
    def compound_statement(self, p):
        return get_an_array_of_all_tokens(p)


    # <stmt_list> ::= <stmt> <stmt_list>
    #               | <stmt>
    @_('stmt stmt_list',
       'stmt')
    def stmt_list(self, p):
        return get_an_array_of_all_tokens(p)

    # <stmt>   ::= <if_else_variant_stmt>
    #       |  <non_if_else_variant_stmt>
    @_('if_else_variant_stmt',
       'non_if_else_variant_stmt')
    def stmt(self, p):
        return get_an_array_of_all_tokens(p)

    # <if_else_variant_stmt>  ::= key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>
    #                      |  key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement> key_word_else <compound_statement>
    @_('IF_KEYWORD LPAREN boolean_expression RPAREN compound_statement',
       'IF_KEYWORD LPAREN boolean_expression RPAREN compound_statement ELSE_KEYWORD compound_statement')
    def if_else_variant_stmt(self, p):
        return get_an_array_of_all_tokens(p)

    # <non_if_else_variant_stmt> ::= <expression_statement>
  	#             | <compound_statement>   ?????
    #             | <iteration_statement>
  	#             | <jump_statement>
    #             | <variable_declaration>
    @_('expression_statement',
       'compound_statement',
       'iteration_statement',
       'jump_statement',
       'variable_declaration')
    def non_if_else_variant_stmt(self, p):
        return {"non_if_else_variant_stmt" : get_an_array_of_all_tokens(p)}

    # <expression_statement> ::= <expression> semi_colon_delimiter
    #                	    | semi_colon_delimiter
    @_('expression SCOLON',
       'SCOLON')
    def expression_statement(self, p):
        return {"expression_statement" : get_an_array_of_all_tokens(p)}

    # <iteration_statement> ::= key_word_while  left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>
    @_('WHILE_KEYWORD LPAREN boolean_expression RPAREN compound_statement')
    def iteration_statement(self, p):
        return {"expression_statement" : get_an_array_of_all_tokens(p)}

    # <jump_statement> ::= <return_stmt>
    #     	      |  <break_stmt>
    @_('return_stmt',
       'break_stmt')
    def jump_statement(self, p):
        return {"jump_statement" : get_an_array_of_all_tokens(p) }

    # <return_stmt> ::= key_word_return semi_colon_delimiter
    #             | key_word_return <expression> semi_colon_delimiter
    @_('RETURN_KEYWORD SCOLON',
       'RETURN_KEYWORD expression SCOLON')
    def return_stmt(self, p):
        return {"return_stmt" : get_an_array_of_all_tokens(p) }

    # <break_stmt>  ::= key_word_break semi_colon_delimiter
    @_('BREAK_KEYWORD SCOLON')
    def break_stmt(self, p):
        return {"break_stmt" : get_an_array_of_all_tokens(p)}

    # <variable_declaration> ::= <type_specifier> <identifier> semi_colon_delimiter
    #                     |  <type_specifier> <identifier> assignment_operator <expression> semi_colon_delimiter
    @_('type_specifier identifier SCOLON',
       'type_specifier identifier ASSIGN expression SCOLON')
    def variable_declaration(self, p):
        return {"variable_declaration" : get_an_array_of_all_tokens(p)}

    # <expression> ::= <arithmetic_expression>  # includes both floats and int operations . A number is a number! ... whether a float or int.
    #           |  <boolean_expression>     # logical operations
    #           |  <assignment_expression>
    @_('arithmetic_expression',
       'boolean_expression',
       'assignment_expression')
    def expression(self, p):
        return {"expression" : get_an_array_of_all_tokens(p)}

    # <assignment_expression> ::= <identifier> assignment_operator <assignment_expression>  # to suppors an expression like x = y = z = 2+3(2*4)
    #                      |   <expression>    # smth like 2+3(2*4)
    @_('identifier ASSIGN assignment_expression',
       'expression')
    def assignment_expression(self, p):
        return {"assignment_expression" : get_an_array_of_all_tokens(p)}

    # <arithmetic_expression>  ::= <arithmetic_expression> addition_operator <arithmetic_expression>
    #                       |  <arithmetic_expression> subtraction_operator <arithmetic_expression>
    #                       |  <arithmetic_expression> multiplication_operator <arithmetic_expression>
    #                       |  <arithmetic_expression> division_operator <arithmetic_expression>
    #                       |  left_rounded_bracket <arithmetic_expression> right_rounded_bracket
    #                       |  <number>
    @_('arithmetic_expression ADD arithmetic_expression',
       'arithmetic_expression MINUS arithmetic_expression',
       'arithmetic_expression TIMES arithmetic_expression',
       'arithmetic_expression DIVIDE arithmetic_expression',
       'arithmetic_expression MODULUS arithmetic_expression',
       'LPAREN arithmetic_expression RPAREN',
       'number')
    def arithmetic_expression(self, p):
        return {"arithmetic_expression" : get_an_array_of_all_tokens(p)}

    # <number>  ::= constant_int
    #            |  constant_float
    @_('INT_CONSTANT',
       'FLOAT_CONSTANT')
    def number(self, p):
        return {"number" : get_an_array_of_all_tokens(p)}

    # <relational_boolean_expression>  ::= <arithmetic_expression> <comparison_sign> <arithmetic_expression>
    @_('arithmetic_expression comparison_sign arithmetic_expression')
    def relational_boolean_expression(self, p):
        return {"relational_boolean_expression" : get_an_array_of_all_tokens(p)}

    # <comparison_sign>       ::= less_than_sign
    #                      |  greater_than_sign
    #                      |  equivalent_to_sign
    #                      |  inequivalent_to_sign
    #                      |  greater_than_or_equal_to_sign
    #                      |  less_than_or_equal_to_sign
    @_('LESS_THAN',
       'GREATER_THAN',
       'EQUIVALENT_TO',
       'INEQUIVALENT_TO',
       'GREATER_OR_EQUAL',
       'LESS_OR_EQUAL')
    def comparison_sign(self, p):
        return {"comparison_sign" : get_an_array_of_all_tokens(p)}

    # <boolean_expression>  ::=    <relational_boolean_expression>
    #                       |  left_rounded_bracket <boolean_expression>  right_rounded_bracket
    #                       |  logical_NOT_sign left_rounded_bracket <boolean_expression>  right_rounded_bracket
    #                       |  <boolean_expression> logical_AND_sign <boolean_expression>
    #                       |  <boolean_expression> logical_OR_sign <boolean_expression>
    #                       |  constant_bool
    @_('relational_boolean_expression',
       'LPAREN boolean_expression RPAREN',
       'LOGICAL_NOT LPAREN boolean_expression RPAREN',
       'boolean_expression LOGICAL_AND boolean_expression',
       'boolean_expression LOGICAL_OR boolean_expression',
       'BOOL_CONSTANT')
    def boolean_expression(self, p):
        return {"boolean_expression" : get_an_array_of_all_tokens(p) }



    # ERROR HANDLING
    def error(self, p):
        if (p == None):
            print("Syntax Error : Compiler reached end of file. The code might be incomplete")
        else:
            with open("Test.c", "r") as src_file:
                text = src_file.read()
                column = find_column(text, p)
                print("Syntax Error : at line ", p.lineno, " column : ", column, " ---> offending token value : ", p.value[0])


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

def get_an_array_of_all_tokens(p):
    array = []
    for token in p:
        array.append(token)
    return array

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    with open("Test.c") as src_file:
        text = src_file.read()
        parser.parse(lexer.tokenize(text))
