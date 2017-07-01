from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty

class Pad(Widget):
	diameter = NumericProperty(50)
	pad_color = ListProperty([1,1,1,1])
	pad_width = NumericProperty(0)

class JoyStick (Widget):
	background_color = ListProperty([0.75,0.75,0.75,0.75])
	perimeter_color = ListProperty([0,0,0,0.75])
	perimeter_width = NumericProperty(6)
	pad_color = ListProperty([1,1,1,1])
	pad_x = NumericProperty(0.0)
	pad_y = NumericProperty(0.0)
	pad_width = NumericProperty(50)
	_reach = NumericProperty(0)
	_perimeter_diameter = NumericProperty(0)
	
	def init(self,**kwargs):
		super(Joystick,self).__init__()
		#self.stick = Ellipse(pos=(self.center_x - 25, self.center_y - 25), size=(50,50),color=(1,1,1))
		#self.canvas.add_widget(self.stick)

	def do_layout(self):
		print("layout!")
		if len(self.ids) > 0:
			self.ids.pad.center = self.center
			self.ids.pad.pad_color = self.pad_color
			self.ids.pad.pad_width = self.pad_width
		
		self._reach = self.width/2 if self.width < self.height else self.height/2
		self._perimeter_diameter = self.width/2 if self.width < self.height else self.height/2
		self._perimeter_diameter -= self.perimeter_width / 2
	
	def on_size(self, *args):
		self.do_layout()
		
	
	def on_pos(self, *args):
		self.do_layout()
	
	def add_widget(self, widget):
		super(JoyStick, self).add_widget(widget)
		self.do_layout()
	
	def remove_widget(self, widget):
		super(JoyStick, self).remove_widget(widget)
		self.do_layout()
	
	def move_pad(self,x,y):
		distance = ((self.center_x - x)**2 + (self.center_y - y) ** 2)**(0.5)
		if distance > self._reach - self.ids.pad.diameter/2:
			new_distance = (self._reach - self.ids.pad.diameter/2) * 1.0 / distance
			new_x = -(self.center_x - x) * new_distance
			new_x = int(self.center_x + new_x)
			new_y = -(self.center_y - y) * new_distance
			new_y = int(self.center_y + new_y)
			self.ids.pad.center_x = new_x
			self.ids.pad.center_y = new_y

			self.pad_x = (x - self.center_x)*new_distance/(1.0*self._reach-self.pad_width/2.0)
			self.pad_y = (y - self.center_y)*new_distance/(1.0*self._reach-self.pad_width/2.0)
		else:
			self.ids.pad.center = (x,y)
			self.pad_x = (x - self.center_x)/(1.0*self._reach-self.pad_width/2.0)
			self.pad_y = (y - self.center_y)/(1.0*self._reach-self.pad_width/2.0)
		
		print("Pad values: {0},{1}".format(self.pad_x,self.pad_y))
	
	def on_touch_down(self, touch):
		if self.collide_point(touch.x,touch.y):
			print("I was touched!")
			self.move_pad(touch.x,touch.y)
		return super(JoyStick, self).on_touch_down(touch)
	
	def on_touch_move(self,touch):
		self.move_pad(touch.x,touch.y)
	
	def on_touch_up(self,touch):
		self.move_pad(self.center_x,self.center_y)


Builder.load_string("""
<JoyStick>:
	canvas:
		Color:
			rgba: root.background_color
		Rectangle:
			pos: self.pos
			size: self.size
		Color:
			rgba: root.perimeter_color
		Line:
			circle: self.center_x, self.center_y, root._perimeter_diameter
			width: root.perimeter_width
	Pad:
		id: pad

<Pad>:
	canvas:
		Color:
			rgba: root.pad_color
		Ellipse:
			pos: self.center_x - root.pad_width/2, self.center_y - root.pad_width/2
			size: root.pad_width,root.pad_width
			id: pad
""")

