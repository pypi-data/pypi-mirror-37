#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import spot_motion_monitor.utils as utils
from spot_motion_monitor.views import PsdPlotConfigTab

class TestPsdPlotConfigTab:

    def test_parametersAfterConstruction(self, qtbot):
        configTab = PsdPlotConfigTab()
        qtbot.addWidget(configTab)
        assert configTab.name == 'PSD'
        assert configTab.waterfallColorMapComboBox.count() == 5

    def test_setParametersFromConfiguration(self, qtbot):
        configTab = PsdPlotConfigTab()
        qtbot.addWidget(configTab)

        config = {'waterfall': {'numBins': 15, 'colorMap': 'plasma'},
                  'xPSD': {'autoscale': True, 'minimum': None, 'maximum': None},
                  'yPSD': {'autoscale': False, 'minimum': 10, 'maximum': 1320}}
        configTab.setConfiguration(config)
        assert int(configTab.waterfallNumBinsLineEdit.text()) == config['waterfall']['numBins']
        assert configTab.waterfallColorMapComboBox.currentText() == config['waterfall']['colorMap']
        assert utils.checkStateToBool(configTab.autoscaleX1dCheckBox.checkState()) is True
        assert configTab.x1dMaximumLineEdit.isEnabled() is False
        assert utils.checkStateToBool(configTab.autoscaleY1dCheckBox.checkState()) is False
        assert configTab.y1dMaximumLineEdit.isEnabled() is True
        assert int(configTab.y1dMaximumLineEdit.text()) == config['yPSD']['maximum']

    def test_getParametersFromConfiguration(self, qtbot):
        configTab = PsdPlotConfigTab()
        qtbot.addWidget(configTab)
        truthConfig = {'waterfall': {'numBins': 35, 'colorMap': 'magma'},
                       'xPSD': {'autoscale': True},
                       'yPSD': {'autoscale': False, 'maximum': 1320.0}}
        configTab.waterfallNumBinsLineEdit.setText(str(truthConfig['waterfall']['numBins']))
        configTab.waterfallColorMapComboBox.setCurrentText(truthConfig['waterfall']['colorMap'])
        configTab.autoscaleX1dCheckBox.setChecked(utils.boolToCheckState(truthConfig['xPSD']['autoscale']))
        configTab.autoscaleY1dCheckBox.setChecked(utils.boolToCheckState(truthConfig['yPSD']['autoscale']))
        configTab.y1dMaximumLineEdit.setText(str(truthConfig['yPSD']['maximum']))
        config = configTab.getConfiguration()
        assert config == truthConfig
