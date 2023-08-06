#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import numpy as np

from spot_motion_monitor.camera import CameraStatus
from spot_motion_monitor.controller import DataController
from spot_motion_monitor.utils import FrameRejected, GenericFrameInformation, RoiFrameInformation
from spot_motion_monitor.utils import passFrame
from spot_motion_monitor.views import CameraDataWidget

class TestDataController():

    def setup_class(cls):
        cls.frame = np.ones((3, 5))
        cls.fullFrameStatus = CameraStatus(24, False, (0, 0), True)
        cls.roiFrameStatus = CameraStatus(40, True, (264, 200), True)

    def test_parametersAfterConstruction(self, qtbot):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        assert dc.cameraDataWidget is not None
        assert dc.updater is not None
        assert dc.fullFrameModel is not None
        assert dc.roiFrameModel is not None
        assert dc.bufferModel is not None
        assert dc.roiResetDone is False

    def test_updateFullFrameData(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        mockCameraDataWidgetReset = mocker.patch.object(cdw, 'reset')
        mocker.patch('spot_motion_monitor.views.camera_data_widget.CameraDataWidget.updateFullFrameData')
        dc.fullFrameModel.calculateCentroid = mocker.Mock(return_value=GenericFrameInformation(300.3,
                                                                                               400.2,
                                                                                               32042.42,
                                                                                               145.422,
                                                                                               70,
                                                                                               None))
        dc.passFrame(self.frame, self.fullFrameStatus)
        assert dc.cameraDataWidget.updateFullFrameData.call_count == 1
        assert mockCameraDataWidgetReset.call_count == 0
        assert dc.roiResetDone is False
        dc.roiResetDone = True
        dc.passFrame(self.frame, self.fullFrameStatus)
        assert mockCameraDataWidgetReset.call_count == 1
        assert dc.roiResetDone is False

    def test_failedFrame(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        mocker.patch('spot_motion_monitor.views.camera_data_widget.CameraDataWidget.updateFullFrameData')
        dc.fullFrameModel.calculateCentroid = mocker.Mock(side_effect=FrameRejected)
        dc.passFrame(self.frame, self.fullFrameStatus)
        assert dc.cameraDataWidget.updateFullFrameData.call_count == 0

    def test_updateRoiFrameData(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        mockCameraDataWidgetReset = mocker.patch.object(cdw, 'reset')
        mockBufferModelUpdateInfo = mocker.patch.object(dc.bufferModel, 'updateInformation')
        dc.roiFrameModel.calculateCentroid = mocker.Mock(return_value=GenericFrameInformation(242.3,
                                                                                              286.2,
                                                                                              2519.534,
                                                                                              104.343,
                                                                                              50,
                                                                                              1.532))

        dc.passFrame(self.frame, self.roiFrameStatus)
        assert mockCameraDataWidgetReset.call_count == 1
        assert mockBufferModelUpdateInfo.call_count == 1
        dc.passFrame(self.frame, self.roiFrameStatus)
        assert mockCameraDataWidgetReset.call_count == 1
        assert mockBufferModelUpdateInfo.call_count == 2

    def test_getBufferSize(self, qtbot):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        bufferSize = dc.getBufferSize()
        assert bufferSize == 1024

    def test_getCentroids(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        truth_centroids = (241.542, 346.931)
        centroids = dc.getCentroids(False)
        assert centroids == (None, None)
        dc.bufferModel.getCentroids = mocker.Mock(return_value=truth_centroids)
        centroids = dc.getCentroids(True)
        assert centroids == truth_centroids

    def test_getPsd(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        currentFps = 40
        psd = dc.getPsd(False, currentFps)
        assert psd == (None, None, None)
        dc.bufferModel.rollBuffer = True
        truth_psd = (np.random.random(3), np.random.random(3), np.random.random(3))
        dc.bufferModel.getPsd = mocker.Mock(return_value=truth_psd)
        psd = dc.getPsd(True, currentFps)
        dc.bufferModel.getPsd.assert_called_with(currentFps)
        assert psd == truth_psd

    def test_setBufferSize(self, qtbot):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        truthBufferSize = 256
        dc.setBufferSize(truthBufferSize)
        assert dc.getBufferSize() == truthBufferSize

    def test_setFrameChecks(self, qtbot):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        dc.setFrameChecks(passFrame, passFrame)
        assert dc.fullFrameModel.frameCheck is not None
        assert dc.roiFrameModel.frameCheck is not None

    def test_noneFrame(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        ffModel = mocker.patch.object(dc.fullFrameModel, "calculateCentroid")
        dc.passFrame(None, self.fullFrameStatus)
        assert ffModel.call_count == 0

    def test_getCentroidForUpdate(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        truthInfo = GenericFrameInformation(300.3, 400.2, 32042.42, 145.422, 70, None)
        dc.fullFrameModel.calculateCentroid = mocker.Mock(return_value=truthInfo)
        info = dc.getCentroidForUpdate(self.frame)
        assert info.centerX == truthInfo.centerX
        assert info.centerY == truthInfo.centerY

    def test_showRoiInformation(self, qtbot, mocker):
        cdw = CameraDataWidget()
        qtbot.addWidget(cdw)
        dc = DataController(cdw)
        currentFps = 40
        mockCameraDataWidgetUpdateRoiInfo = mocker.patch.object(cdw, 'updateRoiFrameData')
        dc.bufferModel.getInformation = mocker.Mock(return_value=RoiFrameInformation(242.5,
                                                                                     286.3,
                                                                                     2501.42,
                                                                                     104.753,
                                                                                     2.5432,
                                                                                     2.2353,
                                                                                     (1000, 25)))

        dc.showRoiInformation(True, currentFps)
        assert mockCameraDataWidgetUpdateRoiInfo.call_count == 1
        dc.showRoiInformation(False, currentFps)
        assert mockCameraDataWidgetUpdateRoiInfo.call_count == 1
