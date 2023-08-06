# -*- coding: utf-8 -*-

import six
import attr
from attrs_mate import AttrsClass
from .templates import env
from .option import Options


@attr.s
class RstObj(AttrsClass):
    meta_not_none_fields = tuple()

    def validate_not_none_fields(self):
        for field in self.meta_not_none_fields:
            if getattr(self, field) is None:
                msg = "`{}.{}` can't be None!" \
                    .format(self.__class__.__name__, field)
                raise ValueError(msg)

    def __attrs_post_init__(self):
        self.validate_not_none_fields()

    @property
    def template_name(self):
        return "{}.{}.rst".format(self.__module__, self.__class__.__name__)

    @property
    def template(self):
        return env.get_template(self.template_name)

    def render(self, indent=None, first_line_indent=None, **kwargs):
        out = self.template.render(obj=self)
        if indent:
            origin_lines = out.split("\n")
            target_lines = [Options.tab * indent + line.rstrip()
                            for line in origin_lines]
            if first_line_indent is not None:
                if first_line_indent >= 0:
                    target_lines[0] = Options.tab * \
                        first_line_indent + origin_lines[0].rstrip()
                else:  # pragma: no cover
                    raise TypeError
            out = "\n".join(target_lines)
        return out

    @staticmethod
    def str_or_render(value, **kwargs):
        if isinstance(value, RstObj):
            return value.render(**kwargs)
        else:
            return six.text_type(value)
