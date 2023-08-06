############################################################
# -*- coding: utf-8 -*-
#
# MOUNTCONTROL
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import sys
import logging
import socket
# external packages
import PyQt5.QtCore
import PyQt5.QtWidgets
import wakeonlan
# local imports
import mountcontrol.mount


__all__ = ['QtMount',
           ]


class WorkerSignals(PyQt5.QtCore.QObject):
    """
    The WorkerSignals class offers a list of signals to be used and instantiated by the
    Worker class to get signals for error, finished and result to be transferred to the
    caller back
    """

    __all__ = ['WorkerSignals']
    version = '0.1'

    finished = PyQt5.QtCore.pyqtSignal()
    error = PyQt5.QtCore.pyqtSignal(object)
    result = PyQt5.QtCore.pyqtSignal(object)


class Worker(PyQt5.QtCore.QRunnable):
    """
    The Worker class offers a generic interface to allow any function to be executed as a
    thread in an threadpool
    """

    __all__ = ['Worker',
               'run']
    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        # the worker signal must not be a class variable, but instance otherwise
        # we get trouble when having multiple threads running
        self.signals = WorkerSignals()

    def run(self):
        """
        runs an arbitrary methods with it's parameters and catches the result

        :return: nothing, but sends results and status as signals
        """

        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit(e)
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class MountSignals(PyQt5.QtCore.QObject):
    """
    The WorkerSignals class offers a list of signals to be used and instantiated by
    the Mount class to get signals for triggers for finished tasks to
    enable a gui to update their values transferred to the caller back.

    This has to be done in a separate class as the signals have to be subclassed from
    QObject and the Mount class itself is subclassed from object
    """

    __all__ = ['MountSignals']
    version = '0.1'

    pointDone = PyQt5.QtCore.pyqtSignal()
    settDone = PyQt5.QtCore.pyqtSignal()
    alignDone = PyQt5.QtCore.pyqtSignal()
    namesDone = PyQt5.QtCore.pyqtSignal()
    fwDone = PyQt5.QtCore.pyqtSignal()
    locationDone = PyQt5.QtCore.pyqtSignal()
    workaroundDone = PyQt5.QtCore.pyqtSignal()
    mountUp = PyQt5.QtCore.pyqtSignal(bool)
    mountClear = PyQt5.QtCore.pyqtSignal()


