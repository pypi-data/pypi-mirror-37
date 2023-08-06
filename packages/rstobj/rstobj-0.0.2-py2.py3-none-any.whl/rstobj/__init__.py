#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct RestructuredText markup and directives from Python Code.
"""

__version__ = "0.0.2"
__short_description__ = "Construct RestructuredText markup and directives from Python Code."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from . import directives, markup
except:  # pragma: no cover
    pass
