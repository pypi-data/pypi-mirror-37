# -*- coding: utf-8 -*-
""" The main initialization of our PySide/PyQt4/pyQt5 Package.

    Warning:
        This module tries to import PySide if available,
        otherwise defaults to PyQt4/PyQt5 for the GUI.
        To change this behaviour set *_TRY_PYSIDE* to False.


    :Author:
        - 2009-2011 Nicola Creati
        - 2009-2018 Roberto Vidmar

    :Copyright: 2011-2012
              Nicola Creati <ncreati@inogs.it>
              Roberto Vidmar <rvidmar@inogs.it>

    :License: MIT/X11 License (see :download:`license.txt
                               <../../license.txt>`)
"""

from __future__ import with_statement
from __future__ import division

_TRY_PYSIDE = True

try:
    if not _TRY_PYSIDE:
        raise ImportError()
    import PySide.QtCore as _QtCore
    import PySide.QtGui as _QtGui
    QtCore = _QtCore
    QtGui = _QtGui
    QtWidgets = _QtGui
    USES_PYSIDE = True
except ImportError:
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    try:
        import PyQt4.QtCore as _QtCore
        import PyQt4.QtGui as _QtGui
        import PyQt4.QtGui as _QtWidgets
    except ImportError:
        import PyQt5.QtCore as _QtCore
        import PyQt5.QtGui as _QtGui
        import PyQt5.QtWidgets as _QtWidgets
    QtCore = _QtCore
    QtGui = _QtGui
    QtWidgets = _QtWidgets
    USES_PYSIDE = False

def _pyside_import_module(moduleName):
    """ The import for PySide
    """
    pyside = __import__('PySide', globals(), locals(), [moduleName], -1)
    return getattr(pyside, moduleName)

def _pyqt4_import_module(moduleName):
    """ The import for PyQt4
    """
    pyside = __import__('PyQt4', globals(), locals(), [moduleName], -1)
    return getattr(pyside, moduleName)

if USES_PYSIDE:
    import_module = _pyside_import_module

    Signal = QtCore.Signal
    Slot = QtCore.Slot
    Property = QtCore.Property

    def getOpenFileName(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getOpenFileName
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(*args, **kargs)
        return pn

    def getOpenFileNames(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getOpenFileNames
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getOpenFileNames(*args, **kargs)
        return pn

    def getSaveFileName(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getSaveFileName
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(*args, **kargs)
        return pn
else:
    import_module = _pyqt4_import_module

    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    Property = QtCore.pyqtProperty

    def getOpenFileName(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getOpenFileName
        """
        return QtWidgets.QFileDialog.getOpenFileName(*args, **kargs)

    def getOpenFileNames(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getOpenFileNames
        """
        return QtWidgets.QFileDialog.getOpenFileNames(*args, **kargs)

    def getSaveFileName(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getSaveFileName
        """
        return QtWidgets.QFileDialog.getSaveFileName(*args, **kargs)

    QtCore.pyqtRemoveInputHook()

Qt = QtCore.Qt
