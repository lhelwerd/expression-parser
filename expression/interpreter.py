#!/usr/bin/env python
"""
Command line interpreter using the expression line parser.
"""

from __future__ import print_function

import cmd
import sys
import traceback
import expression

class Expression_Interpreter(cmd.Cmd):
    """
    Interactive command line interpreter that applies the expression line parser
    to the provided input.
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '>> '
        self.parser = expression.Expression_Parser()

    def default(self, line):
        try:
            self.stdout.write(str(self.parser.parse(line)) + '\n')
        except SyntaxError:
            traceback.print_exc()

    def do_quit(self, line):
        """
        Exit the interpreter.
        """

        if line != '' and line != '()':
            self.stdout.write(line + '\n')
        self._quit()

    @staticmethod
    def _quit():
        sys.exit(1)

def main():
    """
    Main entry point.
    """

    Expression_Interpreter().cmdloop()

if __name__ == '__main__':
    main()
