# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_new_str.ui'
#
# Created: Tue Jun 24 16:33:54 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frmNewSTR(object):
    def setupUi(self, frmNewSTR):
        frmNewSTR.setObjectName(_fromUtf8("frmNewSTR"))
        frmNewSTR.resize(663, 572)
        frmNewSTR.setWizardStyle(QtGui.QWizard.ModernStyle)
        frmNewSTR.setOptions(QtGui.QWizard.HelpButtonOnRight)
        self.frmWizAbout = QtGui.QWizardPage()
        self.frmWizAbout.setObjectName(_fromUtf8("frmWizAbout"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frmWizAbout)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.frmWizAbout)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        frmNewSTR.addPage(self.frmWizAbout)
        self.frmWizPerson = QtGui.QWizardPage()
        self.frmWizPerson.setObjectName(_fromUtf8("frmWizPerson"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frmWizPerson)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.vlPersonNotif = QtGui.QVBoxLayout()
        self.vlPersonNotif.setObjectName(_fromUtf8("vlPersonNotif"))
        self.verticalLayout_2.addLayout(self.vlPersonNotif)
        self.groupBox = QtGui.QGroupBox(self.frmWizPerson)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtFilterPattern = QtGui.QLineEdit(self.groupBox)
        self.txtFilterPattern.setMinimumSize(QtCore.QSize(0, 30))
        self.txtFilterPattern.setMaxLength(100)
        self.txtFilterPattern.setObjectName(_fromUtf8("txtFilterPattern"))
        self.horizontalLayout.addWidget(self.txtFilterPattern)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.cboPersonFilterCols = QtGui.QComboBox(self.groupBox)
        self.cboPersonFilterCols.setMinimumSize(QtCore.QSize(200, 30))
        self.cboPersonFilterCols.setObjectName(_fromUtf8("cboPersonFilterCols"))
        self.horizontalLayout.addWidget(self.cboPersonFilterCols)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tvPersonInfo = QtGui.QTreeWidget(self.frmWizPerson)
        self.tvPersonInfo.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tvPersonInfo.setAlternatingRowColors(True)
        self.tvPersonInfo.setObjectName(_fromUtf8("tvPersonInfo"))
        self.tvPersonInfo.headerItem().setText(0, _fromUtf8("1"))
        self.tvPersonInfo.header().setVisible(False)
        self.verticalLayout_2.addWidget(self.tvPersonInfo)
        frmNewSTR.addPage(self.frmWizPerson)
        self.frmWizProperty = QtGui.QWizardPage()
        self.frmWizProperty.setObjectName(_fromUtf8("frmWizProperty"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frmWizProperty)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tvPropInfo = QtGui.QTreeWidget(self.frmWizProperty)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tvPropInfo.sizePolicy().hasHeightForWidth())
        self.tvPropInfo.setSizePolicy(sizePolicy)
        self.tvPropInfo.setMinimumSize(QtCore.QSize(220, 0))
        self.tvPropInfo.setMaximumSize(QtCore.QSize(220, 16777215))
        self.tvPropInfo.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tvPropInfo.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tvPropInfo.setAlternatingRowColors(True)
        self.tvPropInfo.setObjectName(_fromUtf8("tvPropInfo"))
        self.tvPropInfo.headerItem().setText(0, _fromUtf8("1"))
        self.tvPropInfo.header().setVisible(False)
        self.tvPropInfo.header().setStretchLastSection(False)
        self.gridLayout_4.addWidget(self.tvPropInfo, 2, 0, 1, 1)
        self.vlPropNotif = QtGui.QVBoxLayout()
        self.vlPropNotif.setObjectName(_fromUtf8("vlPropNotif"))
        self.gridLayout_4.addLayout(self.vlPropNotif, 0, 0, 1, 2)
        self.txtPropID = QtGui.QLineEdit(self.frmWizProperty)
        self.txtPropID.setMinimumSize(QtCore.QSize(0, 30))
        self.txtPropID.setMaxLength(50)
        self.txtPropID.setObjectName(_fromUtf8("txtPropID"))
        self.gridLayout_4.addWidget(self.txtPropID, 1, 0, 1, 1)
        self.gpOpenLayers = QtGui.QGroupBox(self.frmWizProperty)
        self.gpOpenLayers.setCheckable(True)
        self.gpOpenLayers.setChecked(False)
        self.gpOpenLayers.setObjectName(_fromUtf8("gpOpenLayers"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gpOpenLayers)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.propWebView = QtWebKit.QWebView(self.gpOpenLayers)
        self.propWebView.setStyleSheet(_fromUtf8(""))
        self.propWebView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.propWebView.setObjectName(_fromUtf8("propWebView"))
        self.gridLayout_3.addWidget(self.propWebView, 0, 0, 1, 4)
        self.groupBox_2 = QtGui.QGroupBox(self.gpOpenLayers)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.rbGMaps = QtGui.QRadioButton(self.groupBox_2)
        self.rbGMaps.setChecked(True)
        self.rbGMaps.setObjectName(_fromUtf8("rbGMaps"))
        self.gridLayout_5.addWidget(self.rbGMaps, 0, 0, 1, 1)
        self.rbOSM = QtGui.QRadioButton(self.groupBox_2)
        self.rbOSM.setObjectName(_fromUtf8("rbOSM"))
        self.gridLayout_5.addWidget(self.rbOSM, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 4)
        self.zoomSlider = QtGui.QSlider(self.gpOpenLayers)
        self.zoomSlider.setMinimum(2)
        self.zoomSlider.setMaximum(20)
        self.zoomSlider.setProperty("value", 12)
        self.zoomSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.zoomSlider.setTickInterval(2)
        self.zoomSlider.setObjectName(_fromUtf8("zoomSlider"))
        self.gridLayout_3.addWidget(self.zoomSlider, 2, 0, 1, 3)
        self.btnResetMap = QtGui.QPushButton(self.gpOpenLayers)
        self.btnResetMap.setObjectName(_fromUtf8("btnResetMap"))
        self.gridLayout_3.addWidget(self.btnResetMap, 2, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.gpOpenLayers)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.gpOpenLayers)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 3, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.gpOpenLayers)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 3, 2, 1, 1)
        self.gridLayout_4.addWidget(self.gpOpenLayers, 1, 1, 2, 1)
        frmNewSTR.addPage(self.frmWizProperty)
        self.frmWizSTRType = QtGui.QWizardPage()
        self.frmWizSTRType.setToolTip(_fromUtf8(""))
        self.frmWizSTRType.setObjectName(_fromUtf8("frmWizSTRType"))
        self.gridLayout_11 = QtGui.QGridLayout(self.frmWizSTRType)
        self.gridLayout_11.setContentsMargins(-1, -1, -1, 15)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.vlSTRTypeNotif = QtGui.QVBoxLayout()
        self.vlSTRTypeNotif.setObjectName(_fromUtf8("vlSTRTypeNotif"))
        self.gridLayout_11.addLayout(self.vlSTRTypeNotif, 0, 0, 1, 2)
        self.label_15 = QtGui.QLabel(self.frmWizSTRType)
        self.label_15.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_11.addWidget(self.label_15, 1, 0, 1, 1)
        self.cboSTRType = QtGui.QComboBox(self.frmWizSTRType)
        self.cboSTRType.setMinimumSize(QtCore.QSize(0, 30))
        self.cboSTRType.setObjectName(_fromUtf8("cboSTRType"))
        self.gridLayout_11.addWidget(self.cboSTRType, 1, 1, 1, 1)
        self.chkSTRAgreement = QtGui.QCheckBox(self.frmWizSTRType)
        self.chkSTRAgreement.setObjectName(_fromUtf8("chkSTRAgreement"))
        self.gridLayout_11.addWidget(self.chkSTRAgreement, 2, 1, 1, 1)
        frmNewSTR.addPage(self.frmWizSTRType)
        self.frmWizSourceDocs = QtGui.QWizardPage()
        self.frmWizSourceDocs.setObjectName(_fromUtf8("frmWizSourceDocs"))
        self.gridLayout_6 = QtGui.QGridLayout(self.frmWizSourceDocs)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.groupBox_3 = QtGui.QGroupBox(self.frmWizSourceDocs)
        self.groupBox_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnAddTitleDeed = QtGui.QPushButton(self.groupBox_3)
        self.btnAddTitleDeed.setMinimumSize(QtCore.QSize(0, 30))
        self.btnAddTitleDeed.setMaximumSize(QtCore.QSize(200, 32))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/attachment.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddTitleDeed.setIcon(icon)
        self.btnAddTitleDeed.setObjectName(_fromUtf8("btnAddTitleDeed"))
        self.gridLayout.addWidget(self.btnAddTitleDeed, 0, 0, 1, 1)
        self.stkSrcDocList = QtGui.QStackedWidget(self.groupBox_3)
        self.stkSrcDocList.setObjectName(_fromUtf8("stkSrcDocList"))
        self.pgPrivate = QtGui.QWidget()
        self.pgPrivate.setObjectName(_fromUtf8("pgPrivate"))
        self.gridLayout_2 = QtGui.QGridLayout(self.pgPrivate)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scrollArea = QtGui.QScrollArea(self.pgPrivate)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 587, 361))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.groupBox_4 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setGeometry(QtCore.QRect(9, 9, 561, 351))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.vlDocTitleDeed = QtGui.QVBoxLayout()
        self.vlDocTitleDeed.setObjectName(_fromUtf8("vlDocTitleDeed"))
        self.gridLayout_7.addLayout(self.vlDocTitleDeed, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.stkSrcDocList.addWidget(self.pgPrivate)
        self.pgStateland = QtGui.QWidget()
        self.pgStateland.setObjectName(_fromUtf8("pgStateland"))
        self.gridLayout_10 = QtGui.QGridLayout(self.pgStateland)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.groupBox_8 = QtGui.QGroupBox(self.pgStateland)
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBox_8)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.txtStateReceiptAmount = QtGui.QLineEdit(self.groupBox_8)
        self.txtStateReceiptAmount.setMinimumSize(QtCore.QSize(0, 30))
        self.txtStateReceiptAmount.setMaxLength(200)
        self.txtStateReceiptAmount.setObjectName(_fromUtf8("txtStateReceiptAmount"))
        self.gridLayout_9.addWidget(self.txtStateReceiptAmount, 1, 1, 1, 1)
        self.txtStateTaxOffice = QtGui.QLineEdit(self.groupBox_8)
        self.txtStateTaxOffice.setMinimumSize(QtCore.QSize(0, 30))
        self.txtStateTaxOffice.setMaxLength(100)
        self.txtStateTaxOffice.setObjectName(_fromUtf8("txtStateTaxOffice"))
        self.gridLayout_9.addWidget(self.txtStateTaxOffice, 3, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_8)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_9.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_8)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_9.addWidget(self.label_13, 2, 0, 1, 1)
        self.dtStateReceiptDate = QtGui.QDateEdit(self.groupBox_8)
        self.dtStateReceiptDate.setMinimumSize(QtCore.QSize(0, 30))
        self.dtStateReceiptDate.setCalendarPopup(True)
        self.dtStateReceiptDate.setObjectName(_fromUtf8("dtStateReceiptDate"))
        self.gridLayout_9.addWidget(self.dtStateReceiptDate, 0, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox_8)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_9.addWidget(self.label_14, 3, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_8)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_9.addWidget(self.label_12, 1, 0, 1, 1)
        self.dtStateLeaseYear = QtGui.QDateEdit(self.groupBox_8)
        self.dtStateLeaseYear.setMinimumSize(QtCore.QSize(0, 30))
        self.dtStateLeaseYear.setCalendarPopup(False)
        self.dtStateLeaseYear.setObjectName(_fromUtf8("dtStateLeaseYear"))
        self.gridLayout_9.addWidget(self.dtStateLeaseYear, 2, 1, 1, 1)
        self.btnPublicReceiptScan = QtGui.QPushButton(self.groupBox_8)
        self.btnPublicReceiptScan.setMinimumSize(QtCore.QSize(0, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/receipt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPublicReceiptScan.setIcon(icon1)
        self.btnPublicReceiptScan.setObjectName(_fromUtf8("btnPublicReceiptScan"))
        self.gridLayout_9.addWidget(self.btnPublicReceiptScan, 4, 1, 1, 1)
        self.vlStateScanReceipt = QtGui.QVBoxLayout()
        self.vlStateScanReceipt.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.vlStateScanReceipt.setObjectName(_fromUtf8("vlStateScanReceipt"))
        self.gridLayout_9.addLayout(self.vlStateScanReceipt, 5, 1, 1, 1)
        self.gridLayout_10.addWidget(self.groupBox_8, 0, 0, 1, 1)
        self.stkSrcDocList.addWidget(self.pgStateland)
        self.gridLayout.addWidget(self.stkSrcDocList, 1, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.vlSourceDocNotif = QtGui.QVBoxLayout()
        self.vlSourceDocNotif.setObjectName(_fromUtf8("vlSourceDocNotif"))
        self.gridLayout_6.addLayout(self.vlSourceDocNotif, 0, 0, 1, 1)
        frmNewSTR.addPage(self.frmWizSourceDocs)
        self.frmSTRSummary = QtGui.QWizardPage()
        self.frmSTRSummary.setObjectName(_fromUtf8("frmSTRSummary"))
        self.gridLayout_14 = QtGui.QGridLayout(self.frmSTRSummary)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.twSTRSummary = QtGui.QTreeWidget(self.frmSTRSummary)
        self.twSTRSummary.setFrameShadow(QtGui.QFrame.Sunken)
        self.twSTRSummary.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.twSTRSummary.setObjectName(_fromUtf8("twSTRSummary"))
        self.twSTRSummary.headerItem().setText(0, _fromUtf8("1"))
        self.twSTRSummary.header().setVisible(False)
        self.gridLayout_14.addWidget(self.twSTRSummary, 1, 0, 1, 1)
        self.label_18 = QtGui.QLabel(self.frmSTRSummary)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_14.addWidget(self.label_18, 0, 0, 1, 1)
        frmNewSTR.addPage(self.frmSTRSummary)

        self.retranslateUi(frmNewSTR)
        QtCore.QMetaObject.connectSlotsByName(frmNewSTR)
        frmNewSTR.setTabOrder(self.cboPersonFilterCols, self.tvPersonInfo)
        frmNewSTR.setTabOrder(self.tvPersonInfo, self.txtFilterPattern)
        frmNewSTR.setTabOrder(self.txtFilterPattern, self.txtPropID)
        frmNewSTR.setTabOrder(self.txtPropID, self.tvPropInfo)

    def retranslateUi(self, frmNewSTR):
        frmNewSTR.setWindowTitle(_translate("frmNewSTR", "New Social Tenure Relationship", None))
        self.frmWizAbout.setTitle(_translate("frmNewSTR", "About", None))
        self.frmWizAbout.setSubTitle(_translate("frmNewSTR", "General information about Social Tenure Relationship (STR).", None))
        self.label.setText(_translate("frmNewSTR", "<html><head/><body><p>Scoial Tenure Relationship refers to the right or \'relationship\' between persons and properties (which as represented as polygons on the map). It also includes conflict information associated with a given property.</p><p>This module provides a mechanism for defining STR applicable to property - both land and building</p><p>Click on the \'Next\' button below to proceed.</p></body></html>", None))
        self.frmWizPerson.setTitle(_translate("frmNewSTR", "Occupant Information", None))
        self.frmWizPerson.setSubTitle(_translate("frmNewSTR", "Select the occupant information by searching through the existing repository.", None))
        self.groupBox.setTitle(_translate("frmNewSTR", "Search Criteria:", None))
        self.txtFilterPattern.setPlaceholderText(_translate("frmNewSTR", "Look for", None))
        self.label_2.setText(_translate("frmNewSTR", "in column:", None))
        self.frmWizProperty.setTitle(_translate("frmNewSTR", "Property information", None))
        self.frmWizProperty.setSubTitle(_translate("frmNewSTR", "Select the land and building information.", None))
        self.txtPropID.setPlaceholderText(_translate("frmNewSTR", "Enter the unique property ID", None))
        self.gpOpenLayers.setTitle(_translate("frmNewSTR", "Preview Property:", None))
        self.groupBox_2.setTitle(_translate("frmNewSTR", "Choose Base Layer", None))
        self.rbGMaps.setText(_translate("frmNewSTR", "Google Maps", None))
        self.rbOSM.setText(_translate("frmNewSTR", "Open Street Maps", None))
        self.btnResetMap.setText(_translate("frmNewSTR", "Reset Map", None))
        self.label_8.setText(_translate("frmNewSTR", "-", None))
        self.label_7.setText(_translate("frmNewSTR", "Zoom", None))
        self.label_9.setText(_translate("frmNewSTR", "+", None))
        self.frmWizSTRType.setTitle(_translate("frmNewSTR", "Social Tenure Relationship (STR) Type", None))
        self.frmWizSTRType.setSubTitle(_translate("frmNewSTR", "Select the type pf relationship that the specified person has with the selected property.", None))
        self.label_15.setText(_translate("frmNewSTR", "STR Type", None))
        self.chkSTRAgreement.setText(_translate("frmNewSTR", "A written agreement is available", None))
        self.frmWizSourceDocs.setTitle(_translate("frmNewSTR", "Source Documents", None))
        self.frmWizSourceDocs.setSubTitle(_translate("frmNewSTR", "Upload one or more documents.", None))
        self.groupBox_3.setTitle(_translate("frmNewSTR", "Supporting Documents", None))
        self.btnAddTitleDeed.setText(_translate("frmNewSTR", "Add Supporting Document", None))
        self.groupBox_8.setTitle(_translate("frmNewSTR", "Tax Information:", None))
        self.label_6.setText(_translate("frmNewSTR", "Date of Latest Receipt", None))
        self.label_13.setText(_translate("frmNewSTR", "Start of Leasing Year", None))
        self.dtStateReceiptDate.setDisplayFormat(_translate("frmNewSTR", "dd/MM/yyyy", None))
        self.label_14.setText(_translate("frmNewSTR", "Tax Office", None))
        self.label_12.setText(_translate("frmNewSTR", "Amount of Last Receipt", None))
        self.dtStateLeaseYear.setDisplayFormat(_translate("frmNewSTR", "yyyy", None))
        self.btnPublicReceiptScan.setText(_translate("frmNewSTR", "Add Receipt Scan", None))
        self.frmSTRSummary.setTitle(_translate("frmNewSTR", "STR Definition Summary", None))
        self.frmSTRSummary.setSubTitle(_translate("frmNewSTR", "A new social tenure relationship will be created based on the information that you have supplied, as summarized below.", None))
        self.label_18.setText(_translate("frmNewSTR", "If you want to review or change any selections, click Back. If you are satisified with the selections, click Finish.", None))

from PyQt4 import QtWebKit
import resources_rc
