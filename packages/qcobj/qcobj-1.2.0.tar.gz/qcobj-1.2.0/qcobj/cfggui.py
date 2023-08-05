# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import textwrap
import signal
from pint import DimensionalityError
from pint.errors import UndefinedUnitError
from datetime import datetime
from io import BytesIO
import itertools

# Local imports
from .qtCompat import Qt, Signal, QtCore, QtGui, QtWidgets, getOpenFileNames
from qcobj.qconfigobj import (QConfigObj, Certifier, ValidateError, Q_,
        eng_string, extract, isStringLike, splitPolygons)

ROOTNAME = 'General'
BOOL_COLOR = QtGui.QColor('green')
QUANTITY_COLOR = QtGui.QColor('red')
STR_COLOR = QtGui.QColor('blue')
qvalidator = Certifier()
EXPAND_ALL = 'Expand All'
COLLAPSE_ALL = 'Collapse All'
BACKGND_COLOR = QtGui.QColor('white')


#------------------------------------------------------------------------------
def split_list(L, n, stringify=True):
    """ Return a generator with the list `L` splitted in groups of `n`
        elements.
        If stringify evaluates as true, the groups of `n` elements
        are joined and terminated by \n
    """
    assert type(L) is list, "%s is not a list!" % L
    for i in range(0, len(L), n):
        if stringify:
            yield " ".join(L[i: i + n]) + "\n"
        else:
            yield L[i: i + n]

#------------------------------------------------------------------------------
def noBlanks(withblanks, wordsPerLine=2):
    """ Remove blanks and format with `wordsPerLine` words per line
    """
    return "".join(list(split_list(withblanks, wordsPerLine)))

#------------------------------------------------------------------------------
def deBlank(section, key, wordsPerLine=2):
    """ Remove blanks and format with `wordsPerLine` words per line
        every value with the key == 'polygon'
    """
    if key == 'polygon':
        section[key] = noBlanks(section[key].split(), wordsPerLine)

#------------------------------------------------------------------------------
def colorize(s, color):
    """ Return an HTML colorized string for `s`
    """
    color = color.lower()
    return "<font color=%s>%s</font>" % (color, s)

#------------------------------------------------------------------------------
def getPath(index):
    """ Return section path at `index`
    """
    # Build section path
    path = []
    parentIndex = index.parent()
    while parentIndex.isValid():
        secname = parentIndex.internalPointer().name()
        if secname != ROOTNAME:
            path.insert(0, secname)
        parentIndex = parentIndex.parent()
    return path

#------------------------------------------------------------------------------
def valueAtPath(cobj, path, name):
    """ Return cobj value at `path` or raise RuntimeError
    """
    if cobj is not None:
        section = cobj
        while path:
            try:
                section = section[path.pop(0)]
            except KeyError:
                return "__???__"
        if name == ROOTNAME:
            return section
        else:
            try:
                return section[name]
            except KeyError:
                return "__???__"

#==============================================================================
class TreeItem(QtCore.QObject):
    def __init__(self, name='', parent=None, data=None):
        self.parentItem = parent
        self.childItems = []
        self._name = name
        self._data = data

    def name(self):
        return self._name

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 3

    def data(self):
        return self._data

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def setData(self, value, validRange, column):
        """ Set node data with value converted to appropriate units as
            stated in validRange and return it or return None
        """
        qtype = validRange.partition('(')[0]
        if column == 1:
            if qtype.endswith('list'):
                try:
                    tmp = eval(value)
                except (NameError, TypeError) as e:
                    msgbox = QtWidgets.QMessageBox(
                            QtWidgets.QMessageBox.Warning,
                            "Validation Error!", str(e),
                            QtWidgets.QMessageBox.Ok)
                    msgbox.exec_()
                    return None
            elif qtype == 'quantity':
                # Quantity: get units
                if isinstance(self._data, (tuple, list)):
                    units = self._data[0].units
                else:
                    units = self._data.units
                # Make value a list
                values = [v.strip() for v in value.split(',')]
                tmp = ["%s %s" % (v, units) for v in values]
                # Validate all elements in list
                try:
                    valid = qvalidator.check(validRange, tmp)
                except (ValidateError, ValueError) as e:
                    msgbox = QtWidgets.QMessageBox(
                            QtWidgets.QMessageBox.Warning,
                            "Validation Error!", str(e),
                            QtWidgets.QMessageBox.Ok)
                    msgbox.exec_()
                    return None
                except UndefinedUnitError as e:
                    msgbox = QtWidgets.QMessageBox(
                            QtWidgets.QMessageBox.Warning,
                            "Undefned Unit Error!", str(e),
                            QtWidgets.QMessageBox.Ok)
                    msgbox.exec_()
                    return None
                self._data = valid
                return self._data
            else:
                # String, boolean, ...
                tmp = value
            try:
                valid = qvalidator.check(validRange, tmp)
            except (ValidateError, ValueError) as e:
                msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                        "Validation Error!", str(e), QtWidgets.QMessageBox.Ok)
                msgbox.exec_()
                return None
            else:
                self._data = valid
                return self._data
        elif column == 2:
            # Units
            # Only quantities have values in column 2
            if value:
                if isinstance(self._data, (tuple, list)):
                    data = self._data
                else:
                    data = (self._data, )
                newdata = ()
                for d in data:
                    try:
                        newq = d.to(value)
                    except DimensionalityError as e:
                        msgbox = QtWidgets.QMessageBox(
                                QtWidgets.QMessageBox.Warning,
                                "Dimensions disagree!", str(e),
                                QtWidgets.QMessageBox.Ok)
                        msgbox.exec_()
                        return None
                    except UndefinedUnitError as e:
                        msgbox = QtWidgets.QMessageBox(
                                QtWidgets.QMessageBox.Warning,
                                "Undefned Unit Error!", str(e),
                                QtWidgets.QMessageBox.Ok)
                        msgbox.exec_()
                        return None
                    else:
                        newdata += (newq, )
                if len(newdata) == 1:
                    self._data = newdata[0]
                else:
                    self._data = newdata
                return self._data
            return None
        else:
            return None

