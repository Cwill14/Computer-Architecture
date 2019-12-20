'''
Bitwise Operations
--------------------
0 = False
1 = True

A B  A and B
------------
0 0     0
1 0     0
0 1     0
1 1     1

A B   A or B
------------
0 0     0
1 0     1
0 1     1
1 1     1

in python, 'and' and 'or' are booleans

use & and | for bitwise
'''
'''
   1
&  1
----
   1

   1010101
&  1101011
----------
   1000001


     ^^
   1110101
&  0011000   Mask
----------
   0010000
     ^^

Mask is when you pull out the values you want
'''
'''
Shifting

  ^^
0010000
0001000
0000100
0000010
     ^^

>> right shift
<< left shift

  ^^
  10100010 MUL
& 11000000 Mask
----------
  10000000 >> 6
  00000010
        ^^

ir = 0b10100010 # Mul
length = ((ir & 0b11000000) >> 6) + 1
* adding 1 because of operation itself to advance pc

pc += length


'''