from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QGridLayout, QGraphicsDropShadowEffect, \
    QVBoxLayout
import ui.file_rc

def set_visual_effects(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setColor(QColor(0, 0, 0))
    shadow.setBlurRadius(20)
    shadow.setOffset(0)
    widget.setGraphicsEffect(shadow)

class XGAMESButton(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #self.setMinimumSize(QSize(190, 108))
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/Logo/graphics/xgames_white.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.setObjectName("xgames_widget")
        #
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 40, 10, 40)
        self.xgames = QLabel()
        self.xgames.setPixmap(QPixmap(":/Logo/graphics/xgames_white.png"))
        self.xgames.setScaledContents(True)
        self.xgames.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.xgames.setFixedSize(150, 50)
        #
        self.user = QLabel("Bienvenido JalexCode Solutions")
        self.user.setWordWrap(True)
        self.user.setStyleSheet("color: white;\nfont: 12pt 'Segoe UI';")
        self.user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #
        self.layout.addWidget(self.xgames)
        self.layout.addWidget(self.user)
        #
        self.setLayout(self.layout)
        # PALETA
        self.p = QPalette()
        self.p.setColor(QPalette.ColorRole.Base, QColor(0, 204, 0))
        self.setPalette(self.p)
        self.setAutoFillBackground(True)
        # EFFECTS
        set_visual_effects(self)

    def set_user(self, user):
        self.user.setText(f"Bienvenido {user}")

    def enterEvent(self, event):
        self.p.setColor(QPalette.ColorRole.Base, QColor(0, 150, 0))
        self.setPalette(self.p)

    def leaveEvent(self, event):
        self.p.setColor(QPalette.ColorRole.Base, QColor(0, 204, 0))
        self.setPalette(self.p)

class TimeStatus(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #
        # PALETA
        self.p = QPalette()
        self.p.setColor(QPalette.ColorRole.Base, QColor(3, 213, 255))
        self.setPalette(self.p)
        self.setAutoFillBackground(True)
        # EFFECTS
        set_visual_effects(self)
        #
        self.setObjectName("time_widget")
        self.gridLayout_5 = QGridLayout(self)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_2 = QLabel(self)
        self.label_2.setMinimumSize(QSize(50, 50))
        self.label_2.setMaximumSize(QSize(50, 50))
        self.label_2.setStyleSheet("font: 20pt \"Segoe UI\";")
        self.label_2.setText("")
        self.label_2.setPixmap(QPixmap(":/Graphics/graphics/connected_time.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
        self.time_content = QWidget(self)
        self.time_content.setObjectName("time_content")
        self.gridLayout_4 = QGridLayout(self.time_content)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.time_percent = QLabel(self.time_content)
        self.time_percent.setStyleSheet("font: bold 12pt \"Segoe UI\";\n"
                                        "    color: rgb(255, 255, 255);")
        self.time_percent.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.time_percent.setObjectName("time_percent")
        self.gridLayout_4.addWidget(self.time_percent, 3, 0, 1, 1)
        self.current_time = QLabel(self.time_content)
        self.current_time.setStyleSheet("font: bold 16pt \"Segoe UI\";\n"
                                        "    color: rgb(255, 255, 255);")
        self.current_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.current_time.setObjectName("current_time")
        self.gridLayout_4.addWidget(self.current_time, 0, 0, 1, 1)
        self.elapsed_time = QLabel(self.time_content)
        self.elapsed_time.setStyleSheet("font: 14pt \"Segoe UI\";\n"
                                        "    color: rgb(255, 255, 255);")
        self.elapsed_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout_4.addWidget(self.elapsed_time, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.time_content, 0, 1, 1, 1)
        self.time_progress = QProgressBar(self)
        self.time_progress.setMaximumSize(QSize(16777215, 5))
        self.time_progress.setStyleSheet("QProgressBar {\n"
                                         "    border: none;\n"
                                         "    /*border-radius: 1px;\n"
                                         "    text-align: center;*/\n"
                                         "    background-color: rgb(0, 0, 0, 100);\n"
                                         "    height:1px;\n"
                                         "}\n"
                                         "\n"
                                         "QProgressBar::chunk {\n"
                                         "    border-radius: 0.5px;\n"
                                         "    background-color: white;\n"
                                         "}")
        self.time_progress.setProperty("value", 50)
        self.time_progress.setTextVisible(False)
        self.time_progress.setObjectName("time_progress")
        self.gridLayout_5.addWidget(self.time_progress, 1, 0, 1, 2)

        self.time_percent.setText("0%")
        self.current_time.setText("00:00:00")
        self.elapsed_time.setText("00:00:00")

    def enterEvent(self, event):
        self.p.setColor(QPalette.ColorRole.Base, QColor(0, 190, 255))
        self.setPalette(self.p)

    def leaveEvent(self, event):
        self.p.setColor(QPalette.ColorRole.Base, QColor(3, 213, 255))
        self.setPalette(self.p)

    def set_time(self, current="00:00:00", remaining="00:00:00", percent=0):
        self.current_time.setText(current)
        self.elapsed_time.setText(remaining)
        self.time_percent.setText(f"{percent}%")
        self.time_progress.setValue(percent)

class NetworkSpeedStatus(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #
        # PALETAA
        self.p = QPalette()
        self.p.setColor(QPalette.ColorRole.Base, QColor(255, 152, 166))
        self.setPalette(self.p)
        self.setAutoFillBackground(True)
        # EFFECTS
        set_visual_effects(self)
        #
        self.setObjectName("speed_widget")
        self.gridLayout_6 = QGridLayout(self)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_5 = QLabel(self)
        self.label_5.setMinimumSize(QSize(50, 50))
        self.label_5.setMaximumSize(QSize(50, 50))
        self.label_5.setStyleSheet("font: 20pt \"Segoe UI\";")
        self.label_5.setText("")
        self.label_5.setPixmap(QPixmap(":/Graphics/graphics/speed_flat.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 0, 0, 1, 1)
        self.widget_5 = QWidget(self)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_10 = QGridLayout(self.widget_5)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_9 = QGridLayout(self.widget_6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.upload_speed = QLabel(self.widget_6)
        self.upload_speed.setStyleSheet("font: bold 14pt \"Segoe UI\";\n"
                                        "    color: rgb(255, 255, 255);")
        self.upload_speed.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.upload_speed.setObjectName("upload_speed")
        self.gridLayout_7.addWidget(self.upload_speed, 0, 0, 1, 1)
        self.increase_u_speed = QLabel(self.widget_6)
        self.increase_u_speed.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                            "    color: rgb(255, 255, 255);")
        self.increase_u_speed.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.increase_u_speed.setObjectName("increase_u_speed")
        self.gridLayout_7.addWidget(self.increase_u_speed, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.download_speed = QLabel(self.widget_6)
        self.download_speed.setStyleSheet("font: bold 14pt \"Segoe UI\";\n"
                                          "    color: rgb(255, 255, 255);")
        self.download_speed.setObjectName("download_speed")
        self.gridLayout_8.addWidget(self.download_speed, 0, 0, 1, 1)
        self.increase_d_speed = QLabel(self.widget_6)
        self.increase_d_speed.setStyleSheet("font: 12pt \"Segoe UI\";\n"
                                            "    color: rgb(255, 255, 255);")
        self.increase_d_speed.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.increase_d_speed.setObjectName("increase_d_speed")
        self.gridLayout_8.addWidget(self.increase_d_speed, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 1, 1, 1)
        self.gridLayout_10.addWidget(self.widget_6, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.widget_5, 0, 1, 1, 1)

        self.upload_speed.setText("↑ 0 B")
        self.increase_u_speed.setText("+0 B")
        self.download_speed.setText("↓ 0 B")
        self.increase_d_speed.setText("+0 B")

    def enterEvent(self, event):
        self.p.setColor(QPalette.ColorRole.Base, QColor(255, 130, 130))
        self.setPalette(self.p)

    def leaveEvent(self, event):
        self.p.setColor(QPalette.ColorRole.Base, QColor(255, 152, 166))
        self.setPalette(self.p)

    def set_speed(self, u, d, i_u=0, i_d=0):
        self.upload_speed.setText(f"↑ {u}")
        self.download_speed.setText(f"↓ {d}")
        #
        self.increase_u_speed.setText(str(i_u))
        self.increase_d_speed.setText(str(i_d))
