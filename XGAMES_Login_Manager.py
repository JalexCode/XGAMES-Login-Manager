import threading
import time
from contextlib import closing
from datetime import datetime
from sys import argv

import psutil
import requests
from PyQt5.QtCore import (QEasingCurve, QEvent, QPropertyAnimation, QRect, Qt,
                          QTime, QTimer, QUrl, pyqtProperty)
from PyQt5.QtGui import QColor, QDesktopServices, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QCompleter,
                             QDialogButtonBox, QGraphicsDropShadowEffect,
                             QInputDialog, QLabel, QLineEdit, QMainWindow,
                             QMenu, QMessageBox, QSystemTrayIcon)

import ui.file_rc
import ui.icons_rc
from data.const import *
from data.database_handler import *
from data.logger import SENT_TO_LOG
from data.settings import *
from data.styles import (styleLineEditError, styleLineEditOk, stylePopupError,
                         stylePopupOk)
from data.threads import InternetSpeedMeterThread#, ParserThread
from data.util import *
from ui.floating_window import FloatingWindow
from ui.main_v2 import Ui_MainWindow
from ui.manage_user import ManageUser

#from ui.tails_container import QCustomListWidget


CREATE_DB()
# >---------------------------------------------------------------------------------------------------------------< #
class MainApp(Ui_MainWindow, QMainWindow):
    ntw_speed_thread_alive = True
    is_warned = False
    def __init__(self):
        QMainWindow.__init__(self)
        #uic.loadUi("ui/main_v2.ui", self)
        self.setupUi(self)
        #
        self.is_logged_in = False
        self.internet_available = True
        self.connected = QTime(0, 0, 0)
        self.left = None
        #
        self.init()
        self.connections()
        #
        self.check_is_already_login()

    def nd(self, segundos: 'int'):
        str = ""
        horas = int(segundos // 3600)
        segundos -= horas * 3600
        minutos = int(segundos // 60)
        segundos -= minutos * 60
        if horas:
            str += f"{horas}h"
        if minutos:
            str += f"{minutos}m"
        if segundos:
            str += f"{segundos}s"
        return str

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.password_ledit.setEchoMode(QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.password_ledit.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)

    def animate_notification(self, show=True):
        parent = self.frame_error.parent()
        spacing = 5
        coord = parent.x()+spacing, parent.y()+spacing
        if show:
            start = *coord, 0, parent.height()-spacing
            end = *coord, parent.width()-spacing*2, parent.height()-spacing
        else:
            start = *coord, parent.width()-spacing*2, parent.height()-spacing
            end = *coord, 0, parent.height()
        self.frame_error.setGeometry(*start)
        if show:
            self.frame_error.show()
        self.animation = QPropertyAnimation(self.frame_error, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setStartValue(QRect(*start))
        self.animation.setEndValue(QRect(*end))
        self.animation.start()
        self.frame_error.setGeometry(*end)
        if not show:
            self.frame_error.hide()

    def showMessage(self, message, status=False, show_details=True):
        self.animate_notification()
        self.label_error.setText(message)
        if status:
            self.show_details.setVisible(False)
            self.frame_error.setStyleSheet(stylePopupOk)
        else:
            self.show_details.setVisible(show_details)
            self.frame_error.setStyleSheet(stylePopupError)

    def closeMessage(self):
        self.animate_notification(False)

    def checkFields(self):
        messages = []
        # CHECK USER
        if not self.user_ledit.text():
            messages.append(" Usuario vacío ")
            self.user_ledit.setStyleSheet(styleLineEditError)
        else:
            self.user_ledit.setStyleSheet(styleLineEditOk)

        # CHECK PASSWORD
        if not self.password_ledit.text() and self.permanent_rb.isChecked():
            messages.append(" Contraseña vacía ")
            self.password_ledit.setStyleSheet(styleLineEditError)
        else:
            self.password_ledit.setStyleSheet(styleLineEditOk)

        # CHECK FIELDS
        if len(messages):
            text = " | ".join(messages)
            self.show_details.hide()
            self.showMessage(text, False, show_details=False)
            return False
        return True

    def check_is_already_login(self):
        print("check_is_already_login")
        self.stackedWidget.setCurrentIndex(3)
        try:
            page = requests.get(self.get_mikrotic_ip(), verify=False, timeout=3)
            if page.status_code == 200:  # SUCCESS
                # ----------------------------------------------------------------------------------- #
                # if already logged in
                if is_logged_in(page.text):
                    #
                    print("ESTA LOGGEADO")
                    # start service
                    if "Bienvenido" in page.text:
                        start_cutting = '<br><div style="text-align: center;">Bienvenido'
                        welcome_idx = page.text.index(start_cutting)
                        end_idx = page.text.index('!</div><br><table border="1" class="tabula">')
                        user = page.text[welcome_idx+len(start_cutting):end_idx].strip()
                        self.user_ledit.setText(user)
                        self.start_status_service(user, notificate=False)
                        return
        except Exception as e:
            self.error_2_log(f"Chequeando contenido de {SETTINGS.value('mikrotic_ip', type=str)}", details=e.args)
        self.stackedWidget.setCurrentIndex(1)

    def init(self):
        self.setWindowTitle(APP_NAME)
        #
        self.f_window = FloatingWindow(self)
        self.message = None
        #
        self.frame_error.hide()
        #
        # visual effects
        self.set_visual_effects(self.login_btn)
        self.set_visual_effects(self.logout_btn)
        self.set_visual_effects(self.frame_error)
        self.set_visual_effects(self.welcome_widget)
        self.set_visual_effects(self.time_widget)
        self.set_visual_effects(self.speed_widget)
        self.set_visual_effects(self.up_down_widget)
        self.set_visual_effects(self.tile_widget)
        self.set_visual_effects(self.buttonBox)
        # password line edit
        self.visibleIcon = QIcon(":/icons/icons/eye_on_32x32.png")
        self.hiddenIcon = QIcon(":/icons/icons/eye_off_32x32.png")
        self.password_ledit.setEchoMode(QLineEdit.Password)
        self.togglepasswordAction = self.password_ledit.addAction(self.visibleIcon,
                                                                  QLineEdit.ActionPosition.TrailingPosition)
        self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)
        self.password_shown = False
        # VARS
        self.var_upload_speed = 0
        self.var_download_speed = 0
        self.parser = None
        self.first_time = datetime.now()
        self.users_register = SELECT_USERS()
        # main timer
        self.refresh = QTimer()
        self.refresh.timeout.connect(self.update_connected_time)
        # uploaded/downloaded timer
        self.request_page = QTimer()
        self.request_page.timeout.connect(self.check_page)
        # check if already connected to XGAMES
        self.check_network = QTimer()
        self.check_network.timeout.connect(self.check_xgames)
        self.check_network.start(1000)
        # check Internet availability
        self.check_internet = QTimer()
        self.check_internet.timeout.connect(self.check_internet_)
        #
        self.adding_components()

    def set_visual_effects(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0))
        shadow.setBlurRadius(20)
        shadow.setOffset(0)
        widget.setGraphicsEffect(shadow)

    def check_username(self, text):
        for n in self.users_register:
            if n[0] == text:
                passw = n[1]
                print(passw)
                if passw:
                    self.permanent_rb.setChecked(True)
                    self.password_ledit.setEnabled(True)
                else:
                    self.ticket_rb.setChecked(True)
                    self.password_ledit.setEnabled(False)
                self.password_ledit.setText(decode_passw(passw))
                break

    def update_db_users(self):
        self.users_register = SELECT_USERS()
        #
        my_completer = QCompleter(GET_USERSNAMES(), self)
        my_completer.setCaseSensitivity(0)
        self.user_ledit.setCompleter(my_completer)

    def adding_components(self):
        self.user_ledit.setFocus()
        self.update_db_users()
        #
        self.status_lbl = QLabel(f"{APP_NAME} {VERSION}")
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.status_lbl.setFont(font)
        self.status_lbl.setStyleSheet("color: white;")
        self.statusbar.addWidget(self.status_lbl)
        #
        self.systray = QSystemTrayIcon(QIcon(":/Icon/graphics/icon.png"), self)
        self.systray_menu = QMenu(self)
        #
        self.max_action = QAction(QIcon(":/Graphics/graphics/topbar_floating_button_maximize.png"), "Maximizar")
        self.max_action.triggered.connect(self.showNormal)
        self.systray_menu.addAction(self.max_action)
        self.quit_action = QAction(QIcon(":/Graphics/graphics/pss_close_nor.png"), "Salir")
        self.quit_action.triggered.connect(self.close)
        self.systray_menu.addAction(self.quit_action)
        # Establecer en el objeto systray.
        self.systray.setContextMenu(self.systray_menu)
        self.systray.messageClicked.connect(self.show)
        self.systray.show()
        #
        self.ntw_status = QLabel()
        self.internet_status = QLabel()
        size = 20
        #
        self.internet_status.setMaximumSize(size, size)
        self.internet_status.setMinimumSize(size, size)
        self.internet_status.setScaledContents(True)
        self.internet_status.setPixmap(QPixmap(":/Graphics/graphics/critical.png"))
        self.statusbar.addPermanentWidget(self.internet_status)
        #
        self.ntw_status.setMaximumSize(size, size)
        self.ntw_status.setMinimumSize(size, size)
        self.ntw_status.setScaledContents(True)
        self.ntw_status.setPixmap(QPixmap(":/Graphics/graphics/not_connected.png"))
        self.statusbar.addPermanentWidget(self.ntw_status)
        #
        self.fill_ntw_adapters()
        self.load_settings()

    def connections(self):
        self.close_pupup.clicked.connect(self.closeMessage)
        self.login_btn.clicked.connect(self.login)
        self.logout_btn.clicked.connect(self.logout)
        self.show_f_window.triggered.connect(self.f_window.show_animated)
        self.admin_users_action.triggered.connect(self.show_users_manage)
        self.user_ledit.textChanged.connect(self.check_username)
        self.show_details.clicked.connect(self.details_message)
        #
        self.options.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0) if self.stackedWidget.currentIndex() != 1 else self.stackedWidget.slideInIndex(0))
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_default)
        self.go_back.clicked.connect(self.go_to_last_page)
        #
        import webbrowser
        self.support_2.triggered.connect(lambda: webbrowser.open(SUPPORT, new=1, autoraise=False))#QDesktopServices.openUrl(QUrl(SUPPORT)))
        self.donate.triggered.connect(self.show_donate_info)
        self.about_me.triggered.connect(lambda: webbrowser.open(DEVELOPER_TELEGRAM, new=1, autoraise=False))
        self.developer_channel.triggered.connect(lambda: webbrowser.open(DEVELOPER_TELEGRAM_CHANNEL, new=1, autoraise=False))
        #self.about_me.triggered.connect(lambda: self.stackedWidget.slideInNext())

    def go_to_last_page(self):
        self.stackedWidget.go_to_last_page()

    def fill_ntw_adapters(self):
        adapters = []
        net = psutil.net_io_counters(pernic=True)
        if net:
            for a in net.keys():
                adapters.append(a)
        #
        self.network_adapter.addItems(adapters)

    def restore_default(self):
        RESTORE()
        self.load_settings()

    def load_settings(self):
        try:
            # adapters
            actual = SETTINGS.value("netw_adapter", type=str)
            idx = self.network_adapter.findText(actual)
            if idx > -1:
                self.network_adapter.setCurrentIndex(idx)
            else:
                self.network_adapter.setCurrentIndex(0)
            # ip
            mikrotic_ip = SETTINGS.value("mikrotic_ip", type=str)
            self.mikrotic_ip.setText(mikrotic_ip)
            #
        except Exception as e:
            self.error("Cargando configuración", "No se pudo cargar la configuración", e.args)    

    def save_settings(self):
        try:
            dict = {}
            #
            adapter = self.network_adapter.currentText()
            dict["netw_adapter"] = adapter
            #
            mikrotic_ip = self.mikrotic_ip.text()
            dict["mikrotic_ip"] = mikrotic_ip
            #
            SAVE(dict)
            #
            self.showMessage(f"Configuración guardada", True)
        except Exception as e:
            self.error("Guardando configuración", "No se pudo guardar la configuración", e.args)

    def get_mikrotic_ip(self):
        return PROTOCOL + self.mikrotic_ip.text()#SETTINGS.value("mikrotic_ip", type=str)

    def login(self):
        try:
            user = self.user_ledit.text().strip()
            passw = self.password_ledit.text()
            if self.checkFields():
                user = "".join(user.split())
                try:
                    # get login page
                    login_page = requests.get(self.get_mikrotic_ip(), verify=False, timeout=3)
                    if login_page.status_code == 200:  # SUCCESS
                        # ----------------------------------------------------------------------------------- #
                        # if already logged in
                        if is_logged_in(login_page.text):
                            # start service
                            self.start_status_service(user)
                            return
                        # else post user credentials to login
                        try:
                            payl = post_data(user, passw, login_page.text)
                            with closing(
                                    requests.post("%s/login" % self.get_mikrotic_ip(), data=payl, verify=False)) as post:
                                if post.status_code == 200:  # SUCCESS
                                    # if success, service starts
                                    self.start_status_service(user)
                        except Exception as e:
                            self.error("LogIn", "Error al realizar POST", e.args)
                    self.start_status_service(user)
                except Exception as e:
                   self.error("LogIn", "Ha ocurrido un error\n-Al solicitar página de logIn\n-Comprobando si se había iniciado sesión", e.args)
        except Exception as e:
            self.error("LogIn", "No se pudo iniciar sesión", e.args)

    def logout(self):
        try:
            with closing(requests.get(f"{SETTINGS.value('mikrotic_ip', type=str)}/logout", verify=False, timeout=3)) as logout_request:
               if logout_request.status_code == 200:
                    #
                    self.set_logged(False)
        except Exception as e:
            self.error("LogOut", "No se pudo cerrar la sesión", e.args)

    def save_user_info(self):
        # save user info
        user = self.user_ledit.text().strip()
        current = self.current_time.text()
        left = self.elapsed_time.text()
        UPDATE_TIME(user, current, left, self.first_time, datetime.now())

    def set_logged(self, status, notificate_session_details=True, notificate_timeout=False):
        icon = QIcon()
        if status:
            #
            text = " Login OK "
            if self.checkBox_save_user.isChecked():
                try:
                    user = self.user_ledit.text().strip()
                    passw = self.password_ledit.text()
                    ADD_USER(user, passw)
                except Exception as e:
                    self.error("Actualizando estado de Login", "Guardando usuario", e.args)
                    if notificate_session_details:
                        text = text + " | !!! No se pudo guardar el usuario !!! (revise el LOG)"
                        self.showMessage(text, False)
                else:
                    if notificate_session_details:
                        text = text + " | Usuario guardado! "
                        self.showMessage(text, True)
            #
            print(True)
            self.stackedWidget.slideInIndex(2)
            self.check_internet.start(1000)
        else:
            print("*C CERRo")
            self.ntw_speed_thread_alive = False
            self.refresh.stop()
            self.request_page.stop()
            self.check_internet.stop()
            self.stackedWidget.slideInIndex(1)
            # floating window
            self.f_window.network_speed(0, 0)
            self.f_window.set_time("00:00:00")
            #
            if notificate_session_details:
                text = " Sesión cerrada "
                self.showMessage(text, True, show_details=False)
            if notificate_timeout:
                text = " Su tiempo se ha agotado "
                self.showMessage(text, False, show_details=False)
                self.systray.showMessage("Fin de sesión", text, QSystemTrayIcon.MessageIcon.Warning)
            #
            self.check_internet.stop()
            self.internet_status.setPixmap(QPixmap(":/Graphics/graphics/critical.png"))
            #
            self.save_user_info()
        self.login_btn.setIcon(icon)

    def start_status_service(self, user, notificate=True):
        # get connected time and left time from status's page (once)
        connected, left = self.get_connected_left_time()
        #print(connected, left)
        if connected is not None:
            self.connected = self.connected.fromString(connected, 'hh:mm:ss')
            if left is not None:
                self.left = QTime(0, 0, 0)
                self.left = self.left.fromString(left, 'hh:mm:ss')
            # set logged in UI
            self.set_logged(True, notificate_session_details=notificate)
            # show Username
            self.f_window.user_welcome.setText(user)
            self.set_user(user)
            # save first time connected
            self.first_time = datetime.now()
            # start timer
            self.refresh.start(1000)
            self.request_page.start(5000)
            #
            #ntw speed
            self.ntw_speed_thread_alive = True
            self.get_network_speed()

    def check_page(self):
        try:
            with closing(requests.get(self.get_mikrotic_ip(), verify=False)) as main_page:
                if main_page.status_code == 200:  # SUCCESS
                    # check if error ocurred
                    try:
                        check_post_response(main_page.text)
                    except Exception as e:
                        self.error(f"Solicitando página en {SETTINGS.value('mikrotic_ip', type=str)}", f"La página lanzó un error", e.args)
                        return
                    if is_logged_in(main_page.text):
                        try:
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(main_page.text, "html.parser")
                            table = soup.find("table", {"class": "tabula"})
                            if table is not None:
                                # find all table values
                                td = table.find_all("td")
                                for i in range(len(td)):
                                    item = td[i]
                                    if item.text == "bytes up/down:":
                                        # splitting value by " / " normally
                                        value = td[i+1].text.split(" / ")
                                        # extracting uploaded & downloaded data
                                        up = speed_2_bytes(value[0])
                                        down = speed_2_bytes(value[1])
                                        # showing
                                        self.uploaded_data.setText(f"↑ {nz(up)}")
                                        self.downloaded_data.setText(f"↓ {nz(down)}")
                                        # showing in floating window
                                        self.f_window.up_down_data(nz(up), nz(down))
                                        return
                            else:
                                return
                        except Exception as e:
                           self.error("Obteniendo bytes traficados", "Error durante Web Scraping", e.args)
                    else:
                        self.set_logged(False, True)
                        return False
        except Exception as e:
           self.error(f"Solicitando página en {SETTINGS.value('mikrotic_ip', type=str)}", details=e.args)

    def update_connected_time(self):
        #print("INICIO TIMER DE ACTUALIZACION DE TIEMPO")
        def set_time(current="00:00:00", remaining="00:00:00", percent=0):
            self.current_time.setText(current)
            self.elapsed_time.setText(remaining)
            self.time_percent.setText(f"{percent}%")
            self.time_progress.setValue(percent)
        try:
            left_time = "00:00:00"
            connected_time = self.connected.toString('hh:mm:ss')
            if self.ticket_rb.isChecked():
                left_time = self.left.toString('hh:mm:ss')
        except Exception as e:
            self.error_2_log("Mostrando datos", "Extrayendo tiempo", e.args)
            return
        ui = "Ventana principal"
        try:
            # Main Window #
            percent = 0
            if self.ticket_rb.isChecked():
                percent = percent_elapsed_time(connected_time, left_time)
            set_time(connected_time, left_time, percent)
            print(left_time)
            #set_speed(upload, download,increase_upload, increase_download)
            # Floating Window
            ui = "Ventana flotante"
            self.f_window.set_time(connected_time, left_time)
            #self.f_window.network_speed(upload, download)
        except Exception as e:
            self.error_2_log("Mostrando datos", f"Mostrando valores en la interfaz {ui}", e.args)
            return
        #
        if self.left is not None:
            percent = percent_elapsed_time(self.connected.toString('hh:mm:ss'), self.left.toString('hh:mm:ss'))
            print(percent)
            if percent >= 80 and percent < 100:
                self.time_alert(True, self.left.toString('hh:mm:ss'))
            # if time is over
            elif percent >= 100:
                #connected, left = self.get_connected_left_time()
                # check if it really happened
                #if connected is None:
                self.set_logged(False, notificate_session_details=False, notificate_timeout=True)
                #    return
                # else
                # warning
                self.time_alert(False)
                self.is_warned = False
                # continue
                #self.connected = self.connected.fromString(connected, 'hh:mm:ss')
                #self.left = self.left.fromString(left, 'hh:mm:ss')
                return
            self.left = self.left.addSecs(-1)
        self.connected = self.connected.addSecs(1)
        #

    def get_connected_left_time(self):
        connected = None
        left = None
        # retry 5 times
        for i in range(5):
            if connected is not None:
                break
            try:
                with closing(requests.get(self.get_mikrotic_ip(), verify=False)) as main_page:
                    if main_page.status_code == 200:  # SUCCESS
                        # check if error ocurred
                        try:
                            check_post_response(main_page.text)
                        except Exception as e:
                            self.error("Obteniendo tiempo", e.args[0])
                            break
                        if is_logged_in(main_page.text):
                            try:
                                from bs4 import BeautifulSoup
                                soup = BeautifulSoup(main_page.text, "html.parser")
                                table = soup.find("table", {"class": "tabula"})
                                # find all table values
                                td = table.find_all("td")
                                for i in range(len(td)):
                                    item = td[i]
                                    if item.text == "connected:":
                                        # connected time must be after "connected:" item
                                        connected = td[i+1].text
                                        # to format hh:mm:ss
                                        connected = parse_time(connected)
                                    elif item.text == "connected / left:":
                                        # spliting string by " / "
                                        value = td[i+1].text.split(" / ")
                                        # first value must be connected time
                                        connected = value[0]
                                        # to format hh:mm:ss
                                        connected = parse_time(connected)
                                        # second value most be left time
                                        left = value[1]
                                        # to format hh:mm:ss
                                        left = parse_time(left)
                                break
                            except Exception as e:
                                self.error("Obteniendo tiempo", "Error durante Web Scraping", e.args)
                        else:
                            self.is_logged_in = False
                            break
            except Exception as e:
                self.error("Obteniendo tiempo", f"Realizando petición a '{SETTINGS.value('mikrotic_ip', type=str)}/status'", e.args)
        return connected, left

    def time_alert(self, status, left="00:00:00"):
        if status:
            if not self.is_warned:
                # show notification
                self.systray.showMessage("Ha consumido el 80% del tiempo disponible", f"Tiempo restante {left}", QSystemTrayIcon.MessageIcon.Warning)
                self.is_warned = True
            # change UI
            self.elapsed_time.setStyleSheet('color: rgb(255, 85, 127);\nfont: 14pt "Segoe UI";')
            self.current_time.setStyleSheet('color: rgb(255, 85, 127);\nfont: bold 16pt "Segoe UI";')
        else:
            self.elapsed_time.setStyleSheet('color: white;\nfont: 14pt "Segoe UI";')
            self.current_time.setStyleSheet('color: white;\nfont: bold 16pt "Segoe UI";')
        self.f_window.time_alert(status)

    def set_speed(self, u, d, recieved_bytes):
        # speed
        increase_upload = 0
        increase_download = 0
        try:
            increase_upload = calculate_increase_speed(self.var_upload_speed, u)
            increase_download = calculate_increase_speed(self.var_download_speed, d)
            self.var_upload_speed = u
            self.var_download_speed = d
        except Exception as e:
            self.error_2_log("Mostrando velocidad", "Calculando diferencia de velocidad", e.args)
            #
        self.upload_speed.setText(f"↑ {nz(u)}")
        self.download_speed.setText(f"↓ {nz(d)}")
        self.f_window.network_speed(nz(u), nz(d))
        #
        self.increase_u_speed.setText(str(increase_upload))
        self.increase_d_speed.setText(str(increase_download))

    def get_network_speed(self):
        try:
            # valores
            ul = 0.00
            dl = 0.00
            #
            t0 = time.time()
            network = SETTINGS.value("netw_adapter")
            if network:
                self.speed_thread = InternetSpeedMeterThread(self)
                self.speed_thread.speed.connect(self.set_speed)
                upload = psutil.net_io_counters(pernic=True)[network][0]
                download = psutil.net_io_counters(pernic=True)[network][1]
                up_down = (upload, download)
                #
                thread = threading.Thread(target=self.speed_thread.run, args=(ul, dl, t0, up_down,))
                thread.start()
        except Exception as e:
            print("get_network_speed", end=" -> ")
            print(e.args)

    def check_xgames(self):
        def check_request():
            try:
                requests.get(self.get_mikrotic_ip(), timeout=2)
            except Exception as e:
                self.refresh.stop()
                self.set_ntw_status(False)
                print("XGAMES - " + str(e.args))
            else:
                self.set_ntw_status(True)
        #
        thread = threading.Thread(target=check_request)
        thread.start()

    def check_internet_(self):
        def check_request():
            # internet connection papu
            try:
                requests.get("http://www.google.com", timeout=2)
            except Exception as e:
                print("INTERNET - " +  str(e.args))
                #
                if self.internet_available:
                    self.systray.showMessage(APP_NAME, "No hay conexión a Internet", QSystemTrayIcon.MessageIcon.Critical)
                #
                self.set_internet_status(False)
                #
            else:
                self.set_internet_status(True)
        #
        thread = threading.Thread(target=check_request)
        thread.start()

    def set_internet_status(self, status):
        if status:
            self.internet_status.setToolTip("Conectado a Internet")
            self.internet_status.setPixmap(QPixmap(":/Graphics/graphics/success.png"))
        else:
            self.internet_status.setToolTip("Sin conexión a Internet")
            self.internet_status.setPixmap(QPixmap(":/Graphics/graphics/critical.png"))
        self.f_window.change_internet_status(status)
        self.internet_available = status

    def set_ntw_status(self, status):
        if status:
            self.ntw_status.setToolTip("Conectado a X-GAMES")
            self.ntw_status.setPixmap(QPixmap(":/Graphics/graphics/connected.png"))
        else:
            self.ntw_status.setToolTip("Desconectado de X-GAMES")
            self.ntw_status.setPixmap(
                QPixmap(":/Graphics/graphics/not_connected.png"))
        self.f_window.change_ntw_status(status)

    def show_users_manage(self):
        self.users_manage = ManageUser(self)
        self.users_manage.show()

    def details_message(self):
        if self.message is not None:
            self.message.exec_()
            self.message = None

    def error(self, place, text="", details=""):
        self.error_2_log(place, text, details)
        ####################################
        self.message = QMessageBox(QMessageBox.Icon.Critical, "Error", f"* {place} *")
        self.message.buttonClicked.connect(self.frame_error.close)
        self.message.setBaseSize(300, 100)
        self.message.setInformativeText(f"-> {text}")
        if details:
            self.message.setDetailedText(str(details))
        #
        self.showMessage(text.split("\n")[0])
        self.show_details.setVisible(True)
        self.frame_error.setStyleSheet(stylePopupError)

    def error_2_log(self, place, text="", details=""):
        SENT_TO_LOG("->".join((place, str(text), str(details))))

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMinimized and self.stackedWidget.currentIndex() == 1:
                self.hide()
                self.f_window.show_animated()
            # elif event.oldState() == Qt.WindowState.WindowMinimized:
            #     self.floating_window.close()

    def closeEvent(self, event):
        try:
            self.ntw_speed_thread_alive = False
            self.check_internet.stop()
            self.check_network.stop()
            self.refresh.stop()
            self.f_window.close()
            event.accept()
        except:
            event.accept()
    # MOSTRAR DATOS ####################################################################################################
    def set_user(self, user):
        self.user_2.setText(f"Bienvenido {user}")

    def show_donate_info(self):
        i = QMessageBox.information(self, "Donación", "Este software es gratis. Como desarrollador solo gano la satisfacción de saber que usted lo usa y le es útil. Aún así, si desea sentirse parte de este proyecto y apoyarlo además de motivarme a seguir desarrollándolo, siempre puede realizar una donación. Gracias de antemano :-)\nMi número: 54655909")

def main():
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
