import threading
import time
from contextlib import closing

import psutil
import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QMessageBox

from data.const import URL
from data.logger import SENT_TO_LOG
from data.settings import *
from data.util import is_logged_in, nz

class ParserThread(QObject):
    set_data = pyqtSignal(dict)
    error = pyqtSignal(str, str, object)
    stop = pyqtSignal()
    def __init__(self, parent=None):
        QObject.__init__(self)
        self.parent = parent

    def run(self):
        try:
            with closing(requests.get(self.parent.get_mikrotic_ip(), verify=False)) as main_page:
                if main_page.status_code == 200:  # SUCCESS
                    if is_logged_in(main_page.text):
                        try:
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(main_page.text, "html.parser")
                            ######################################################################
                            table = soup.find("table", {"class": "tabula"})
                            # items
                            td = table.find_all("td")
                            dict = {}
                            for i in range(0, len(td), 2):
                                text = td[i].getText().strip(":").strip()
                                value = td[i + 1].getText()
                                dict[text] = value
                                #
                                self.set_data.emit(dict)
                        except Exception as e:
                            self.error.emit("Hilo de parseo", "Error parseando datos", e.args)
                    else:
                        self.stop.emit()
        except Exception as e:
            self.error.emit("Hilo de parseo", f"Realizando petición a '{URL}/status'", e.args)

class InternetSpeedMeterThread(QObject):
    speed = pyqtSignal(float, float, str)
    error = pyqtSignal(str)
    stop = False
    def __init__(self, parent=None):
        super(InternetSpeedMeterThread, self).__init__(parent)
        self.parent = parent

    def run(self, ul, dl, t0, up_down):
        while self.parent.ntw_speed_thread_alive:
            NETWORK = SETTINGS.value("netw_adapter")
            dictry = psutil.net_io_counters(pernic=True)
            adapters = dictry.keys()
            if not NETWORK or NETWORK is None or not NETWORK in adapters:
                NETWORK = tuple(adapters)[0]
            try:
                last_up_down = up_down
                upload = dictry[NETWORK][0]
                download = dictry[NETWORK][1]
                # speed
                speed = dictry.get(NETWORK)
                #
                t1 = time.time()
                up_down = (upload, download)
                try:
                    ul, dl = [(now - last) / (t1 - t0)  # / 1024.0
                              for now, last in zip(up_down, last_up_down)]
                    t0 = time.time()
                except:
                    pass
                if dl > 0.1 or ul >= 0.1:
                    # time.sleep(0.75)
                    self.speed.emit(ul, dl, nz(speed.bytes_recv))
                else:
                    self.speed.emit(0.00, 0.00, nz(speed.bytes_recv))
            except Exception as e:
                print("InternetSpeedMeterThread", end=" -> ")
                print(e.args)
                SENT_TO_LOG(f"LEER LA VELOCIDAD DEL TRAFICO - {e.args}")
            time.sleep(1)


