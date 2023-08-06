#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from spot_motion_monitor.utils import getLutFromColorMap

class TestGetLutFromColorMap:

    def test_getLutFromColorMap(self):
        lut = getLutFromColorMap('viridis')
        assert lut.shape == (256, 3)
        assert lut[0].tolist() == [68, 1, 84]
