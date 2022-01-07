from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QListView, QAbstractItemView, QListWidgetItem

from ui.tails import TimeStatus, NetworkSpeedStatus, XGAMESButton

class QCustomListWidget(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self)
        self.parent = parent
        # Customize SizePolicy
        self.setMinimumHeight(150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                 QSizePolicy.Policy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setSpacing(10)
        #self.setSizeAdjustPolicy(QSizePolicy)
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        # set frameless
        self.setFrameShape(0)
        #
        self.setStyleSheet("QListView::item{\n"
                                           "    font: 12pt \"Segoe UI\";\n"
                                           "    color: rgb(255, 255, 255);\n"
                                           "    /*padding:5px;*/\n"
                                           "    border:none;\n"
                                           "    border-radius: 10px;\n"
                                           "}\n"
                                           "QListWidget{\n"
                                           "    color: rgb(255, 255, 255);\n"
                                           "}\n"
                                           "QAbstractScrollArea\n"
                                           "{\n"
                                           "    border-radius: 2px;\n"
                                           "    /*border: 1px solid #76797C;*/\n"
                                           "    background-color: transparent;\n"
                                           "    color: white;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar:horizontal\n"
                                           "{\n"
                                           "    height: 15px;\n"
                                           "    margin: 3px 15px 3px 15px;\n"
                                           "    border: 1px transparent #2A2929;\n"
                                           "    border-radius: 4px;\n"
                                           "    background-color: #2A2929;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::handle:horizontal\n"
                                           "{\n"
                                           "    background-color: #605F5F;\n"
                                           "    min-width: 5px;\n"
                                           "    border-radius: 4px;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-line:horizontal\n"
                                           "{\n"
                                           "    margin: 0px 3px 0px 3px;\n"
                                           "    border-image: url(:/qss_icons/rc/right_arrow_disabled.png);\n"
                                           "    width: 10px;\n"
                                           "    height: 10px;\n"
                                           "    subcontrol-position: right;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-line:horizontal\n"
                                           "{\n"
                                           "    margin: 0px 3px 0px 3px;\n"
                                           "    border-image: url(:/qss_icons/rc/left_arrow_disabled.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: left;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on\n"
                                           "{\n"
                                           "    border-image: url(:/qss_icons/rc/right_arrow.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: right;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on\n"
                                           "{\n"
                                           "    border-image: url(:/qss_icons/rc/left_arrow.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: left;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
                                           "{\n"
                                           "    background: none;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
                                           "{\n"
                                           "    background: none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar:vertical\n"
                                           "{\n"
                                           "    background-color: #2A2929;\n"
                                           "    width: 15px;\n"
                                           "    margin: 15px 3px 15px 3px;\n"
                                           "    border: 1px transparent #2A2929;\n"
                                           "    border-radius: 4px;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::handle:vertical\n"
                                           "{\n"
                                           "    background-color: #605F5F;\n"
                                           "    min-height: 5px;\n"
                                           "    border-radius: 4px;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-line:vertical\n"
                                           "{\n"
                                           "    margin: 3px 0px 3px 0px;\n"
                                           "    border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: top;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-line:vertical\n"
                                           "{\n"
                                           "    margin: 3px 0px 3px 0px;\n"
                                           "    border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: bottom;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on\n"
                                           "{\n"
                                           "\n"
                                           "    border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: top;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on\n"
                                           "{\n"
                                           "    border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                           "    height: 10px;\n"
                                           "    width: 10px;\n"
                                           "    subcontrol-position: bottom;\n"
                                           "    subcontrol-origin: margin;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
                                           "{\n"
                                           "    background: none;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
                                           "{\n"
                                           "    background: none;\n"
                                           "}")
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.IgnoreAction)
        self.setFlow(QListView.LeftToRight)
        self.setResizeMode(QListView.Fixed)
        self.setObjectName("tails_container")
        # items
        self.time = TimeStatus()
        self.speed = NetworkSpeedStatus()
        self.xgames = XGAMESButton()
        #
        self.add_item(self.xgames)
        self.add_item(self.time)
        self.add_item(self.speed)
        #
        #self.setItemAlignment(Qt.AlignmentFlag.AlignCenter)

    def add_item(self, item):
        # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(self)
        # Set size hint
        myQListWidgetItem.setSizeHint(item.sizeHint())
        # Add QListWidgetItem into QListWidget
        self.addItem(myQListWidgetItem)
        self.setItemWidget(myQListWidgetItem, item)


    def get_item(self, j):
        return self.itemWidget(self.item(j))