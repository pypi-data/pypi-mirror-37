# -*- coding: utf-8 -*-

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

    def render(self, indent=None, **kwargs):
        out = self.template.render(obj=self)
        if indent:
            out = "\n".join([
                Options.tab * indent + line
                for line in out.split("\n")
            ])
        return out
