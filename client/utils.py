from PyQt5.QtWidgets import QMessageBox

def pop_info_and_back(self, info, back_hook):
    button = QMessageBox.question(self, "Info",\
                                info,\
                                QMessageBox.Ok,\
                                QMessageBox.Ok)
    if button == QMessageBox.Ok:
        back_hook()
        self.close()
    else:
        self.close()
        raise SystemExit(0)