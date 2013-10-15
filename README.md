LC2K+ Macro Preprocessor
=========

LC2K+ is a C-like macro preprocessor for [LC2K](http://evanhahn.com/random/eecs-370-lc-2k-tricks/), 
the assembly language used for EECS370 at the University of Michigan. It adds basic C-like symbol 
and function style macro definition, line continuation, better labelling, and C and C++ style comments 
to the LC2K assembly language.

Writing assembly is hard. Writing LC2K is harder. LC2K+ makes it easier to write your LC2K assembly
programs by allowing you to rename register, reduce code duplication, and most importantly, organize 
your code with indentation, multiline comments, and empty lines.

LC2K+ is written by a C programmer with the C language in mind. All language constructs added to the 
LC2K+ language are equivalent to those in the C language. If you're familiar with C/C++, you will
instantly master LC2K+

## Usage
LC2K+ converts an LC2K+ source file into a valid LC2K assembly file. Use

    lc2k+.py <source file> <dest file>

where `<source file>` is the location of your LC2K+ code file, and `<dest file>` is the assembly file
to be generated. For example,

    lc2k+.py comb.hras comb.as
    
## Download and Install

Download `lc2k+.py` from https://raw.github.com/interarticle/lc2k-plus/master/lc2k+.py

### Linux
You need to have Python 2.7 installed. Since most linux distributions come installed with python,
just open a terminal and type `python --version` to ensure you have Python 2.7 set as the default
`python`. If not, consult your distributions manuals for the installation of Python 2.7 and setting
it as the default `python` program.

Make sure `lc2k+.py` is executable through 

    chmod +x l2ck+.py

You can either copy `lc2k+.py` to `/usr/local/bin`, or put it under your working directory. In the second
case, invoke LC2K+ using

    ./lc2k+.py <source file> <dest file>

### Windows
You must install Python 2.7 from http://www.python.org/download/. Please do not use Python 3.x.

After installation, you may simply open a Command Prompt (cmd.exe), then type

    lc2k+.py <source file> <dest file>
    
under the folder you put `lc2k+.py`.

## The Language
The language used by LC2K+ is mostly compatible with LC2K, except in label handling. Make sure you read the
next section on labels before you start, or you will find surprising results.

### Labels
In LC2K, labels are put as the first word on each line. Such a design makes it hard to write code without 
pounding on the space key. As such, the author has decided to drop compatibility with the LC2K label
syntax.

Labels in LC2K+ are denoted by a colon (:), the same as in C/C++, in the form

    label: instruction

As opposed to LC2K, you may start a line without any space/label, and it will be handled accordingly. 
For example,

    add 0 0 1
    label: add 0 0 1

Labels do not have to be on the same line as the instruction. Thus, the following is also legal:

    label:
    add 0 0 1

Finally, you may indent each line as you like:

    main:
        instruction
        instruction
        instruction
    func1:
        instruction
        instruction
        ...

### Alternative Register Naming
Bored of refering to registers using just numbers? Like the way you call registers `r?` in ARM? LC2K+ also supports
this way of refering to registers. You can call any register with a `r` prefix, for example,

     add r0 r0 r1

### Macros
Macros in LC2K+ are the same as macros in C/C++. Macros are defined using the `#define` preprocessor command. 
Macro names may contain a-z, A-Z, 0-9, and symbols `$` and `_`

#### Symbol-like Macros
Symbol-like macros are like constants. Any word in the LC2K+ source code that matches the name of the macro will
be replaced by the value defined for the macro. For example:

    #define NAME VALUE

After the definition, any mention of `NAME` will be replaced by `VALUE`.

For example, you may want to call `r0` `$zero`. You would do

    #define $zero r0

Then, you can do things like

    lw $zero r7 addr

which is the same as writing `lw r0 r7 addr`

#### Function-like Macros
Function-like macros are like C functions. Function-like macros may have parameters, which will replace the 
corresponding values in the macro value. For example, (based on http://evanhahn.com/random/eecs-370-lc-2k-tricks/)

    #define mov(src, dst) add r0 src dst

Then, you can copy the value from register 3 to register 2 using

    mov(r2, r3)

**WARNING**: LC2K+ macros do NOT define new LC2K instructions. You must add a pair of parenthesis when 
instantiating a function-like macro.

### Multiple Commands on the Same Line
To facilitate multiple commands in a macro, I added the feature to include multiple commands on the same
line. To do so, simply seperate the commands using semicolons (`;`). For example:

    add r1 r2 r3; add r2 r3 r4

will be processed to

    add r1 r2 r3
    add r2 r3 r4

With this feature, you can write the following macros:

    #define twonoops() noop; noop

**WARNING**: LC2K+ is still sensitive to line-breaks.

### Line Continuation

Just like in C, you may put multiple lines into a macro or instruction (hmm, can't think of why you'd need that)
with line continuation. To do line continuation, add a backslash (`\`) and the end of a line. For example,

    #define twonoops() noop; \
                       noop

This is equivalent to

    #define twonoops() noop; noop

### Comments
Last but not least, you can add C and C++ style comments to your LC2K+ code. For example:

    /*
     @file something.hras
     This is a block comment for the LC2K+ file!
    */
    //And here's an inline comment
    noop //This is a comment for noop

All comments are *removed* after processing. If you want to retain comment in the resulting LC2K file, please
do it the LC2K way, i.e. by adding text directly after the instruction.

## Disclaimer
In addition to the disclaimer in the [license](https://raw.github.com/interarticle/lc2k-plus/master/LICENSE), you 
should understand that

* This software is not required/necessary as part of any class projects in EECS370.
* The author does not guarantee the correctness of this software.
* The author should not be held responsible for any consequences caused by the use of this software, like
  losing points for an incorrectly generated LC2K assembly file, or failing to understand raw LC2K code
  in an exam due to excessive use of this software (unlikely).

Please, make sure you check the generated LC2K file before you submit it. Since this software was hacked out in a day,
I cannot guarantee that it's bug-free. 

Feel free to report any bugs you find using github. Or even better, fork the code and improve it yourself!

## Tips
* Under Linux, you may rename `lc2k+.py` to `lc2k+`, in order that you may invoke the program as `lc2k+`.

赵迤晨 (Zhao, Yichen)
interarticle@gmail.com
