#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from .output import PythonOutput, CallInstruction

__all__ = ("YattagOutput", )


class YattagOutput(PythonOutput):
    """
    YattagOutput.

    This class provide an interface to write a python file with yattag library.
    Yattag: https://github.com/leforestier/yattag
    """

    RE_ONLY_SPACE = re.compile(r"^\s+$")
    RE_EXTRA_SPACES = re.compile(r"(.*)\s{3,}(.*)")

    def __init__(self, *args, doctype=None, **kwargs):
        super(YattagOutput, self).__init__(*args, **kwargs)
        if doctype:
            self.instructions.append(CallInstruction("asis", self.identation * self.idenstr, doctype))

    def process_tree(self, tree):
        """Convert parsed tags."""
        try:
            for el in self.parser.parse_tree(tree):
                if el[0] == "tag":
                    self.instructions.append(CallInstruction(el[0], self.identation * self.idenstr,
                                                             el[1], **el[2], use_with=True))
                    self.identation += 1
                elif el[0] == "endtag":
                    self.identation -= 1
                elif el[0] in ("line", ):
                    self.instructions.append(CallInstruction(el[0], self.identation * self.idenstr,
                                                             el[1], el[2], **el[3]))
                elif el[0] in ("stag", ):
                    self.instructions.append(CallInstruction(el[0], self.identation * self.idenstr,
                                                             el[1], **el[2]))
                elif el[0] in ("text", "asis"):
                    text = el[1]
                    if self.del_unused_spaces:
                        if self.RE_ONLY_SPACE.search(el[1]) is None:
                            text = self.RE_EXTRA_SPACES.sub(r"\1\2", text)
                        else:
                            continue
                    self.instructions.append(CallInstruction(el[0],
                                                             self.identation * self.idenstr,
                                                             text))
                else:
                    raise NotImplementedError("Instructions {} isn't yet implemented.".format(el[0]))
        except StopIteration:
            pass
