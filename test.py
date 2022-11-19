from __future__ import print_function
from PyQt5 import QtCore, QtGui, QtWidgets

qapp = QtWidgets.QApplication([])
worker_thread = QtCore.QThread()
worker_thread.start()
worker_thread.quit()

def fin():
    print('isFinished:', worker_thread.isFinished())
    print("9999")

worker_thread.finished.connect(fin)
QtCore.QTimer.singleShot(2000, fin)
qapp.exec_()