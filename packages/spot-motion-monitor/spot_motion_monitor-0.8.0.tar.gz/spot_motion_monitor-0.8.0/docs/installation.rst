============
Installation
============

At the command line either via easy_install or pip::

    $ easy_install spot_motion_monitor
    $ pip install spot_motion_monitor

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv spot_motion_monitor
    $ pip install spot_motion_monitor

Once you have installed the package, the provided Gaussian camera provides 
a nice way to explore the interface. However, it was designed for use with a
real camera system. The one supported by this interface is the 
`Allied Vision Technologies <https://www.alliedvision.com/en/digital-industrial-camera-solutions.html>`_ Prosilica GigE cameras. This requires the ``pymba`` package which
can be found `here <https://github.com/morefigs/pymba>`_. Follow the
installation instructions there. For clarity, the installation of ``pymba``
requires a clone of the repository.
