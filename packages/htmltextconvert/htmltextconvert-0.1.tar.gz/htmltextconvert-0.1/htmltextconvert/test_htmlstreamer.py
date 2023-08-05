from .htmlstreamer import HTMLStreamer


class TestHTMLStreamer:

    def get_stream(self, html):
        parser = HTMLStreamer()
        parser.feed(html)
        parser.close()
        return parser.tokens

    def test_it_streams(self):
        html = "<html>\n\t<p class='bar'>foo<br><img/></p>\n"
        assert self.get_stream(html) == [
            (HTMLStreamer.START, ('html', [])),
            (HTMLStreamer.TEXT, '\n\t'),
            (HTMLStreamer.START, ('p', [('class', 'bar')])),
            (HTMLStreamer.TEXT, 'foo'),
            (HTMLStreamer.STARTEND, ('br', [])),
            (HTMLStreamer.STARTEND, ('img', [])),
            (HTMLStreamer.END, 'p'),
            (HTMLStreamer.TEXT, '\n'),
            (HTMLStreamer.END, 'html'),
        ]

    def test_it_concats_refs(self):
        html = "<p>&amp;hello&#38;</p>"
        assert self.get_stream(html) == [
            (HTMLStreamer.START, ('p', [])),
            (HTMLStreamer.TEXT, '&hello&'),
            (HTMLStreamer.END, 'p'),
        ]

    def test_it_emits_missing_end_tags(self):
        html = "<div><p>"
        assert self.get_stream(html) == [
            (HTMLStreamer.START, ('div', [])),
            (HTMLStreamer.START, ('p', [])),
            (HTMLStreamer.END, 'p'),
            (HTMLStreamer.END, 'div')
        ]

    def test_it_fixes_nesting(self):
        html = "<div>a<p>b</div>"
        assert self.get_stream(html) == [
            (HTMLStreamer.START, ('div', [])),
            (HTMLStreamer.TEXT, 'a'),
            (HTMLStreamer.START, ('p', [])),
            (HTMLStreamer.TEXT, 'b'),
            (HTMLStreamer.END, 'p'),
            (HTMLStreamer.END, 'div')
        ]