class Mount(mountcontrol.mount.Mount):
    """
    The Mount class is the main interface for interacting with the mount computer.
    The user could:
        setup / change the interface to the mount
        start / stop cyclic tasks to poll data from mount
        send and get data from mount
        has signals for interfacing to external GUI's for data updates

        >>> settings = Mount(
        >>>                     host=host,
        >>>                     MAC=MAC,
        >>>                     pathToTS=pathToTS,
        >>>                     expire=expire,
        >>>                     verbose=verbose,
        >>>                 )

    """

    CYCLE_POINTING = 500
    CYCLE_MOUNT_UP = 1000
    CYCLE_SETTING = 3000

    def __init__(self,
                 host=None,
                 MAC=None,
                 pathToTS=None,
                 expire=None,
                 verbose=None,
                 ):

        super().__init__(host=host,
                         MAC=MAC,
                         pathToTS=pathToTS,
                         expire=expire,
                         verbose=verbose,
                         )

        # signal handling
        self.signals = MountSignals()
        self.threadpool = PyQt5.QtCore.QThreadPool()
        self.mutexPointing = PyQt5.QtCore.QMutex()
        self.mutexSetting = PyQt5.QtCore.QMutex()
        self.mutexGetAlign = PyQt5.QtCore.QMutex()
        self.mutexGetNames = PyQt5.QtCore.QMutex()
        self.mutexGetFW = PyQt5.QtCore.QMutex()
        self.mutexGetLocation = PyQt5.QtCore.QMutex()
        self.mutexWorkaround = PyQt5.QtCore.QMutex()
        # timers
        self.timerPointing = PyQt5.QtCore.QTimer()
        self.timerPointing.setSingleShot(False)
        self.timerPointing.timeout.connect(self.cyclePointing)
        self.timerSetting = PyQt5.QtCore.QTimer()
        self.timerSetting.setSingleShot(False)
        self.timerSetting.timeout.connect(self.cycleSetting)
        self.timerMountUp = PyQt5.QtCore.QTimer()
        self.timerMountUp.setSingleShot(False)
        self.timerMountUp.timeout.connect(self.checkMountUp)

    def startTimers(self):
        """
        startTimers enables the cyclic timers for polling necessary mount data.

        :return: nothing
        """

        self.timerSetting.start(self.CYCLE_SETTING)
        self.timerPointing.start(self.CYCLE_POINTING)
        self.timerMountUp.start(self.CYCLE_MOUNT_UP)

    def stopTimers(self):
        """
        stopTimers disables the cyclic timers for polling necessary mount data.

        :return: nothing
        """

        self.timerPointing.stop()
        self.timerSetting.stop()
        self.timerMountUp.stop()

    def resetData(self):
        """
        resetData deletes all data already stored in classes just by redefining the
        classes. it send as well a signal, when the data is cleared.

        :return: nothing
        """

        super().resetData()
        self.signals.mountClear.emit()

    def checkMountUp(self):
        """
        checkMountUp polls the host/port of the mount computer and set the state and
        signals for the status accordingly.

        :return: nothing
        """

        client = socket.socket()
        client.settimeout(self.SOCKET_TIMEOUT)
        try:
            client.connect(self.host)
        except Exception:
            if self.mountUp:
                self.mountUp = False
                self.signals.mountUp.emit(False)
        else:
            if not self.mountUp:
                self.mountUp = True
                self.signals.mountUp.emit(True)
        finally:
            client.close()

    def clearCyclePointing(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexPointing.unlock()

    def cyclePointing(self):
        """
        cyclePointing prepares the worker thread and the signals for getting the pointing
        data.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexPointing.tryLock():
            self.logger.info('overrun in pointing')
            return
        worker = Worker(self.obsSite.pollPointing)
        worker.signals.result.connect(lambda: self.signals.pointDone.emit())
        worker.signals.finished.connect(self.clearCyclePointing)
        self.threadpool.start(worker)

    def clearCycleSetting(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexSetting.unlock()

    def cycleSetting(self):
        """
        cycleSet prepares the worker thread and the signals for getting the settings
        data.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexSetting.tryLock():
            self.logger.info('overrun in setting')
            return
        worker = Worker(self.sett.pollSetting)
        worker.signals.result.connect(lambda: self.signals.settDone.emit())
        worker.signals.finished.connect(self.clearCycleSetting)
        self.threadpool.start(worker)

    def clearGetAlign(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexGetAlign.unlock()

    def getAlign(self):
        """
        getAlign prepares the worker thread and the signals for getting the alignment model
        data.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexGetAlign.tryLock():
            self.logger.info('overrun in getAlign')
            return
        worker = Worker(self.model.pollStars)
        worker.signals.result.connect(lambda: self.signals.alignDone.emit())
        worker.signals.finished.connect(self.clearGetAlign)
        self.threadpool.start(worker)

    def clearGetNames(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexGetNames.unlock()

    def getNames(self):
        """
        getNames prepares the worker thread and the signals for getting the alignment model
        names.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexGetNames.tryLock():
            self.logger.info('overrun in getNames')
            return
        worker = Worker(self.model.pollNames)
        worker.signals.result.connect(lambda: self.signals.namesDone.emit())
        worker.signals.finished.connect(self.clearGetNames)
        self.threadpool.start(worker)

    def clearGetFW(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexGetFW.unlock()

    def getFW(self):
        """
        getFW prepares the worker thread and the signals for getting the build data of
        the mount computer.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexGetFW.tryLock():
            self.logger.info('overrun in getFW')
            return
        worker = Worker(self.fw.poll)
        worker.signals.result.connect(lambda: self.signals.fwDone.emit())
        worker.signals.finished.connect(self.clearGetFW)
        self.threadpool.start(worker)

    def clearGetLocation(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexGetLocation.unlock()

    def getLocation(self):
        """
        getLocation prepares the worker thread and the signals for getting the mount
        location data.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexGetLocation.tryLock():
            self.logger.info('overrun in getLocation')
            return
        worker = Worker(self.obsSite.getLocation)
        worker.signals.result.connect(lambda: self.signals.locationDone.emit())
        worker.signals.finished.connect(self.clearGetLocation)
        self.threadpool.start(worker)

    def clearWorkaround(self):
        """
        the cyclic or long lasting tasks for getting date from the mount should not run
        twice for the same data at the same time. so there is a mutex to prevent this
        behaviour. remove the mutex unlock this mutex.

        :return: nothing
        """

        self.mutexWorkaround.unlock()

    def workaround(self):
        """
        workaround prepares the worker thread and the signals for preparing the mount
        computer for processing the alignment model data.

        :return: nothing
        """

        if not self.mountUp:
            return
        if not self.mutexWorkaround.tryLock():
            self.logger.info('overrun in workaround')
            return
        worker = Worker(self.model.workaroundAlign)
        worker.signals.result.connect(lambda: self.signals.workaroundDone.emit())
        worker.signals.finished.connect(self.clearWorkaround)
        self.threadpool.start(worker)
