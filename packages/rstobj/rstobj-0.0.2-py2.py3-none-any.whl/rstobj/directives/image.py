# -*- coding: utf-8 -*-

"""
image related directives.
"""

import attr
from .base import Directive


@attr.s
class Image(Directive):
    """
    ``.. image::`` directive.
    """
    uri = attr.ib(default=None)
    height = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    width = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    scale = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    alt_text = attr.ib(default=None)
    align = attr.ib(default=None)

    meta_directive_keyword = "image"
    meta_not_none_fields = ("uri",)

    class AlignOptions(object):
        left = "left"
        center = "center"
        right = "right"
        top = "top"
        middle = "middle"
        bottom = "bottom"

    @align.validator
    def check_align(self, attribute, value):  # pragma: no cover
        if value not in [None, "left", "center", "right", "top", "middle", "bottom"]:
            raise ValueError(
                "ListTable.align has to be one of 'left', 'center', 'right', 'top', 'middle', 'bottom'!"
            )

    @property
    def arg(self):
        return self.uri
