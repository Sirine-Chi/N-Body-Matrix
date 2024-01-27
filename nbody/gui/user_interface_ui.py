# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_interface.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QKeySequenceEdit,
    QLabel, QListView, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QSizePolicy, QStatusBar,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_NBodySimulations(object):
    def setupUi(self, NBodySimulations):
        if not NBodySimulations.objectName():
            NBodySimulations.setObjectName(u"NBodySimulations")
        NBodySimulations.resize(829, 596)
        self.actionAbout_Simulator = QAction(NBodySimulations)
        self.actionAbout_Simulator.setObjectName(u"actionAbout_Simulator")
        self.actionSettings = QAction(NBodySimulations)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionQuit_Simulations = QAction(NBodySimulations)
        self.actionQuit_Simulations.setObjectName(u"actionQuit_Simulations")
        self.actionOPen = QAction(NBodySimulations)
        self.actionOPen.setObjectName(u"actionOPen")
        self.centralwidget = QWidget(NBodySimulations)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(33, 13, 44);\n"
"font-family: 12pt \"Menlo\";")
        self.outputwidget = QWidget(self.centralwidget)
        self.outputwidget.setObjectName(u"outputwidget")
        self.outputwidget.setGeometry(QRect(460, 10, 331, 411))
        self.outputwidget.setStyleSheet(u"background-color: rgba(85, 86, 86, 30);\n"
"border: 1px solid rgba(100, 100, 100, 50);\n"
"border-radius: 8px;")
        self.widget = QWidget(self.outputwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(7, 10, 321, 401))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.openGLWidget = QOpenGLWidget(self.widget)
        self.openGLWidget.setObjectName(u"openGLWidget")
        self.openGLWidget.setMinimumSize(QSize(0, 200))

        self.verticalLayout.addWidget(self.openGLWidget)

        self.widget1 = QWidget(self.widget)
        self.widget1.setObjectName(u"widget1")
        self.horizontalLayout_5 = QHBoxLayout(self.widget1)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.widget1)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: rgb(176, 178, 178);")

        self.horizontalLayout_5.addWidget(self.label)

        self.progressBar = QProgressBar(self.widget1)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMouseTracking(False)
        self.progressBar.setTabletTracking(False)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setValue(24)

        self.horizontalLayout_5.addWidget(self.progressBar)


        self.verticalLayout.addWidget(self.widget1)

        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.keySequenceEdit = QKeySequenceEdit(self.widget)
        self.keySequenceEdit.setObjectName(u"keySequenceEdit")

        self.verticalLayout.addWidget(self.keySequenceEdit)

        self.inputwidget = QWidget(self.centralwidget)
        self.inputwidget.setObjectName(u"inputwidget")
        self.inputwidget.setGeometry(QRect(20, 10, 421, 411))
        self.inputwidget.setStyleSheet(u"background-color: rgba(85, 86, 86, 30);\n"
"border: 1px solid rgba(100, 100, 100, 50);\n"
"border-radius: 8px;")
        self.horizontalFrame = QFrame(self.inputwidget)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        self.horizontalFrame.setGeometry(QRect(10, 10, 411, 401))
        self.horizontalFrame.setMouseTracking(False)
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.textBrowser_2 = QTextBrowser(self.horizontalFrame)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.horizontalLayout_2.addWidget(self.textBrowser_2)

        self.listView = QListView(self.horizontalFrame)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout_2.addWidget(self.listView)

        NBodySimulations.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(NBodySimulations)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 829, 24))
        self.menuSimulator = QMenu(self.menubar)
        self.menuSimulator.setObjectName(u"menuSimulator")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        NBodySimulations.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(NBodySimulations)
        self.statusbar.setObjectName(u"statusbar")
        NBodySimulations.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSimulator.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuSimulator.addAction(self.actionAbout_Simulator)
        self.menuSimulator.addAction(self.actionSettings)
        self.menuSimulator.addAction(self.actionQuit_Simulations)
        self.menuFile.addAction(self.actionOPen)

        self.retranslateUi(NBodySimulations)

        QMetaObject.connectSlotsByName(NBodySimulations)
    # setupUi

    def retranslateUi(self, NBodySimulations):
        NBodySimulations.setWindowTitle(QCoreApplication.translate("NBodySimulations", u"MainWindow", None))
        self.actionAbout_Simulator.setText(QCoreApplication.translate("NBodySimulations", u"About N Body Simulations", None))
        self.actionSettings.setText(QCoreApplication.translate("NBodySimulations", u"Settings", None))
        self.actionQuit_Simulations.setText(QCoreApplication.translate("NBodySimulations", u"Quit Simulations", None))
        self.actionOPen.setText(QCoreApplication.translate("NBodySimulations", u"Open", None))
        self.label.setText(QCoreApplication.translate("NBodySimulations", u"Progress", None))
        self.menuSimulator.setTitle(QCoreApplication.translate("NBodySimulations", u"Simulations", None))
        self.menuFile.setTitle(QCoreApplication.translate("NBodySimulations", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("NBodySimulations", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("NBodySimulations", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("NBodySimulations", u"Help", None))
    # retranslateUi