#==============================================================================
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent, qcobj=None):
        super(TreeModel, self).__init__()
        self._parent = parent
        self._header = ["Item", "Value", "Units"]
        self.rootItem = TreeItem(name='root', parent=None)
        self._loaded = False
        self.setupModelData(qcobj)
        self._compareQcobj = None

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        item = index.internalPointer()
        name = item.name()
        val = item.data()
        refval = valueAtPath(self._compareQcobj, getPath(index), name)
        if refval is None:
            # Only one Qcobj!
            refval = val

        # Units
        try:
            if isinstance(val, tuple):
                units = str(val[0].units)
            else:
                units = str(val.units)
        except AttributeError:
            units = None

        # Reference Units
        try:
            if isinstance(val, tuple):
                refunits = str(refval[0].units)
            else:
                refunits = str(refval.units)
        except AttributeError:
            refunits = None

        #########
        # Tooltip
        #########
        if role == Qt.ToolTipRole:
            return self.qcobj.comment(getPath(index), name)
        ##################
        # Foreground Color
        ##################
        elif role == Qt.ForegroundRole:
            try:
                if isinstance(val, tuple):
                    val[0].magnitude
                else:
                    val.magnitude
                if index.column() == 1:
                    if val == refval:
                        return QUANTITY_COLOR
                    else:
                        return BACKGND_COLOR
                elif index.column() == 2:
                    if units == refunits:
                        return QUANTITY_COLOR
                    else:
                        return BACKGND_COLOR
            except AttributeError:
                if isStringLike(val) and index.column() == 1:
                    if val == refval:
                        return STR_COLOR
                    else:
                        return BACKGND_COLOR
                elif isStringLike(val) and index.column() == 2:
                    if units == refunits:
                        return STR_COLOR
                    else:
                        return BACKGND_COLOR
                if (str(val) in "True False".split()
                        and index.column() in (1, 2)):
                    if val == refval:
                        return BOOL_COLOR
                    else:
                        return BACKGND_COLOR
                return None
        ##################
        # Background Color
        ##################
        elif role == Qt.BackgroundRole:
            try:
                if isinstance(val, tuple):
                    val[0].magnitude
                else:
                    val.magnitude
                if index.column() == 1:
                    if val == refval:
                        return BACKGND_COLOR
                    else:
                        return QUANTITY_COLOR
                elif index.column() == 2:
                    if units == refunits:
                        return BACKGND_COLOR
                    else:
                        return QUANTITY_COLOR
            except AttributeError:
                if isStringLike(val) and index.column() == 1:
                    if val == refval:
                        return BACKGND_COLOR
                    else:
                        return STR_COLOR
                elif isStringLike(val) and index.column() == 2:
                    if units == refunits:
                        return BACKGND_COLOR
                    else:
                        return STR_COLOR
                if (str(val) in "True False".split()
                        and index.column() == 1):
                    if val == refval:
                        return BACKGND_COLOR
                    else:
                        return BOOL_COLOR
                elif (str(val) in "True False".split()
                        and index.column() == 2):
                    if units == refunits:
                        return BACKGND_COLOR
                    else:
                        return BOOL_COLOR
                return None
            return None
        ###########
        # Display
        ###########
        elif role in (Qt.DisplayRole, ):
            if item.childCount() == 0:
                if index.column() == 0:
                    return name
                elif index.column() == 1:
                    # Value column
                    try:
                        if isinstance(val, tuple):
                            return ", ".join(
                                    [str(eng_string(v.magnitude, doround=6))
                                    for v in val])
                        else:
                            return str(eng_string(val.magnitude, doround=6))
                    except AttributeError:
                        return textwrap.dedent(str(val)).strip('\n')
                elif index.column() == 2:
                    # Units column
                    return units
            else:
                if index.column() == 0:
                    return name.title()
        #########
        # Edit
        #########
        elif role in (Qt.EditRole, ):
            if item.childCount() == 0:
                if index.column() == 0:
                    return name
                elif index.column() == 1:
                    # Value column
                    try:
                        if isinstance(val, tuple):
                            return ", ".join(
                                    [str(eng_string(v.magnitude, doround=6))
                                    for v in val])
                        else:
                            return str(eng_string(val.magnitude, doround=6))
                    except AttributeError:
                        return textwrap.dedent(str(val)).strip('\n')
                elif index.column() == 2:
                    # Units column
                    return units
            else:
                if index.column() == 0:
                    return name.title()

    def flags(self, index):
        """ Must be implemented
        """
        if not index.isValid():
            return Qt.NoItemFlags

        default = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == 0:
            return default
        else:
            return default | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[section]
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setComparison(self, qcobj):
        """ Set comparison qcobj for highlighting differences
        """
        self._compareQcobj = qcobj

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            path = getPath(index)
            key = index.internalPointer().name()
            validRange = self.qcobj.validRange(path, key)
            retval = index.internalPointer().setData(value, validRange,
                    index.column())
            if retval is not None:
                # Save value into qcobj
                section = self.qcobj
                for p in path:
                    section = section[p]
                section[key] = retval
                self.dataChanged.emit(index, index)
                self._parent.setFileChanged(self.qcobj.filename)
                return True
            else:
                return False
        else:
            print("Treemodel setData", args)
            return False

    def setupModelData(self, qcobj):
        """ Populate model with data from QCconfigObj instance
        """
        parent = self.rootItem
        self.qcobj = qcobj

        def fill(obj, parent):
            if parent != self.rootItem:
                for item in sorted(obj.scalars):
                    section = TreeItem(name=item, parent=parent,
                            data=obj[item])
                    parent.appendChild(section)
            for item in sorted(obj.sections):
                section = TreeItem(name=item, parent=parent, data=obj[item])
                parent.appendChild(section)
                if obj[item].sections is not None:
                    fill(obj[item], section)

        if self._loaded:
            # Make a new root item
            self.rootItem = TreeItem(name='root', parent=None)

        generalItem = TreeItem(name=ROOTNAME, parent=self.rootItem)
        self.rootItem.appendChild(generalItem)
        if qcobj:
            for item in sorted(qcobj.scalars):
                section = TreeItem(name=item, parent=generalItem,
                        data=qcobj[item])
                generalItem.appendChild(section)

            fill(qcobj, self.rootItem)
        self._loaded = True
        self.layoutChanged.emit()

