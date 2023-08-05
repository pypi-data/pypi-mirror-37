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
from collections import deque
from html import escape
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
import itertools

import textwrap

from .htmlstreamer import HTMLStreamer
from .htmlstreamer import html_to_stream


inline_elements = {'a', 'abbr', 'acronym', 'b', 'bdo', 'big', 'br', 'button',
                   'cite', 'code', 'dfn', 'em', 'i', 'img', 'input', 'kbd',
                   'label', 'map', 'object', 'q', 'samp', 'select', 'small',
                   'span', 'strong', 'sub', 'sup', 'textarea', 'time', 'tt',
                   'var'}


def window(seq, n=2, empty=None):
    seq = iter(seq)
    win = deque((empty for _ in range(n)), maxlen=n)
    append = win.append
    for e in seq:
        append(e)
        yield win
    for _ in range(n - 1):
        append(empty)
        yield win


def is_block(tag: str) -> bool:
    if isinstance(tag, tuple):
        tag, _ = tag
    return tag not in inline_elements


def stream_to_html(stream: Iterable) -> str:
    """
    Render a stream produced by
    :class:htmlconvertext.htmlstreamer.HTMLStreamer` back into an HTMl
    document.
    """
    buf: List[str] = []
    write = buf.append
    for type_, data in stream:
        if type_ in {HTMLStreamer.START, HTMLStreamer.STARTEND}:
            tag, attrs = data
            write(f'<{tag}')
            write(''.join(' {k}="{v}"'.format(k, escape(v)) for k, v in attrs))
            if type_ == HTMLStreamer.STARTEND:
                write('/>')
            else:
                write('>')
        elif type_ == HTMLStreamer.END:
            write(f'</{data}>')
        elif type_ == HTMLStreamer.TEXT:
            write(escape(data))
    return ''.join(buf)


def normalize_tags(stream):
    """
    Normalize tag names, mapping deprecated tags to newer names (eg '<b>'
    becomes '<strong>'), and forcing tag names to lower case
    """
    tagmap = {'b': 'strong',
              'i': 'em',
              }
    for type_, data in stream:
        if type_ in {HTMLStreamer.START, HTMLStreamer.STARTEND}:
            tag, attrs = data
            tag = tag.lower()
            tag = tagmap.get(tag, tag)
            yield type_, (tag, attrs)
        elif type_ == HTMLStreamer.END:
            tag = data
            tag = tag.lower()
            tag = tagmap.get(tag, tag)
            yield type_, tag
        else:
            yield type_, data


def collapse_whitespace(stream: Iterable) -> Iterable:
    """
    Remove whitespace except around inline elements
    """
    #: Stack of (tag, text-content) tuples
    tagstack: List[Tuple[str, str]] = [('', '')]

    windowed = window(stream, 2, empty=(None, None))
    next(windowed, None)

    for a, b in windowed:

        type_, data = a
        peek_type, peek_data = b

        if type_ == HTMLStreamer.START:
            yield type_, data
            tagstack.append((data[0], ''))

        elif type_ == HTMLStreamer.TEXT:
            if any(t in {'pre', 'code'} for t, _ in tagstack):
                yield type_, data
            else:
                container, last_sibling = tagstack[-1]
                in_block = is_block(container) and is_block(last_sibling)
                if in_block:
                    data = data.lstrip()
                if peek_type in {HTMLStreamer.START, HTMLStreamer.END} and \
                        is_block(peek_data):
                    data = data.rstrip()
                if data:
                    yield type_, data
        else:
            yield type_, data


def convert_stream(stream: Iterable) -> str:
    """
    Convert a stream produced by
    :class:htmlconvertext.htmlstreamer.HTMLStreamer`
    into a nicely formatted plain text string
    """
    indent_level = 0
    list_indent_level = -1

    tagstack: List[Tuple[str, Dict]] = []
    output = ['']
    write = output.append

    def write_append(s):
        output[-1] += s

    def push_indent():
        nonlocal indent_level
        indent_level += 1

    def push_list_indent():
        nonlocal list_indent_level
        list_indent_level += 1

    def pop_indent():
        nonlocal indent_level
        indent_level -= 1

    def pop_list_indent():
        nonlocal list_indent_level
        list_indent_level -= 1

    def indent():
        level = indent_level + max(0, list_indent_level)
        text = output[-1]
        if level > 0:
            output[-1] = textwrap.indent(text, '  ')

    def reformat(format_str):
        def reformat():
            text = output[-1]
            formatted = format_str.format(text=text)
            output[-1] = formatted
        return reformat

    def format_ahref():
        link = ''
        attrs = dict(tagstack[-1][1])
        text = output[-1]
        if 'href' in attrs:
            link = f' <{attrs["href"]}>'
        output[-1] = f'{text}{link}'

    def add_separator_before_block(separator='\n'):
        def add_separator_before_block():
            if not output:
                return
            if not is_block(tagstack[-1][0]):
                return
            if output[-1].endswith(separator):
                return

            parents = ((tag, content)
                       for (tag, _), content in reversed(
                           list(zip(tagstack, output))))
            nonempty_ancestors = itertools.dropwhile(
                lambda item: not item[1] and is_block(item[0][0]),
                parents
            )
            last_content = next((c for t, c in nonempty_ancestors), '')
            if last_content and not last_content.endswith(separator):
                overlap = list(itertools.takewhile(
                    lambda item: item[0] == item[1],
                    zip(reversed(last_content), separator)))
                output[-1] += separator[len(overlap):]

        return add_separator_before_block

    def drop_content():
        output[-1] = ''

    start_actions = {
        'blockquote': [push_indent, add_separator_before_block()],
        'ul': [push_list_indent, add_separator_before_block()],
        'ol': [push_list_indent, add_separator_before_block()],
        'p': [add_separator_before_block('\n\n')],
        '*': [add_separator_before_block()],
    }
    end_actions = {
        'strong': [reformat('*{text}*')],
        'em': [reformat('_{text}_')],
        'code': [reformat('`{text}`')],
        'blockquote': [reformat('{text}\n'), indent, pop_indent],
        'br': [reformat('{text}\n')],
        'ul': [reformat('{text}\n\n')],
        'li': [reformat('* {text}\n')],
        'a': [format_ahref],
        'script': [drop_content],
        'style': [drop_content],
        'title': [drop_content],
    }

    stream = list(stream)
    for type_, data in stream:
        assert len(tagstack) == len(output) - 1
        if type_ == HTMLStreamer.START:
            tag, attrs = data
            tagstack.append((tag, attrs))
            actions = start_actions.get(tag, start_actions['*'])
            for fn in actions:
                fn()
            write('')

        elif type_ == HTMLStreamer.STARTEND:
            tag, attrs = data
            actions = end_actions.get(tag, [])
            for fn in actions:
                fn()

        elif type_ == HTMLStreamer.END:
            tag = data
            actions = end_actions.get(tag, [])
            if not isinstance(actions, (tuple, list)):
                actions = [actions]
            for fn in actions:
                fn()
            tagstack.pop()
            if len(output) > 1:
                # Squash this tag's output into its parent
                output[-2:] = [''.join(output[-2:])]

        elif type_ == HTMLStreamer.TEXT:
            write_append(data)

    return ''.join(output).rstrip() + '\n'


def html_to_text(s: str) -> str:
    stream = html_to_stream(s)
    stream = normalize_tags(stream)
    stream = collapse_whitespace(stream)
    result = convert_stream(stream)
    return result
