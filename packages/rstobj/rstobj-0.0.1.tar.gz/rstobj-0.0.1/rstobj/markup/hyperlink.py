# -*- coding: utf-8 -*-

import attr
from ..base import RstObj


@attr.s
class URI(RstObj):
    title = attr.ib()
    link = attr.ib()


URL = URI
