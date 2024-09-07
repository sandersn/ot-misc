"""A collection of all the utilities I have created, plus some by Kaleb Captain and Jeremy McNeal

Note on docstrings. I use a notation to describe passing/returning types which is similar to Haskell's
notation. Here is how it works:
type*type -> returntype
int, str, float are the basic scalar types.
[], (), {} are the basic compound types.
fn, file, Any and None are some other ones.
type... indicates that an arbitrary number of type can be passed in that position.
Classes are represented by their class names, e.g. Symbol and Node.
Compound types (while actually heterogenous) are indicated as to what type they should contain,
if there is any homogeneaity to speak of, e.g. [Symbol].
This system can be nested arbitrarily deeply. Here are some examples:
    This example does not care what is in the list, although presumably fn might
        fn*[] -> []
    This function might obtain a string list from a transform specified by fn over the int list.
        fn*[int] -> [str]
    This function takes a list of int 2-tuples and returns an int list
        [(int*int)...] -> [int]
    This function has a variable arglist, but expects them all to be ints:
        int... -> int
If a function is passed, I try to specify its signature lower in the docstring if it's not obvious.
    fn :: int -> int

Also, destructively altered parameters (also known as -out- or -inout- params)
are marked with ! (after Scheme). Obviously, these are minimised but do show up occasionally.
Example:
    str*{str:(int,int)}! -> str
Will modify the dict passed in some way. The rest of the docstring should explain how.

        LICENCE (modified BSD licence)
Redistribution and use in source and binary forms,
    with or without modification, are permitted provided that the following condition is met:

    1. Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.
    3. The name of the author may not be used to endorse or promote products
        derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS''
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
__all__=["fs","web","fnc", "data_struct", 'text', 'reflect', 'dct', 'lst']
