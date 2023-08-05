# -*- coding: utf-8 -*-

import attr
from .base import Directive


@attr.s
class ListTable(Directive):
    data = attr.ib(default=None)
    title = attr.ib(default="")
    index = attr.ib(default=False)
    header = attr.ib(default=True)
    align = attr.ib(default=None)

    meta_directive_keyword = "list-table"
    meta_not_none_fields = ("data",)

    class AlignOptions(object):
        left = "left"
        center = "center"
        right = "right"

    @align.validator
    def check_align(self, attribute, value):
        if value not in [None, "left", "center", "right"]:  # pragma: no cover
            raise ValueError(
                "ListTable.align has to be one of 'left', 'center', 'right'!"
            )

    @property
    def arg(self):
        return self.title
