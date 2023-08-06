#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from spot_motion_monitor.views import VimbaCameraConfigTab

class TestVimbaCameraConfigTab:

    def test_parametersAfterConstruction(self, qtbot):
        vcConfigTab = VimbaCameraConfigTab()
        qtbot.addWidget(vcConfigTab)

        assert vcConfigTab.name == 'Vimba'

    def test_setParametersFromConfiguration(self, qtbot):
        vcConfigTab = VimbaCameraConfigTab()
        qtbot.addWidget(vcConfigTab)

        config = {'roiSize': 20, 'roiFluxMinimum': 1000, 'roiExposureTime': 5000}
        vcConfigTab.setConfiguration(config)

        assert int(vcConfigTab.roiSizeLineEdit.text()) == config['roiSize']
        assert int(vcConfigTab.roiFluxMinLineEdit.text()) == config['roiFluxMinimum']
        assert int(vcConfigTab.roiExposureTimeLineEdit.text()) == config['roiExposureTime']

    def test_getParametersFromConfiguration(self, qtbot):
        vcConfigTab = VimbaCameraConfigTab()
        qtbot.addWidget(vcConfigTab)
        vcConfigTab.show()

        truthConfig = {'roiSize': 75, 'roiFluxMinimum': 1000, 'roiExposureTime': 3000}

        vcConfigTab.roiSizeLineEdit.setText(str(truthConfig['roiSize']))
        vcConfigTab.roiFluxMinLineEdit.setText(str(truthConfig['roiFluxMinimum']))
        vcConfigTab.roiExposureTimeLineEdit.setText(str(truthConfig['roiExposureTime']))
        config = vcConfigTab.getConfiguration()
        assert config == truthConfig
