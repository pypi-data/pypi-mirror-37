.. :changelog:

History
-------

0.8.0 (2018-10-24)
~~~~~~~~~~~~~~~~~~

* Added 1D Power Spectrum Distribution plots
* Rearranged plots on UI
* Added color map to PSD Waterfall plots
* Change data widget to only update once per buffer fill
* Speed improvement work to obtain 150 FPS for Vimba camera

0.7.0 (2018-09-30)
~~~~~~~~~~~~~~~~~~

* Added configuration dialogs for plots and camera

0.6.0 (2018-09-14)
~~~~~~~~~~~~~~~~~~

* Support for Vimba interface cameras
* Added menu switching for multiple cameras
* Added CLI parser for profiling and future use

0.5.1 (2018-09-10)
~~~~~~~~~~~~~~~~~~

* Fix crash when using buffer size spinbox

0.5.0 (2018-09-03)
~~~~~~~~~~~~~~~~~~

* Adding spot oscillation to Gaussian camera
* Adding new controls to UI

  * ROI FPS
  * Buffer Size
  * Show Frames

* Centroid 1D plots disable auto range after start
* Make scatter and histogram plots update at same rate as PSD plots
* Locking out control buttons to stop unexpected behavior

0.4.0 (2018-07-29)
~~~~~~~~~~~~~~~~~~

* Create ROI frame processing
* Create and fill plots for ROI mode:

  * Rolling 1D centroid plots
  * 2D scatter plot with axis projections
  * Power spectrum distribution waterfall plots

* Push ROI data to camera status widget

0.3.0 (2018-07-12)
~~~~~~~~~~~~~~~~~~

* Create full frame processing
* Added camera status widget 

0.2.0 (2018-06-29)
~~~~~~~~~~~~~~~~~~

* Created Gaussian camera and controls
* Integrated camera CCD frame plot

0.1.2 (2018-05-30)
~~~~~~~~~~~~~~~~~~

* Switch to entry_points use exclusively

0.1.1 (2018-05-29)
~~~~~~~~~~~~~~~~~~

* Testing entry_points mechanism

0.1.0 (2018-05-24)
~~~~~~~~~~~~~~~~~~

* Creating basic application with no functionality
* Testing deployment
