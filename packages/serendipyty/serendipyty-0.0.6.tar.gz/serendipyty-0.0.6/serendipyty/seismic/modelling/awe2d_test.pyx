# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:58:34 2016

@author: Filippo Broggini (ETH Zürich) - filippo.broggini@erdw.ethz.ch
"""

# %% Full model run on 2D staggered grid
# O(2,2)

print('After before')

from timeit import default_timer as timer
import numpy as np
cimport numpy as np

print('After numpy import')

# Cython imports
cimport cython
from cython.parallel cimport prange, parallel
#cimport serendipyty.seismic.modelling.generate_pml_coeff as generate_pml_coeff

print('After cython imports')

# Set floating point precision
ctypedef double MVTYPE
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

ver=2
print('version {}'.format(ver))

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def forward(numero):
    r"""Acoustic wave equation forward modeling.

    Finite-difference time-domain solution of the 2D acoustic wave equation
    implemented using Cython.

    Parameters
    ----------
    model : BaseModel
        Model class.
    src : BaseSource
        Source class.
    outparam: list
        List of outputs.
    bc: BaseBc
        Boundary conditions class.
    hpc: BaseHpc
        HPC class.
    verbose: int
        Set to 1 output more information.

    Returns
    -------
    outputs: dict
        Dictionary containing the outputs required by the input outparam list.
    """

    print('Supercazzola: {}'. format(numero))
    
    return 'Ciaone'