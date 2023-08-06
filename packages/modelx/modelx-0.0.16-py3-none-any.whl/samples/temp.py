# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 21:42:26 2018

@author: fumito
"""

import modelx as mx
from modelx import defcells
import modelx.core

modelx.core.system.callstack.max_depth = 10

m, s = mx.new_model(), mx.new_space()

@defcells
def cash(t):
    return cash(t-1) + interest(t) + cashin(t)

@defcells
def cashin(t):
    return 0

@defcells
def interest(t):
    return cash(t-1) * interest_rate


s.interest_rate = 0.03
# cash[1] = 100
interest(3)