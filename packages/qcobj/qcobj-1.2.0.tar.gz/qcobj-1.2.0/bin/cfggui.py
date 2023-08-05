#!/usr/bin/env python
import sys
import os
import argparse
import signal

# Local imports
from qcobj.qtCompat import Qt, QtGui, QtWidgets, getOpenFileNames
from qcobj.cfggui import CfgGui

#==============================================================================
class MainWindow(QtWidgets.QMainWindow):
     def __init__(self, opts):
        super(MainWindow, self).__init__()
        self._options = opts
        if opts.configspec is None:
            # Get configspec pathname
            choice = getOpenFileNames(self,
                "Open configspec File", '.',
                "configspec (*.cfg)",
                options=QtWidgets.QFileDialog.DontUseNativeDialog)
            opts.configspec = choice[0][0]

        cfgGui = CfgGui(opts)
        self.setCentralWidget(cfgGui)

        openFile = QtWidgets.QAction("&Open...", self,
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open configuration file",
                triggered=cfgGui.openFile)

        saveFile = QtWidgets.QAction("&Save", self,
                shortcut=QtGui.QKeySequence.Save,
                statusTip="Save configuration to disk",
                triggered=cfgGui.saveFile)

        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        self.setAttribute(Qt.WA_DeleteOnClose)
        if self._options.cfg:
            cfgGui._loadQCobjs(self._options.cfg)
            self.setWindowTitle('%s: %s' % (self._options.cfg,
            [model.qcobj['description'] for model in cfgGui.models]))


#==============================================================================
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="\nEdit QConfigobj configuration files in a GUI.",
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog=os.path.basename(sys.argv[0]))

    parser.add_argument('-c', '--configspec',
        help=("ConfigSpec file. Configuration files will be validated "
            "against this file ")
        )
    parser.add_argument('cfg', default=None, nargs='*',
        help=("Configuration file. Configuration parameters will be loaded "
            "from this file ")
        )
    parser.add_argument('-s', '--strict', default=True,
        action='store_false',
        help=("Validate cfg against configspec ")
        )
    parser.add_argument('-n', '--noextra', default=True,
        action='store_false',
        help=("Forbid extra keywords / sections NOT in configspec files ")
        )
    options = parser.parse_args(sys.argv[1:])

    app = QtWidgets.QApplication(sys.argv)
    cfgGui = MainWindow(options)
    cfgGui.setGeometry(0, 0, 1000, 800)
    cfgGui.show()
    sys.exit(app.exec_())
