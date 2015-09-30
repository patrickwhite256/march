import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MarchWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	wnd = MarchWindow()
	wnd.show()
	app.exec_()
