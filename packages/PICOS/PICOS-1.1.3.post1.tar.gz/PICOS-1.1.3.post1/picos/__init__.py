# coding: utf-8

#-------------------------------------------------------------------------------
# Copyright (C) 2012-2017 Guillaume Sagnol
# Copyright (C)      2018 Maximilian Stahlberg
#
# This file is part of PICOS.
#
# PICOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PICOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

import os

from .problem import *
from .expression import *
from .constraint import *
from .tools import sum,lse,new_param,diag,diag_vect,geomean,norm,tracepow,trace,detrootn,QuadAsSocpError,NotAppropriateSolverError,NonConvexError,flow_Constraint,ball,simplex,truncated_simplex,partial_trace,partial_transpose,import_cbf,sum_k_largest,sum_k_largest_lambda,lambda_max,sum_k_smallest,sum_k_smallest_lambda,lambda_min, kron

__all__=['tools','constraint','expression','problem']

LOCATION = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
VERSION_FILE = os.path.join(LOCATION, ".version")

def get_version_info():
    with open(VERSION_FILE, "r") as versionFile:
        return tuple(versionFile.read().strip().split("."))

__version_info__ = get_version_info()
__version__ = '.'.join(__version_info__)
