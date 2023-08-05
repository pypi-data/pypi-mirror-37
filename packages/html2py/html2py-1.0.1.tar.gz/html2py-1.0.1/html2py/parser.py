#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parser.

This module parse and analyze an html/xhtml tree for become code.
It support almost all html syntaxes and don't do anything for handle special chars.
For now any kind of comments and text outside root tag will be silently discarded and could be create
problems in parsing.
"""

import lxml


__all__ = ("XMLParser", "HTMLParser")


class XMLParser(object):
    """
    XMLParser class.

    It parse a tree and convert single tags to instructions processable to an YattagFile instance.
    """

    def start_tag(self, tag, data, attrs):
        """
        Open tag.

        It handle tags that have subtags in there.
        """
        start = ("tag", tag, attrs)
        if data:
            return (start, self.text(data))
        else:
            return (start, None)

    def line_tag(self, tag, data, attrs):
        """Handle Linear tags with some data."""
        return ("line", tag, self.handle_quotes(data), attrs)

    def stag_tag(self, tag, attrs):
        """Handle start end tags."""
        return ("stag", tag, attrs)

    def end_tag(self, tag):
        """End of tags that was opened by start_tag."""
        return ("endtag", tag)

    def text(self, text):
        """Handle text and check for space only strings."""
        return ("text", self.handle_quotes(text))

    def comment(self, text):
        """Handle comments; comments will be added with asis."""
        return ("asis", self.handle_quotes("<!--{}-->".format(text)))

    def handle_quotes(self, s):
        """Check if there is any quote in string."""
        if s.find('"') != -1:
            return '""{}""'.format(s)
        else:
            return s

    def parse_tree(self, tree):
        """
        Parse and handle xml tree.

        NOTE: Currently it was tested only with lxml trees.
        """
        if len(tree) > 0:
            start, text = self.start_tag(tree.tag, tree.text, tree.attrib)
            yield start
            if text is not None:
                yield text
        else:
            yield self.line_tag(tree.tag, tree.text, tree.attrib)
        for el in tree:
            if isinstance(el, lxml.etree._Comment):
                # comment
                yield self.comment(el.text)
            elif len(el) > 0:
                # if tag has children
                # start, text = self.start_tag(el.tag, el.text, el.attrib)
                # yield start
                # if text is not None:
                    # yield text
                yield from self.parse_tree(el)
                yield self.end_tag(el.tag)
            else:
                if el.text:
                    # if tag has no children but some data
                    yield self.line_tag(el.tag, el.text, el.attrib)
                else:
                    # if tag has no children and no data
                    yield self.stag_tag(el.tag, el.attrib)


class HTMLParser(XMLParser):
    """
    HTMLParser class.

    As for XMLParser it parse a tree, but handle html only specification.
    BUG: Due to Yattag bug, attributes name that contain alphanumeric character is not supported and may cause errors.
    """

    def __init__(self, *args, **kwargs):
        super(HTMLParser, self).__init__(*args, **kwargs)
        # self.yattagfile.add_instruction(YInst("asis", self.idenstr * self.identation, "<!doctype html>"))

    def stag_tag(self, tag, attrs):
        """Handle html tags that don't work with stag tags (ex: script)."""
        if tag in ("script", "li", "div"):
            return ("line", tag, "", attrs)
        else:
            return ("stag", tag, attrs)
