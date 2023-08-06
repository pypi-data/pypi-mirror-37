#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QDialog

from spot_motion_monitor.views import CentroidPlotConfigTab, PsdPlotConfigTab
from spot_motion_monitor.views.forms.ui_configuration_dialog import Ui_ConfigurationDialog

__all__ = ['PlotConfigurationDialog']

class PlotConfigurationDialog(QDialog, Ui_ConfigurationDialog):
    """Class that generates the dialog for handling plot configuration.

    Attributes
    ----------
    centroidPlotConfigTab : CentroidPlotConfigTab
        Instance of the centroid plot configuration tab.
    psdPlotConfigTab : PsdPlotConfigTab
        Instance of the Power Spectrum Distribution plot configuration tab.
    """

    def __init__(self, parent=None):
        """Initialize the class.

        Parameters
        ----------
        parent : None, optional
            Top-level widget.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.centroidPlotConfigTab = CentroidPlotConfigTab(self)
        self.psdPlotConfigTab = PsdPlotConfigTab(self)

        self.tabWidget.addTab(self.centroidPlotConfigTab, self.centroidPlotConfigTab.name)
        self.tabWidget.addTab(self.psdPlotConfigTab, self.psdPlotConfigTab.name)

    def getPlotConfiguration(self):
        """Get the current plotting configuration from all the tabs.

        Returns
        -------
        dict, dict
            The current centroid and PSD plot configurations.
        """
        centroidConfig = self.centroidPlotConfigTab.getConfiguration()
        psdConfig = self.psdPlotConfigTab.getConfiguration()
        return centroidConfig, psdConfig

    def setPlotConfiguration(self, centroidConfig, psdConfig):
        """Set the current plotting configuration in the plot tab's widgets.

        Parameters
        ----------
        centroidConfig : dict
          The current set of Centroid plot configuration parameters.
        psdConfig : dict
          The current set of Power Spectrum Distribution plot configuration
          parameters.
        """
        self.centroidPlotConfigTab.setConfiguration(centroidConfig)
        self.psdPlotConfigTab.setConfiguration(psdConfig)
