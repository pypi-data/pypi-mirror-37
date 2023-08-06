# -*- coding: utf-8 -*-

import attr
from ..base import RstObj


@attr.s
class URI(RstObj):
    """
    Example::

        `title <link>`_
    """
    title = attr.ib()
    link = attr.ib()


URL = URI


@attr.s
class RefLabel(RstObj):
    label = attr.ib()


@attr.s
class Reference(RstObj):
    """
    Example::

        :ref:`title <label`
    """
    title = attr.ib()
    label = attr.ib()


Ref = Reference
