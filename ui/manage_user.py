from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDialog, QInputDialog, QTableWidgetItem, QMenu, QAction, QMessageBox
from data.database_handler import *
import ui.file_rc
from ui.users_manage import Ui_Dialog


class ManageUser(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self)
        #uic.loadUi("ui/users_manage.ui", self)
        self.setupUi(self)
        self.__parent = parent
        self.__users = ()
        #
        self.tableWidget.itemDoubleClicked.connect(self.edit_user)
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.custom_context_menu)
        self.fill_table()

    def clean_table(self):
        # tabla principal
        while self.tableWidget.rowCount () > 0:
            self.tableWidget.removeRow (0)

    def fill_table(self):
        self.__users = SELECT_USERS()
        self.__parent.update_db_users()
        self.clean_table()
        for tuple in self.__users:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(tuple[0].split(".")[0] if tuple[0] else "-"))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(tuple[4].split(".")[0] if tuple[4] else "-"))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(tuple[5].split(".")[0] if tuple[5] else "-"))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(tuple[2].split(".")[0] if tuple[2] else "-"))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(tuple[3].split(".")[0] if tuple[3] else "-"))
        self.tableWidget.resizeColumnsToContents()

    def edit_user(self):
        row = self.tableWidget.currentRow()
        #column = self.tableWidget.currentColumn()
        # --------------------------------------- #
        user, passw = self.__users[row][0], self.__users[row][1]
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor("white"))
        #palette.setColor(QPalette.ColorRole.Base, QColor(150, 150, 150))
        window = QInputDialog(self)
        window.setStyleSheet(u"\ncolor:white;\nfont: bold 12pt 'Segou UI';}")
        window.setForegroundRole(QPalette.ColorRole.Text)
        window.setPalette(palette)
        input, ok = window.getText(self, "Editar contraseña", "Nueva contraseña del usuario:", 2)
        if input and ok:
            print("ok")
            UPDATE_PASSW(user, encode_passw(input))
        self.fill_table()

    def delete_user(self, row):
        q = QMessageBox.question(self, "Eliminar usuario", f"¿Realmente desea eliminar el usuario?",
                                 QMessageBox.Yes | QMessageBox.No)
        if q == QMessageBox.Yes:
            #row = self.tableWidget.currentRow()
            DEL_USER(self.__users[row][0])
            self.fill_table()

    def custom_context_menu(self, pos):
        try:
            row = self.tableWidget.currentRow()
            if row != -1:
                print("ASD")
                menu = QMenu()
                action = QAction("Eliminar usuario", menu)
                # abrir_explorer.setData(indice)
                action.triggered.connect(lambda: self.delete_user(row))
                menu.addAction(action)
                menu.exec(self.tableWidget.viewport().mapToGlobal(pos))
        except Exception as e:
            print(e.args)
            #self.error("Mostrando menú conceptual", e.args)
            SENT_TO_LOG(f"Mostrando menú conceptual {e.args}")