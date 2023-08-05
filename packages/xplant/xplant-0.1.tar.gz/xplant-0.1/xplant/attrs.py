from .six import str_types


class XmlAttributes(dict):
    """
        # A bit different dictionary. Can be created out of single string arguments,
        # tuples with two elements or by keyword arguments.
        # Its __str__ method returns well formed, reproducible xml attributes representation.

        from xplant.attrs import XmlAttributes

        a = XmlAttributes()
        assert str(a) == ''
        assert a == {}

        b = XmlAttributes("one", ("two", 2), three=3)
        # note sorting below
        assert str(b) == ' one three="3" two="2"'
        assert b == {'one': None, 'three': 3, 'two': 2}
    """
    default_attribute_rank = 100
    attribute_precedence_rank = {}
    attribute_name_substitutes = {}
    attribute_value_substitutes = {
        # keys need be written as repr of actual key (because of aliasing e.g. False with 0)
        "True": "true",
        "False": "false",
    }

    def __init__(self, *strings_or_tuples, **keyword_arguments):
        super(XmlAttributes, self).__init__(self._normalize_arguments(strings_or_tuples, keyword_arguments))

    def __str__(self):
        return ''.join(self._generate_xml_representation())

    def _generate_xml_representation(self):
        for key, value in sorted(self.items(), key=self._attribute_name_sorting_key):
            if value is None:
                yield " {}".format(key)
            else:
                yield ' {}="{}"'.format(key, self.attribute_value_substitutes.get(str(value), value))

    @classmethod
    def _attribute_name_sorting_key(cls, element):
        attribute_name = element[0]
        attribute_rank = cls.attribute_precedence_rank.get(attribute_name, cls.default_attribute_rank)
        return attribute_rank, attribute_name

    @classmethod
    def _normalize_arguments(cls, positional_arguments, keyword_arguments):
        for argument in positional_arguments:
            if isinstance(argument, tuple):
                if len(argument) != 2:
                    raise ValueError("Attribute argument must be tuple of 2 elements (name, value).")
                yield argument
            elif isinstance(argument, str_types):
                yield (argument, None)
            else:
                raise ValueError("Couldn't make an attribute & value pair out of {!r}.".format(argument))

        for keyword, keyword_value in keyword_arguments.items():
            reclaimed_keyword = cls.attribute_name_substitutes.get(keyword, keyword)
            yield reclaimed_keyword, keyword_value
