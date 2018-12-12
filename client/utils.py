from PyQt5.QtWidgets import QMessageBox

def pop_info_and_back(this, info, back_hook):
    button = QMessageBox.question(this, "Info",\
                                info,\
                                QMessageBox.Ok,\
                                QMessageBox.Ok)
    if button == QMessageBox.Ok:
        back_hook()
        this.close()
    else:
        this.close()
        raise SystemExit(0)