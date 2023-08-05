#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Output module.

This module provides an interface to generate python instructions to a script file.
"""

__all__ = ("PythonInstruction", "PythonOutput", "CallInstruction")

from abc import ABCMeta, abstractmethod


class PythonInstruction(object):
    """Base representation of a Python instruction."""

    __metaclass__ = ABCMeta
    RESERVED_KEYWORDS = ("class", "for")

    @abstractmethod
    def genstr(self):
        """Generate string from class datas."""
        pass


class CallInstruction(PythonInstruction):
    """Python call representation."""

    __slots__ = ("func", "idenstr", "use_with", "args", "kwargs")

    def __init__(self, func, idenstr, *args, use_with=False, **kwargs):
        super(CallInstruction, self).__init__()
        self.func = func
        self.idenstr = idenstr
        self.use_with = use_with
        self.args = args
        self.kwargs = kwargs

    def genstr(self):
        """Generate string from given attributes."""
        if self.use_with:
            # import pdb; pdb.set_trace()
            return "{}with {}({}{}):".format(self.idenstr,
                                             self.func,
                                             ", ".join(['"{}"'.format(x) for x in self.args]),
                                             self._escape_keywords(self.kwargs))

        else:
            # import pdb; pdb.set_trace()
            return "{}{}({}{})".format(self.idenstr,
                                       self.func,
                                       ", ".join(['"{}"'.format(x) for x in self.args]),
                                       self._escape_keywords(self.kwargs))

    def _escape_keywords(self, attrs):
        reserved = {}
        for key, val in attrs.items():
            if key in self.RESERVED_KEYWORDS or key.find("-") != -1:
                reserved[key] = val

        if reserved:
            for key in reserved:
                del attrs[key]
            return ", **dict({}{})".format(reserved, "".join([', {}="{}"'.format(key, val)
                                                              for key, val in attrs.items()]))
        else:
            return "".join([', {}="{}"'.format(key, val) for key, val in self.kwargs.items()])


class PythonOutput(object):
    """
    Main interface to write python code.

    It need PythonInstruction objects, processing parsed data to write code.
    It just write instructions, do not provide any kind of wrapping in function or imports;
    see html2py.converter to do this.
    """

    LINE_END = "\n"

    def __init__(self, stream, parser, identation=0, idenstr="\t", del_unused_spaces=False):
        super(PythonOutput, self).__init__()
        self.stream = stream
        self.parser = parser
        self.identation = identation
        self.idenstr = idenstr
        self.del_unused_spaces = del_unused_spaces
        self.instructions = []

    def apply(self):
        """Write all instructions to given stream."""
        for inst in self.instructions:
            self.stream.write(inst.genstr().replace("\n", "\\n") + self.LINE_END)
