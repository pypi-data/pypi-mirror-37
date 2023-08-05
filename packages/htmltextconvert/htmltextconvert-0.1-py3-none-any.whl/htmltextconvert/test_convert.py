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
from textwrap import dedent
from .htmlstreamer import HTMLStreamer
from . import convert


class TestNormalizeStream:

    def get_stream(self, html):
        parser = HTMLStreamer()
        parser.feed(html)
        parser.close()
        return list(convert.normalize_tags(parser.tokens))

    def test_it_normalizes_tag_case(self):
        assert self.get_stream('<HTML>') == [
            (HTMLStreamer.START, ('html', [])),
            (HTMLStreamer.END, 'html'),
        ]

    def test_it_normalizes_tag_names(self):
        assert self.get_stream('<b><i>') == [
            (HTMLStreamer.START, ('strong', [])),
            (HTMLStreamer.START, ('em', [])),
            (HTMLStreamer.END, 'em'),
            (HTMLStreamer.END, 'strong')
        ]


class TestCollapseWhitespace:
    def process(self, html):
        parser = HTMLStreamer()
        parser.feed(html)
        parser.close()
        return convert.stream_to_html(
            convert.collapse_whitespace(parser.tokens)
        )

    def test_it_collapses_whitespace(self):
        assert self.process('<p></p>') == '<p></p>'
        assert self.process('<p> </p>') == '<p></p>'
        assert self.process('<p> </p> ') == '<p></p>'
        assert self.process(' <p> </p>') == '<p></p>'
        assert self.process('<p> <a></a></p>') == '<p><a></a></p>'
        assert self.process('<p><a></a> </p>') == '<p><a></a></p>'
        assert self.process('<p><a></a> <a></a></p>') == '<p><a></a> <a></a></p>'
        assert self.process('<div> x <div>y</div></div>') == '<div>x<div>y</div></div>'

        html = dedent('''
            <html>
                <head>
                </head>
                <body>
                </body>
            </html>''')
        assert self.process(html) == '<html><head></head><body></body></html>'


class TestHtmlToText:

    def test_it_renders_lists(self):
        html = dedent("""
                    <ul>
                        <li>foo</li>
                        <li>bar</li>
                        <li>baz</li>
                    </ul>""")
        expected = '* foo\n* bar\n* baz\n'
        assert str(convert.html_to_text(html)) == expected

    def test_it_renders_blocks(self):
        html = '<p>p1</p><p>p2</p>'
        expected = 'p1\n\np2\n'
        result = convert.html_to_text(html)
        assert result == expected

    def test_it_replaces_links(self):
        html = '<p>before <a href="https://www.example.com/">link</a> after</p>'
        expected = 'before link <https://www.example.com/> after\n'
        result = convert.html_to_text(html)
        assert result == expected

    def test_it_converts_br_to_newline(self):
        assert convert.html_to_text('a<br>b<br/>c') == 'a\nb\nc\n'

    def test_it_strips_style_script_etc(self):
        html = dedent('''
            <html>
                <head>
                    <title>blah</title>
                    <style>more blah</style>
                    <script>yet more</script>
                </head>
                <body>
                    <p>
                        whoa nelly
                    </p>
                </body>
            </html>''')

        assert convert.html_to_text(html) == 'whoa nelly\n'

    def test_it_handles_refs(self):
        assert convert.html_to_text('&lt;&#x31;&#50&gt;') == '<12>\n'

    def test_it_handles_blockquotes(self):
        html = '<blockquote><p>l1</p></blockquote>'
        assert convert.html_to_text(html) == '  l1\n'

    def test_it_handles_nested_blockquotes(self):
        html = dedent('''
            <blockquote>
                l1
                <blockquote>
                    l2
                </blockquote>
            </blockquote>
            ''')

        assert convert.html_to_text(html) == '  l1\n    l2\n'

    def test_it_handles_nested_blockquotes2(self):
        html = dedent('''
            <p>l0</p>
            <blockquote>
                <p>l1</p>
                <blockquote>
                    <p>l2<br>l2</p>
                </blockquote>
            </blockquote>
            <p>l0</p>
            ''')

        assert convert.html_to_text(html) == 'l0\n\n  l1\n\n    l2\n    l2\n\nl0\n'
