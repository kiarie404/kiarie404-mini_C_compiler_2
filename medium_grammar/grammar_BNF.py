<program> ::= <function_definition> # we will fix this later, let us work with main() function only for now

<function_definition> ::= <type_specifier> <identifier> left_rounded_bracket <function_parameters> right_rounded_bracket <compound_statement>
                        | <type_specifier> <identifier> left_rounded_bracket  right_rounded_bracket <compound_statement>   # made function accept NULL as a parameter safely


<function_parameters> ::= <parameter_list>

<parameter_list> ::= <parameter> comma_delimiter <parameter_list>
        	| <parameter>

<parameter> ::= <type_specifier> <identifier>

<identifier> ::= constant_identifier

<type_specifier> ::=      key_word_void
      	                | key_word_bool
      	                | key_word_int
      	                | key_word_float

<compound_statement> ::= left_curly_bracket <stmt_list> right_curly_bracket

<stmt_list> ::= <stmt> <stmt_list>
             | <stmt>

<stmt>   ::= <if_else_variant_stmt>
          |  <non_if_else_variant_stmt>

<if_else_variant_stmt>  ::= key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>
                         |  key_word_if left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement> key_word_else <compound_statement>

<non_if_else_variant_stmt> ::= <expression_statement>
  	            | <compound_statement>   ?????
                | <iteration_statement>
  	            | <jump_statement>
                | <variable_declaration>

<expression_statement> ::= <expression> semi_colon_delimiter
                   	    | semi_colon_delimiter

<iteration_statement> ::= key_word_while  left_rounded_bracket <boolean_expression> right_rounded_bracket <compound_statement>


<jump_statement> ::= <return_stmt>
        	      |  <break_stmt>

<return_stmt> ::= key_word_return semi_colon_delimiter
                | key_word_return <expression> semi_colon_delimiter

<break_stmt>  ::= key_word_break semi_colon_delimiter

<variable_declaration> ::= <type_specifier> <identifier> semi_colon_delimiter
                        |  <type_specifier> <identifier> assignment_operator <expression> semi_colon_delimiter


<expression> ::= <arithmetic_expression>  # includes both floats and int operations . A number is a number! ... whether a float or int.
              |  <boolean_expression>     # logical operations
              |  <assignment_expression>

<assignment_expression> ::= <identifier> assignment_operator <assignment_expression>  # to suppors an expression like x = y = z = 2+3(2*4)
                         |   <expression>    # smth like 2+3(2*4)


<arithmetic_expression>  ::= <arithmetic_expression> addition_operator <arithmetic_expression>
                          |  <arithmetic_expression> subtraction_operator <arithmetic_expression>
                          |  <arithmetic_expression> multiplication_operator <arithmetic_expression>
                          |  <arithmetic_expression> division_operator <arithmetic_expression>
                          |  left_rounded_bracket <arithmetic_expression> right_rounded_bracket
                          |  <number>

<number>  ::= constant_int
           |  constant_float

<relational_boolean_expression>  ::= <arithmetic_expression> <comparison_sign> <arithmetic_expression>

<comparison_sign>       ::= less_than_sign
                         |  greater_than_sign
                         |  equivalent_to_sign
                         |  inequivalent_to_sign
                         |  greater_than_or_equal_to_sign
                         |  less_than_or_equal_to_sign

<boolean_expression>  ::=    <relational_boolean_expression>
                          |  left_rounded_bracket <boolean_expression>  right_rounded_bracket
                          |  logical_NOT_sign left_rounded_bracket <boolean_expression>  right_rounded_bracket
                          |  <boolean_expression> logical_AND_sign <boolean_expression>
                          |  <boolean_expression> logical_OR_sign <boolean_expression>
                          |  constant_bool

------------------------- part 2 : Terminals used and their regex -------------------------------
#tokens for keywords
  key_word_int = "^int$"
  key_word_float = "^float$"
  key_word_bool = "^bool$"
  key_word_void = "^void$"
  key_word_return = "^return$"
  key_word_while = "^while$"
  key_word_if = "^if$"
  key_word_else = "^else$"
  key_word_break = "^break$"


#tokens for constants
  constant_int = "^[\+\-]{0,1}\d+$"             # integers can be signed or unsigned
  constant_float = "^[\+\-]{0,1}\d+\.{1}\d+$"   # floats can be signed or unsigned
  constant_bool = "^(true|false|TRUE|FALSE)$"
  constant_identifier ="^[a-zA-Z_][a-zA-Z0-9_]*"


#tokens for logical signs
  equivalent_to_sign = "^==$"
  inequivalent_to_sign = "^!=$"
  less_than_sign = "^<$"
  greater_than_sign = "^>$"
  greater_than_or_equal_to_sign = "^>=$"
  less_than_or_equal_to_sign = "^<=$"
  logical_NOT_sign = "^!$"
  logical_OR_sign = "^\|\|$"
  logical_AND_sign = "^&&$"

#tokens for delimiters
  semi_colon_delimiter = "^;$"
  comma_delimiter      = "^,$"
  right_rounded_bracket = "^\)$"
  left_rounded_bracket = "^\($"
  left_curly_bracket = "^\{$"
  right_curly_bracket = "^\}$"

#tokens for mathematical operators
  addition_operator = "^\+$"
  subtraction_operator = "^-$"
  division_operator = "^\/$"
  multiplication_operator = "\*$"
  modulus_operator = "^%$"
  assignment_operator= "^=$"

------------------------- end of part 2 : Terminals used and their regex  ------------------------
