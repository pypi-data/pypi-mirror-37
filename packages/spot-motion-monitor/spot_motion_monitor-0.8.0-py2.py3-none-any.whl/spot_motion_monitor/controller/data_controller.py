#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from spot_motion_monitor.models import BufferModel, FullFrameModel, RoiFrameModel
from spot_motion_monitor.utils import FrameRejected, FullFrameInformation
from spot_motion_monitor.utils import InformationUpdater, STATUSBAR_FAST_TIMEOUT

__all__ = ["DataController"]

class DataController():

    """This class manages the interactions between the information calculated
       by a particular frame model and the CameraDataWidget.

    Attributes
    ----------
    bufferModel : TYPE
        Description
    cameraDataWidget : .CameraDataWidget
        An instance of the camera data widget.
    fullFrameModel : .FullFrameModel
        An instance of the full frame calculation model.
    roiFrameModel : .RoiFrameModel
        An instance of the ROI frame calculation model.
    updater : .InformationUpdater
        An instance of the information updater.
    """

    def __init__(self, cdw):
        """Initialize the class.

        Parameters
        ----------
        cdw : .CameraDataWidget
            An instance of the camera data widget.
        """
        self.cameraDataWidget = cdw
        self.fullFrameModel = FullFrameModel()
        self.roiFrameModel = RoiFrameModel()
        self.bufferModel = BufferModel()
        self.updater = InformationUpdater()
        self.roiResetDone = False

    def getBufferSize(self):
        """Get the buffer size of the buffer data model.

        Returns
        -------
        int
            The buffer size that the buffer model holds.
        """
        return self.bufferModel.bufferSize

    def getCentroidForUpdate(self, frame):
        """Calculate centroid from frame for offset update.

        Parameters
        ----------
        frame : numpy.array
            A frame from a camera CCD.

        Returns
        -------
        GenericInformation
            The instance containing the results of the calculations.
        """
        return self.fullFrameModel.calculateCentroid(frame)

    def getCentroids(self, isRoiMode):
        """Return the current x, y coordinate of the centroid.

        Parameters
        ----------
        isRoiMode : bool
            True is system is in ROI mode, False if in Full Frame mode.

        Returns
        -------
        (float, float)
            The x and y pixel coordinates of the most current centroid.
            Return (None, None) if not in ROI mode.
        """
        if isRoiMode:
            return self.bufferModel.getCentroids()
        else:
            return (None, None)

    def getPsd(self, isRoiMode, currentFps):
        """Return the power spectrum distribution (PSD).

        Parameters
        ----------
        isRoiMode : bool
            True is system is in ROI mode, False if in Full Frame mode.
        currentFps : float
            The current Frames per Second rate from the camera.

        Returns
        -------
        (numpy.array, numpy.array, numpy.array)
            The PSDX, PSDY and Frequencies from the PSD calculation.
        """
        if isRoiMode:
            return self.bufferModel.getPsd(currentFps)
        else:
            return (None, None, None)

    def passFrame(self, frame, currentStatus):
        """Get a frame, do calculations and update information.

        Parameters
        ----------
        frame : numpy.array
            A frame from a camera CCD.
        currentStatus : .CameraStatus
            Instance containing the current camera status.
        """
        if frame is None:
            return
        try:
            if currentStatus.isRoiMode:
                if not self.roiResetDone:
                    self.cameraDataWidget.reset()
                    self.roiResetDone = True
                genericFrameInfo = self.roiFrameModel.calculateCentroid(frame)
                self.bufferModel.updateInformation(genericFrameInfo, currentStatus.frameOffset)
            else:
                if self.roiResetDone:
                    self.cameraDataWidget.reset()
                    self.roiResetDone = False
                genericFrameInfo = self.fullFrameModel.calculateCentroid(frame)
                fullFrameInfo = FullFrameInformation(int(genericFrameInfo.centerX),
                                                     int(genericFrameInfo.centerY),
                                                     genericFrameInfo.flux, genericFrameInfo.maxAdc)
                self.cameraDataWidget.updateFullFrameData(fullFrameInfo)
        except FrameRejected as err:
            self.updater.displayStatus.emit(str(err), STATUSBAR_FAST_TIMEOUT)

    def setBufferSize(self, value):
        """Set the buffer size on the buffer model.

        Parameters
        ----------
        value : int
            The requested buffer size.
        """
        self.bufferModel.bufferSize = value

    def setFrameChecks(self, fullFrameCheck, roiFrameCheck):
        """Set the frame checks to the corresponding models.

        Parameters
        ----------
        fullFrameCheck : func
            The function capturing the full frame check.
        roiFrameCheck : func
            The function capturing the ROI frame check.
        """
        self.fullFrameModel.frameCheck = fullFrameCheck
        self.roiFrameModel.frameCheck = roiFrameCheck

    def showRoiInformation(self, show, currentFps):
        """Display the current ROI information on camera data widget.

        Parameters
        ----------
        show : bool
            Flag that determines if information is shown.
        currentFps : int
            The current camera FPS.
        """
        if show:
            roiFrameInfo = self.bufferModel.getInformation(currentFps)
            self.cameraDataWidget.updateRoiFrameData(roiFrameInfo)
