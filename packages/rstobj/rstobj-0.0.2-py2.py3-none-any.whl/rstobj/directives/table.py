# -*- coding: utf-8 -*-

"""
table related directives.
"""

import attr
from .base import Directive


@attr.s
class ListTable(Directive):
    """
    Example::

        .. list-table:: Title of the table
            :widths: 10 10 10
            :header-rows: 1

            * - Header1
              - Header2
              - Header3
            * - Value1
              - Value2
              - Value3
    """
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
