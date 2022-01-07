from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog
import ui.file_rc
from ui.floating_window_v2 import Ui_Dialog


class FloatingWindow(Ui_Dialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.parent = parent
        #uic.loadUi("ui/floating_window_v2.ui", self)
        self.setupUi(self)
        #
        self.opacity_value = 0
        self.setWindowOpacity(self.opacity_value)
        #
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowSystemMenuHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.pressing = False
        #
        self.max_btn.clicked.connect(self.intercambiar)
        self.close_btn.clicked.connect(self.hide)
        #
        self.show_current = True
        self.img_time.clicked.connect(self.toggle_current_left_time)

    def toggle_current_left_time(self):
        if self.show_current:
            self.img_time.setIcon(QIcon(":/Graphics/graphics/left_time.png"))
        else:
            self.img_time.setIcon(QIcon(":/Graphics/graphics/connected_time.png"))
        self.show_current = not self.show_current

    def change_ntw_status(self, status):
        if status:
            self.ntw_status.setToolTip("Con acceso a XGAMES")
            self.ntw_status.setPixmap(QPixmap(":/Graphics/graphics/connected.png"))
        else:
            self.ntw_status.setToolTip("Sin conexión")
            self.ntw_status.setPixmap(QPixmap(":/Graphics/graphics/not_connected.png"))

    def change_internet_status(self, status):
        if status:
            self.internet_status.setToolTip("Conectado a Internet")
            self.internet_status.setPixmap(QPixmap(":/Graphics/graphics/success.png"))
        else:
            self.internet_status.setToolTip("Sin conexión a Internetg")
            self.internet_status.setPixmap(QPixmap(":/Graphics/graphics/critical.png"))

    def change_opacity(self, value):
        self.setWindowOpacity(value/100)

    def set_time(self, current, left="00:00:00"):
        if self.show_current:
            self.connected_time.setText(current)
        else:
            self.connected_time.setText(left)

    def network_speed(self, up, down):
        self.upload.setText(f"↑ {up}")
        self.download.setText(f"↓ {down}")

    def up_down_data(self, up, down):
        self.uploaded.setText(f"↑ {up}")
        self.downloaded.setText(f"↓ {down}")

    def time_alert(self, status):
        if status:
            self.connected_time.setStyleSheet('color: rgb(255, 85, 127);\nfont: 12pt "Segoe UI";')
        else:
            self.connected_time.setStyleSheet('color: white;\nfont: 12pt "Segoe UI";')

    def intercambiar(self):
        self.parent.showNormal()
        self.hide()

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                             self.mapToGlobal(self.movement).y(),
                             self.width(), self.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def show_animated(self):
        if not self.isVisible():
            self.show()
            self.animate()
        else:
            self.opacity_value = 90
            self.show()

    # INTERFAZ
    def animate(self, duration=2, function=b"fade_in", start_value=0, end_value=90):
        self.animation = QPropertyAnimation(self, function)
        self.animation.setDuration(duration * 1000)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.start()

    @pyqtProperty(int)
    def fade_in(self):
        return self.opacity_value

    @fade_in.setter
    def fade_in(self, value):
        self.opacity_value = value / 100
        self.setWindowOpacity(self.opacity_value)