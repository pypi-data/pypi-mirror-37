# -*- coding: utf-8 -*-

import attr
from ..base import RstObj


@attr.s
class Directive(RstObj):
    class_ = attr.ib(default=None)
    name = attr.ib(default=None)

    meta_directive_keyword = None
