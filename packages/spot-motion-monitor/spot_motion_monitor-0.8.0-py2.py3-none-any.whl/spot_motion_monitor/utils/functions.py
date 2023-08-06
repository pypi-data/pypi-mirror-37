#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from matplotlib import cm
import numpy as np

__all__ = ['getLutFromColorMap', 'passFrame']

def getLutFromColorMap(name):
    """Get a LUT from a color map.

    Parameters
    ----------
    name : str
        The name of the color map to retrieve.

    Returns
    -------
    np.array
        The LUT translated from color map.
    """
    colorMap = getattr(cm, name)
    lut = (np.array(colorMap.colors) * 256).astype('int')
    return lut

def passFrame(*args):
    """Say frame is valid no matter what arguments are.

    Parameters
    ----------
    *args
        Any arguments required by API.

    Returns
    -------
    bool
        Always True to pass the frame check.
    """
    return True
