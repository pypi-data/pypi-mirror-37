# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .memo import PimMemo
from .category import Category
from .notereport import ReportOdt


def register():
    Pool.register(
        Category,
        PimMemo,
        module='pim_memos', type_='model')
    Pool.register(
        ReportOdt,
        module='pim_memos', type_='report')
