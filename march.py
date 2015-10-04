import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MarchWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	songFile = None
	if(len(sys.argv) > 1):
		songFile = open(sys.argv[1], 'r')
	else:
		print("I'm temporarily requiring you to pass an .sm file as an argument right now")
		exit()
	wnd = MarchWindow(songFile)
	wnd.show()
	app.exec_()
