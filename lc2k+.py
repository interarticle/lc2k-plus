#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LC2K+
LC2K Macro Preprocessor

Compiles LC2K-derived language with support for C-like macros, multiline 
comments and instruction aggregation.

See https://github.com/interarticle/lc2k-plus for documentation

Copyright (C) 2013 赵迤晨 (Zhao, Yichen)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__    = "赵迤晨 (Zhao, Yichen) <interarticle@gmail.com>"
__copyright__ = "Copyright (C) 2013 赵迤晨 (Zhao, Yichen)"
__license__   = "MIT"
__version__   = "0.1"
__status__    = "Prototype"
__email__     = "interarticle@gmail.com"

import argparse
import re
import sys

MACRO_VAL =0
MACRO_FUNC=1

argSplitter = re.compile(r'\s+')

def string_replace(string, replacement, start, end):
	return string[0:start] + replacement + string[end:], start + len(replacement)

def chain(gen_input, *gen_funcs):
	"""
	Chain generator functions by calling each generator with the input of the previous one.
	The first generator is passed the gen_input value
	"""
	for func in gen_funcs:
		gen_input = func(gen_input)
	return gen_input

def main():
	parser = argparse.ArgumentParser(description="LC2K Macro Preprocessor")
	parser.add_argument("sourceFile", nargs=1)
	parser.add_argument("destFile",nargs=1)
	args = parser.parse_args()

	def cleanLines(lines):
		"""
		Trim and remove empty lines
		"""
		for ln in lines:
			ln = ln.strip()
			if ln:
				yield ln

	def processEOL(lines):
		"""
		Sanitize before
		Process end-of-line backslashes
		"""
		linebuf = ""
		for ln in lines:
			if ln[len(ln) - 1] == '\\':
				ln = ln[0:len(ln) - 1]
				linebuf += ln
			else:
				if linebuf:
					yield linebuf + ln
					linebuf = ""
				else:
					yield ln

		if linebuf:
			yield linebuf

	def processComments(lines):
		"""
		Remove all comments
		Sanitize after
		"""
		commentStart = re.compile(r'/[/\*]')
		commentEnd = re.compile(r'\*/')
		blockComment = False
		for ln in lines:
			startPos = 0
			startMatch = None
			if blockComment:
				ln = "/*" + ln
			while True:
				startMatch = commentStart.search(ln, startPos)
				if startMatch:
					if startMatch.group(0) == "//":
						blockComment = False
						ln = ln[0:startMatch.start()]
					else:
						endMatch = commentEnd.search(ln, startMatch.end())
						if endMatch:
							ln = ln[0:startMatch.start()] + ln[endMatch.end():]
							startPos = startMatch.start()
							startMatch = None
							blockComment = False
							continue
						else:
							blockComment = True
							ln = ln[0:startMatch.start()]
				break
			yield ln

	def preprocessLabels(lines):
		"""
		Handle labels (seperate lines)
		Sanitize after
		"""
		for ln in lines:
			pos = ln.find(":")
			if pos > 0:
				yield ln[0:pos+1]
				ln = ln[pos+1:]
			yield ln

	def processMacros(lines):
		"""
		Take macro definitions and resolve
		"""
		macroDef = re.compile(r'^(?P<name>[a-zA-Z0-9_\$\.]+)\s*(\((?P<args>[^\)]+)\)|)\s*(?P<value>.*)$')
		macroNameScan = re.compile(r'(?P<name>[a-zA-Z0-9_\$\.]+)')
		macroScan = re.compile(r'(?P<name>[a-zA-Z0-9_\$\.]+)\s*(\((?P<args>[^\)]+)\)|)')

		macros = {}

		def substituteMacros(line):
			startPos = 0
			while True:
				nameMatch = macroNameScan.search(line, startPos)
				if nameMatch:
					name = nameMatch.group("name")
					if name in macros:
						mtype, mfunc = macros[name]
						if mtype == MACRO_VAL:
							line, startPos = string_replace(line, mfunc, nameMatch.start(), nameMatch.end())
							continue
						elif mtype == MACRO_FUNC:
							macroMatch = macroScan.match(line, nameMatch.start())
							if macroMatch:
								line, startPos = string_replace(line, mfunc(argSplitter.split(macroMatch.group("args").strip())), macroMatch.start(), macroMatch.end())
								continue
					startPos = nameMatch.end()
					continue
				break
			return line
		def generateMacroFunc(macroMatch):
			if macroMatch.group("args"):
				#has arguments
				args = argSplitter.split(macroMatch.group("args").strip())
				value = macroMatch.group("value")
				values = []
				extractPos = 0
				startPos = 0
				#Extract tokens and populate array for macro instantiation
				while True:
					nameMatch = macroNameScan.search(value, startPos)
					if nameMatch:
						if nameMatch.group("name") in args:
							values.append(value[extractPos:nameMatch.start()])
							values.append(args.index(nameMatch.group("name")))
							extractPos = nameMatch.end()
						
						startPos = nameMatch.end()
						continue
					break
				values.append(value[extractPos:])

				def macroResolver(params):
					#replace parameters in value
					output = "".join(map(lambda x: params[x] if type(x) == int else str(x), values))
					output = substituteMacros(output)
					return output
					pass
				return (MACRO_FUNC, macroResolver)

			else:
				#just value
				return (MACRO_VAL, substituteMacros(macroMatch.group("value")))

		for line in lines:
			if line.startswith("#"):
				if not line.startswith("#define"):
					raise Exception("Invalid Macro " + line[1:])
				macro = line[len("#define"):].strip()
				macroMatch = macroDef.match(macro)
				if not macroMatch:
					raise Exception("Invalid Macro " + line)
				macros[macroMatch.group("name")] = generateMacroFunc(macroMatch)
			else:
				yield substituteMacros(line)
	def expandSemicolons(lines):
		"""
		Expands semicolons to new lines
		Sanitize after
		"""
		for ln in lines:
			for part in ln.split(";"):
				yield part

	def numberToFill(lines):
		"""
		Convert purely numeric lines into .fill instructions
		"""
		for ln in lines:
			try:
				num = int(ln)
				yield ".fill %s" % (num,)
			except ValueError:
				yield ln

	def restoreRegisters(lines):
		"""
		Restore register to numbers
		"""
		regFormat = re.compile(r"\br(\d)\b")
		for ln in lines:
			startMatch = argSplitter.search(ln)
			if startMatch:
				ln = ln[0:startMatch.end()] + regFormat.sub(r"\1",ln[startMatch.end():])
			yield ln

	def resolveLabels(lines):
		"""
		Sanitize before
		Resolve labels into correct lc2k format
		"""
		clabel = ""
		for ln in lines:
			if ln.endswith(":"):
				if clabel:
					raise Exception("Multiple labels for the same line " + ln)
				clabel = ln[0:len(ln)-1]
				if len(clabel) > 6:
					raise Exception("Label " + clabel + " too long")
			else:
				yield "%-6s %s" % (clabel, ln)
				clabel = ""

	#Um, this is embarrassing. The following code is directly adapted from test code,
	#therefore, they are not aesthetically pleasing. The following code essentially 
	#invokes different parts of the program chained up through a series of (Python)
	#generators, allowing parts of the source code file to be processed in a pipeline,
	#making use of smaller amounts of memory (does it really matter with LC2K?), and 
	#easier/clearer to write
	finput = sys.stdin
	foutput = sys.stdout
	if args.sourceFile[0] != "-":
		finput = open(args.sourceFile[0], 'r')
	if args.destFile[0] != "-":
		foutput = open(args.destFile[0], 'w')
	#Data is passed in this direction >------->-------------->---------------->--------
	processor = chain(finput, cleanLines, processEOL, processComments, preprocessLabels,
		cleanLines, processMacros, expandSemicolons, cleanLines, numberToFill,
		restoreRegisters, resolveLabels)
	for ln in processor:
		foutput.write(ln)
		foutput.write("\n")

if __name__ == "__main__":
	main()