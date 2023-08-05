from .attrs import XmlAttributes
from .base import IndentableStringItem, XmlItem


class EmptyXmlElement(XmlItem):
    attribute_processor = XmlAttributes
    """ E.g.: <br />, <hr /> or <img src="#" alt="" /> """
    __slots__ = ("_tag_name", "attributes")

    def __init__(self, tag_name, *args, **kwargs):
        self._tag_name = tag_name
        self.attributes = self.attribute_processor(*args, **kwargs)

    @property
    def tag_name(self):
        return self._tag_name

    def build_lines(self):
        tag_body = "<%s%s />" % (self.tag_name, self.attributes)
        return [IndentableStringItem(tag_body)]


class XmlElement(EmptyXmlElement):
    __slots__ = ("_tag_name", "attributes", "children")
    max_line_width = 100

    def __init__(self, tag_name, *args, **kwargs):
        super(XmlElement, self).__init__(tag_name, *args, **kwargs)
        self.children = []

    def build_lines(self):
        begin_tag = "<%s%s>" % (self.tag_name, self.attributes)
        end_tag = "</%s>" % self.tag_name
        children_lines = [line for child in self.children for line in child.build_lines()]

        if len(children_lines) <= 1:
            # try to fit it in single line
            parts = [begin_tag] + [str(l) for l in children_lines] + [end_tag]
            total_length = sum(map(len, parts))
            if total_length <= self.max_line_width:
                return [IndentableStringItem("".join(parts))]

        for child_line in children_lines:
            child_line.increase_indent()
        return [IndentableStringItem(begin_tag)] + children_lines + [IndentableStringItem(end_tag)]
