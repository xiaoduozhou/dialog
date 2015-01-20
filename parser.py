#!/usr/bin/env python3

"""
Dialog parsing module.
"""
__author__ = "Mark Birger"
__date__ = "19 Nov 2014"

import re
from states import Question, Answer, Routine, Literal

class Parser:
    def __init__(self, filename, scope, returns, identation='\t'):
        print("Parsing dialog... ", end="")
        self.scope = scope
        self.returns = returns
        self.identation = identation
        with open(filename) as dialog_file:
            self.lines = dialog_file.read().splitlines()
        self._remove_comments()
        self._remove_whitespaces()
        self._remove_empty_lines()
        self._join_lines()
        self.root = []
        self.stack = []
        self.literals = []
        self._parse()
        print("finished")

    def _remove_comments(self):
        self.lines = [re.sub(r'#.*$', '', line) for line in self.lines]

    def _remove_whitespaces(self):
        self.lines = [re.sub(r'\s*$', '', line) for line in self.lines]

    def _remove_empty_lines(self):
        self.lines = [line for line in self.lines if line != '']

    def _join_lines(self):
        joined = []
        summary = ""
        for line in self.lines:
            if line.endswith("\\"):
                if summary == "":
                    summary += line[:-1]
                else:
                    summary += line.lstrip()[:-1]
            else:
                if summary == "":
                    joined.append(line)
                else:
                    joined.append(summary + line.lstrip())
                    summary = ""
        self.lines = joined

    def _parse_identations(self, line):
        level = 0
        while line.startswith(self.identation):
            level += 1
            line = line[len(self.identation):]
        return level, line

    def _clean_literals(self, current):
        stay = []
        for level in self.literals:
            if level <= current:
                stay.append(level)
        self.literals = stay

    def _parse(self):
        for line in self.lines:
            level, line = self._parse_identations(line)
            self._clean_literals(level)
            #TODO: routine parsing
            if level % 2 == 0: # it's a question
                if level in self.literals:
                    new = Literal(line)
                else:
                    new = Question(line, self.scope)
            else:
                if line.startswith('`') and line.endswith('?`'):
                    new = Routine(line, self.scope, self.returns)
                    self.literals.append(level+1)
                else:
                    new = Answer(line, self.scope)
            self._place_state(level, new)

    def _place_state(self, level, state):
        self.stack = self.stack[:level]
        if not self.stack: # we are at the root
            self.root.append(state)
            self.stack.append(state)
        else:
            self.stack[-1].add(state)
            self.stack.append(state)

    def result(self):
        return self.root

# dlg = Parser("examples/tickets.dlg", globals(),None)














