from lexer_execute import CalcLexer
from sly import Parser, Lexer


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/', '%')
        )

    def __init__(self):
        self.names = { }  # where we store variables
                          # in the format : { variable_name : "num", variable_type : int, variable_value : 2}

    @_('function_definition')
    def program(self, p):
        with open("parse_tree.json", "w") as target_file:
            json.dump(p.function_definition, target_file, indent=4)

    @_('type_specifier identifier "(" function_parameters ")"  compound_statement')
    def function_definition(self, p):
        return get_an_array_of_all_tokens(p)

    @_('type_specifier identifier "("  ")"  compound_statement')
    def function_definition(self, p):
        return get_an_array_of_all_tokens(p)

    # <function_parameters> ::= <parameter_list>
    @_('parameter_list')
    def function_parameters(self, p):
        return p[0]

    # <parameter_list> ::= <parameter> comma_delimiter <parameter_list>
    #     	          | <parameter>
    @_('parameter "," parameter_list',
       'parameter')
    def parameter_list(self, p):
        return get_an_array_of_all_tokens(p)

    @_('parameter')
    def function_parameters(self, p):
        return p[0]

    # <parameter> ::= <type_specifier> <identifier>
    @_('type_specifier identifier')
    def parameter(self, p):
        return get_an_array_of_all_tokens(p)

    # <identifier> ::= constant_identifier
    @_('IDENTIFIER')
    def identifier(self, p):
        return p[0]

    # <type_specifier> ::=      key_word_void
    #   	                | key_word_bool
    #   	                | key_word_int
    #   	                | key_word_float
    @_('VOID_KEYWORD',
       'BOOL_KEYWORD',
       'INT_KEYWORD',
       'FLOAT_KEYWORD')
    def type_specifier(self, p):
        return p[0]

    # <compound_statement> ::= left_curly_bracket <stmt_list> right_curly_bracket
    @_('"{" stmt_list "}"')
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
        return p[0]

    # <if_else_variant_stmt>  ::= key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>
    #                      |  key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement> key_word_else <compound_statement>
    @_('IF_KEYWORD "(" boolean_expression ")" compound_statement',
       'IF_KEYWORD "(" boolean_expression ")" compound_statement ELSE_KEYWORD compound_statement')
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
        return {"non_if_else_variant_stmt" : p[0]}

    # <expression_statement> ::= <expression> semi_colon_delimiter
    #                	    | semi_colon_delimiter
    @_('expression ";"',
       '";"')
    def expression_statement(self, p):
        return {"expression_statement" : get_an_array_of_all_tokens(p)}

    # <iteration_statement> ::= key_word_while  left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>
    @_('WHILE_KEYWORD "(" boolean_expression ")" compound_statement')
    def iteration_statement(self, p):
        return {"expression_statement" : get_an_array_of_all_tokens(p)}

    # <jump_statement> ::= <return_stmt>
    #     	      |  <break_stmt>
    @_('return_stmt',
       'break_stmt')
    def jump_statement(self, p):
        return {"jump_statement" : p[0] }

    # <return_stmt> ::= key_word_return semi_colon_delimiter
    #             | key_word_return <expression> semi_colon_delimiter
    @_('RETURN_KEYWORD ";"',
       'RETURN_KEYWORD expression ";"')
    def return_stmt(self, p):
        return {"return_stmt" : get_an_array_of_all_tokens(p) }

    # <break_stmt>  ::= key_word_break semi_colon_delimiter
    @_('BREAK_KEYWORD ";"')
    def break_stmt(self, p):
        return {"break_stmt" : get_an_array_of_all_tokens(p)}

    # <variable_declaration> ::= <type_specifier> <identifier> semi_colon_delimiter
    #                     |  <type_specifier> <identifier> assignment_operator <expression> semi_colon_delimiter
    @_('type_specifier identifier ";"',
       'type_specifier identifier "=" expression ";"')
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
    @_('identifier "=" assignment_expression',
       'expression')
    def assignment_expression(self, p):
        return {"assignment_expression" : get_an_array_of_all_tokens(p)}

    # <arithmetic_expression>  ::= <arithmetic_expression> addition_operator <arithmetic_expression>
    #                       |  <arithmetic_expression> subtraction_operator <arithmetic_expression>
    #                       |  <arithmetic_expression> multiplication_operator <arithmetic_expression>
    #                       |  <arithmetic_expression> division_operator <arithmetic_expression>
    #                       |  left_rounded_bracket <arithmetic_expression> right_rounded_bracket
    #                       |  <number>
    @_('arithmetic_expression "+" arithmetic_expression',
       'arithmetic_expression "-" arithmetic_expression',
       'arithmetic_expression "*" arithmetic_expression',
       'arithmetic_expression "/" arithmetic_expression',
       'arithmetic_expression "%" arithmetic_expression',
       '"(" arithmetic_expression ")"',
       'number')
    def arithmetic_expression(self, p):
        return {"arithmetic_expression" : get_an_array_of_all_tokens(p)}

    # <number>  ::= constant_int
    #            |  constant_float
    @_('INT_CONSTANT',
       'FLOAT_CONSTANT')
    def number(self, p):
        return {"number" : p[0]}

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
        return {"comparison_sign" : p[0]}

    # <boolean_expression>  ::=    <relational_boolean_expression>
    #                       |  left_rounded_bracket <boolean_expression>  right_rounded_bracket
    #                       |  logical_NOT_sign left_rounded_bracket <boolean_expression>  right_rounded_bracket
    #                       |  <boolean_expression> logical_AND_sign <boolean_expression>
    #                       |  <boolean_expression> logical_OR_sign <boolean_expression>
    #                       |  constant_bool
    @_('relational_boolean_expression',
       '"(" boolean_expression ")"',
       'LOGICAL_NOT "(" boolean_expression ")"',
       'boolean_expression LOGICAL_AND boolean_expression',
       'boolean_expression LOGICAL_OR boolean_expression',
       'BOOL_CONSTANT')
    def boolean_expression(self, p):
        return {"boolean_expression" : get_an_array_of_all_tokens(p) }








    # @_('statement')
    # def block(self, p):
    #     return p.statement
    #
    # @_('NAME "=" expr ";"')
    # def statement(self, p):
    #     self.names[p.NAME] = p.expr
    #     return (p[0], p[1], p[2], p[3])
    #
    # # SYNTAX ERROR HANDLING for missing assignment sign.
    # @_('NAME error  expr ";" ')
    # def expr(self, p):
    #     src_file = open("Test.c")
    #     text = src_file.read()
    #     column = find_column(text, p.error)
    #     print("Syntax error in line " ,p.error.lineno, " : expected '=' at position ", column , " but found ", p.error.value, " instead")
    #
    #
    # @_('expr ";" ')
    # def statement(self, p):
    #     return (p.expr, p[1])
    #
    # @_('expr "+" expr')
    # def expr(self, p):
    #     return ( p[0], p[1], p[2] )
    #
    # # ERROR HANDLING for missing mathematical sign.
    # @_('expr error  expr')
    # def expr(self, p):
    #     src_file = open("Test.c")
    #     text = src_file.read()
    #     column = find_column(text, p.error)
    #     print("Syntax error in line " ,p.error.lineno, " : expected a mathematical sign at position ", column , " but found ", p.error.value, " instead")
    #
    # @_('expr "-" expr')
    # def expr(self, p):
    #     return (p[0], p[1], p[2])
    #
    # @_('expr "*" expr')
    # def expr(self, p):
    #     return (p[0], p[1], p[2])
    #
    # @_('expr "/" expr')
    # def expr(self, p):
    #     return (p[0], p[1], p[2])
    #
    # @_('"-" expr %prec UMINUS')
    # def expr(self, p):
    #     return (p[0], p[1], p[2])
    #
    # @_('"(" expr ")"')
    # def expr(self, p):
    #     return (p[0], p[1], p[2])
    #
    # @_('NUMBER')
    # def expr(self, p):
    #     #  SEMANTIC ANALYSIS --- type-checking
    #     if isinstance(p.NUMBER, int):
    #         pass
    #     return {"NUMBER" : p.NUMBER }
    #
    # @_('NAME')
    # def expr(self, p):
    #     try:
    #         return { p.NAME : self.names[p.NAME] }
    #     except LookupError:
    #         print("Undefined name '%s'" % p.NAME)
    #         return 0

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

def get_an_array_of_all_tokens(p):
    array = ()
    for token in p:
        array.append(token)
    return array

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    with open("Test.c") as src_file:
        text = src_file.read()
        parser.parse(lexer.tokenize(text))
