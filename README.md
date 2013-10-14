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

You can either copy `lc2k+.py` to `/usr/local/bin`, or put it under your working directory. In the second
case, invoke LC2K+ using

    ./lc2k+.py <source file> <dest file>

### Windows
You must install Python 2.7 from http://www.python.org/download/. Please do not use Python 3.x.

After installation, you may simply open a Command Prompt (cmd.exe), then type

    lc2k+.py <source file> <dest file>
    
under the folder you put `lc2k+.py`.
