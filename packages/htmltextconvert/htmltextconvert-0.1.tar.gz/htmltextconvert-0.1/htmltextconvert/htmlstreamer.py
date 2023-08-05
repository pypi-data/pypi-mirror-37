# Copyright 2018 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
from html.parser import HTMLParser
from typing import Any
from typing import List
from typing import Tuple
from html.entities import name2codepoint


class HTMLStreamer(HTMLParser):
    """
    Use Python's stdlib html.parser to convert an HTML document into a
    more convenient iterable stream of (type_, data) tuples.
    """

    START = 'start'
    END = 'end'
    TEXT = 'text'
    STARTEND = 'startend'

    empty = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
             'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__()
        self.tokens: List[Tuple[str, Any]] = []
        self._open: List[str] = []
        self.append = self.tokens.append

    def handle_starttag(self, tag, attrs):
        if tag in self.empty:
            type_ = self.STARTEND
        else:
            self._open.append(tag)
            type_ = self.START
        self.tokens.append((type_, (tag, attrs)))

    def handle_endtag(self, tag):
        while self._open and tag != self._open[-1]:
            self.tokens.append((self.END, self._open.pop()))
        if not self._open:
            return
        self._open.pop()
        self.tokens.append((self.END, tag))

    def handle_startendtag(self, tag, attrs):
        self.tokens.append((self.STARTEND, (tag, attrs)))

    def handle_entityref(self, name):
        return self.handle_charref(str(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        self.handle_data(c)

    def handle_data(self, s):
        if self.tokens and self.tokens[-1][0] == self.TEXT:
            _, text = self.tokens.pop()
            self.tokens.append((self.TEXT, text + s))
        else:
            self.tokens.append((self.TEXT, s))

    def close(self):
        super().close()
        while self._open:
            self.tokens.append((self.END, self._open.pop()))


def html_to_stream(html):
    parser = HTMLStreamer()
    parser.feed(html)
    parser.close()
    return iter(parser.tokens)
