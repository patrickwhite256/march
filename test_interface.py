
import pickle
from GUI import Application, ScrollableView, Document, Window, Cursor, rgb
from GUI.Files import FileType
from GUI.StdColors import black

class InterfaceApp(Application):
	def __init__(self):
		Application.__init__(self)

	def open_app(self):
		self.new_cmd()

	def make_document(self, fileref):
		return AppDoc()

	def make_window(self, document):
		win = Window(size = (400, 400), document = document)
		view = ApplicationView(model = document, extent = (1000, 1000), scrolling = 'hv')
		win.place(view, left = 0, top =  0, right = 0, bottom = 0, sticky = 'nsew')
		win.show()



class ApplicationView(ScrollableView):

	def draw(self, canvas, update_rect):
		canvas.pencolor = black

	def mouse_down(self, event):
		x, y = event.position
		canvas.fill_frame_rect(x - 20, y - 20, x + 20, y + 20)


class AppDoc(Document):

	boxes = None

	def new_contents(self):
		self.boxes = []

	def read_contents(self, file):
		self.boxes = pickle.load(file)

	def write_contents(self, file):
		pickle.dump(self.boxes, file)



InterfaceApp().run()