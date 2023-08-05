class StringItem(object):
    __slots__ = ("content",)

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def increase_indent(self):
        """ Action."""


class IndentableStringItem(StringItem):
    """
        Caches an arbitrary content, collects indent value info and is able to return its value with the indent.
    """
    __slots__ = ("content", "indent_level")
    single_indent_value = "  "

    def __init__(self, content):
        super(IndentableStringItem, self).__init__(content)
        self.indent_level = 0

    def increase_indent(self):
        self.indent_level += 1

    @property
    def indent_value(self):
        return self.single_indent_value * self.indent_level

    def __str__(self):
        return "%s%s" % (self.indent_value, self.content)


class XmlItem(object):

    def build_lines(self):
        abstract_method_error = "This method is supposed to be overridden in derived {!r} class."
        raise NotImplementedError(abstract_method_error.format(self.__class__.__name__))

    def __str__(self):
        return "\n".join(str(l) for l in self.build_lines())


class Text(XmlItem):
    __slots__ = ("_text",)

    def __init__(self, text):
        self._text = text

    def build_lines(self):
        return [IndentableStringItem(l) for l in self._text.split("\n")]


class PlainText(Text):
    __slots__ = ("_text",)

    def build_lines(self):
        return [StringItem(str(self))]


class Comment(Text):
    __slots__ = ("_text",)

    def __str__(self):
        return "<!-- %s -->" % self._text


class CdataTag(PlainText):
    __slots__ = ("_text",)

    def __str__(self):
        return "<![CDATA[%s]]>" % self._text
