// #include<stdio.h>
// #include<stdbool.h>
// showing how functions are declared
// showing a function with mutiple parameters
int main(){
 // showing declarations
 int an_int = 34;
 int num ;     // integers without immediate initialization are assigned the value 0 by default
 num = 10;
 float a_float = 34.78; // floats without immediate initialization are assigned the value 0 by default
 float f ;
 f = 2.5;
 bool a_bool = true;


 // showing arithmetic capability
 float some_value = an_int * a_float + (32 % 8) / 10.9;
 float another_value = some_value = 10;

 // boolean operations
 // relational boolean operations
 bool comparison = 2 < 4 ; // returns true
 bool comparison2 = 2 || an_int ; // false

 bool comparison3 = comparison ||   comparison2;
 bool comparison4 = (comparison && comparison2) $ || !(2 == 3);

 // demonstrating loops
 int count = 2;
 // int num = 12;   // semantic error - "redeclaration of a variable within the same scope"
 num = 12;
 while(count <= num){
   // simple if stmt.
   if (count == num){ break; } // demonstrating break stmt
  // If-else statement
  if((num % count) == 0) { // Arithmetic operation and comparison
  return false; //Use of boolean
  }
  else {
  count++; // Arithmetic operation
  }
 }
} // emd of main()