#==============================================================================
class TreeView(QtWidgets.QTreeView):
    def __init__(self, *args):
        super(TreeView, self).__init__(*args)

    def resizeColumns(self):
        for column in range(self.model().columnCount(QtCore.QModelIndex())):
            self.resizeColumnToContents(column)


#==============================================================================
class QuantityDialog(QtWidgets.QDialog):
    def __init__(self, text, parent=None):
        super(QuantityDialog, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        #text = "".join(["<p>%s</p>" % line for line in text])
        #text = "<PRE>%s</PRE>" % text
        self._text = QtWidgets.QTextEdit("", self)
        #self._text.setAcceptRichText(True)
        self._text.setHtml(text)
        self._text.setFont(QtGui.QFont("Courier New", 11))
        self._text.setReadOnly(True)
        #self._bbox = QtWidgets.QDialogButtonBox()
        #self._bbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        #self._bbox.clicked.connect(self._onOk)
        layout.addWidget(self._text)
        #layout.addWidget(self._bbox)
        self.resize(600, 400)

    def _onOk(self, btn):
        self.close()

#==============================================================================
class CfgGui(QtWidgets.QWidget):
    def __init__(self, opts):
        super(CfgGui, self).__init__()
        # Avoid QtCore.QObject::startTimer: QTimer can only be used with
        # threads...
        QtWidgets.QFileSystemModel(self)
        self._options = opts
        self._configSpec = opts.configspec
        self._filesThatChanged = []

    def _loadQCobjs(self, pn):
        """ Load all QConfigObj instances form file(s) in pn
            Remove blanks in polygons and create the widgets for every
            instance.
        """
        if isinstance(pn, list):
            qcobjs = [QConfigObj(p, configspec=self._configSpec,
                    strict=self._options.strict,
                    noextra=self._options.noextra) for p in pn]
        else:
            qcobjs = [QConfigObj(pn, configspec=self._configSpec,
                strict=self._options.strict,
                noextra=self._options.noextra), ]

        # Remove blanks in polygons
        for q in qcobjs:
            q.walk(deBlank, call_on_sections=True, wordsPerLine=2)

        ntrees = len(qcobjs)
        self._trees = [TreeView(self) for i in range(ntrees)]
        self.models = [TreeModel(self) for i in range(ntrees)]
        allCfgLayout = QtWidgets.QHBoxLayout()
        self._filesThatChanged = []

        i = 0
        for tree, model, qcobj in zip(self._trees, self.models, qcobjs):
            tree.setModel(model)
            model.dataChanged.connect(tree.resizeColumns)
            model.setupModelData(qcobj)
            if i:
                model.setComparison(qcobjs[i -1])
            else:
                pass

            # The Buttons
            btnsWidget = QtWidgets.QWidget(self)
            hbl = QtWidgets.QHBoxLayout()
            expandBtn = QtWidgets.QPushButton(EXPAND_ALL, btnsWidget)
            expandBtn.setEnabled(True)
            expandBtn.clicked.connect(self.toggleExpand)
            expandBtn.tree = tree
            hbl.addWidget(expandBtn)
            btnsWidget.setLayout(hbl)

            singleCfgWidget = QtWidgets.QWidget(self)
            singleCfgLayout = QtWidgets.QVBoxLayout()
            singleCfgLayout.addWidget(btnsWidget)
            singleCfgLayout.addWidget(tree)
            singleCfgWidget.setLayout(singleCfgLayout)
            tree.resizeColumns()

            allCfgLayout.addWidget(singleCfgWidget)
            i += 1

        vlo = QtWidgets.QVBoxLayout(self)
        if len(qcobjs) > 1:
            self._scrollLock = QtWidgets.QCheckBox("Lock scrollbars")
            self._scrollLock.stateChanged.connect(self._onScroll)
            vlo.addWidget(self._scrollLock)
        vlo.addLayout(allCfgLayout)

    def _onScroll(self, value):
        if value:
            # Connect all scrollbars together
            for t1, t2 in itertools.permutations(self._trees, 2):
                t1.verticalScrollBar().valueChanged.connect(
                        t2.verticalScrollBar().setValue)
        else:
            # Disconnect all scrollbars
            for t1, t2 in itertools.permutations(self._trees, 2):
                t1.verticalScrollBar().valueChanged.disconnect(
                        t2.verticalScrollBar().setValue)

    def _quantityChanged(self, index):
        if index < 0:
            return
        sender = self.sender()
        quant = sender.itemText(index)
        html = self.makeHtml(quant)
        q = QuantityDialog(html, self)
        q.exec_()

    def setFileChanged(self, filename):
        if filename not in self._filesThatChanged:
            self._filesThatChanged.append(filename)

    def closeEvent(self, event):
        # Changes?
        if self._filesThatChanged:
            self.saveFile()
        event.accept() # let the window close

    def openFile(self):
        pn = getOpenFileNames(self,
                "Open Configuration File", '.',
                "Configuration (*.cfg)",
                options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if pn:
            self._loadQCobjs(pn[0])

    def saveFile(self):
        for pn in self._filesThatChanged:
            extensions = "CFG (*.cfg)"
            dlg = QtWidgets.QFileDialog(self, "Save configuration", pn)
            dlg.setNameFilter(extensions)
            dlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
            dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            if dlg.exec_():
                newpn = dlg.selectedFiles()[0]
                if newpn:
                    # Search for the model with pn filename
                    for model in self.models:
                        if model.qcobj.filename == pn:
                            break
                    cfg = model.qcobj.write_to_string()
                    now = datetime.now().strftime("%Y%m%d% at %H:%M:%S")
                    with open(newpn, "wb") as theFile:
                        timestamp = ("# Created by %s at %s\n\n"
                                % (__file__, now))
                        theFile.write(timestamp.encode("utf-8"))
                        theFile.write(cfg)
                    theFile.close()

    def toggleExpand(self, *args):
        senderBtn = self.sender()
        if senderBtn.text() == EXPAND_ALL:
            senderBtn.tree.expandAll()
            senderBtn.tree.resizeColumns()
            senderBtn.setText(COLLAPSE_ALL)
        else:
            senderBtn.tree.collapseAll()
            senderBtn.tree.resizeColumns()
            senderBtn.setText(EXPAND_ALL)
