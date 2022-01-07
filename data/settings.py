# > ---------------------------------------- SETTINGS -------------------------------------------------------------
from PyQt5.QtCore import QSettings
from data.const import *
from data.logger import SENT_TO_LOG

DEFAULT_SETTINGS = {"netw_adapter":"", "mikrotic_ip":"192.168.10.1"}
SETTINGS = QSettings(APP_ID, "settings")

def RESTORE():
    for i in DEFAULT_SETTINGS.keys():
        SETTINGS.setValue(i, DEFAULT_SETTINGS[i])

def SAVE(dict):
    for i in dict:
        SETTINGS.setValue(i, dict[i])
    SETTINGS.sync()

try:
    for key in DEFAULT_SETTINGS.keys():
        if SETTINGS.value(key) is None:
            SETTINGS.setValue(key, DEFAULT_SETTINGS[key])
    SETTINGS.sync()
except Exception as e:
    print("REESTABLECIENDO CONFIGURACION")
    SENT_TO_LOG(f"REESTABLECIENDO CONFIGURACION {e.args}")