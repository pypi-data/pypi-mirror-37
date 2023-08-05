from contextlib import contextmanager

from .base import Text, XmlItem
from .element import XmlElement, EmptyXmlElement


class XmlDoc(object):
    class DocumentRootTag(object):
        __slots__ = ("children",)

        def __init__(self):
            self.children = []

        def __str__(self):
            return "".join(str(child) for child in self.children)

    def __init__(self):
        self.__tag_stack = [XmlDoc.DocumentRootTag()]

    def __str__(self):
        return str(self.__tag_stack[0])

    @property
    def _top_element(self):
        return self.__tag_stack[-1]

    def append_child(self, element):
        assert isinstance(element, XmlItem), "Can append only instances of XmlItem."
        self._top_element.children.append(element)

    @contextmanager
    def stack(self, element):
        self.append_child(element)
        self.__tag_stack.append(element)
        try:
            yield
        finally:
            self.__tag_stack.pop()

    @contextmanager
    def tag(self, tag_name, *args, **kwargs):
        tag = XmlElement(tag_name, *args, **kwargs)
        with self.stack(tag):
            yield

    def text(self, *text):
        for t in text:
            self.append_child(Text(t))

    def line(self, tag_name, content="", *args, **kwargs):
        tag = XmlElement(tag_name, *args, **kwargs)
        tag.children.append(Text(content))
        self.append_child(tag)

    def stag(self, tag_name, *args, **kwargs):
        tag = EmptyXmlElement(tag_name, *args, **kwargs)
        self.append_child(tag)
