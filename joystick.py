from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.properties import NumericProperty

class Pad(Widget):
	diameter = NumericProperty(50)

class JoyStick (Widget):
	reach = NumericProperty(0)
	def init(self,**kwargs):
		super(Joystick,self).__init__()
		#self.stick = Ellipse(pos=(self.center_x - 25, self.center_y - 25), size=(50,50),color=(1,1,1))
		#self.canvas.add_widget(self.stick)

	def do_layout(self):
		print("layout!")
		if len(self.ids) > 0:
			self.ids.pad.center = self.center
		
		self.reach = self.width/2 if self.width > self.height else self.height/2
	
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
		if distance > self.reach - self.ids.pad.diameter/2:
			new_distance = (self.reach - self.ids.pad.diameter/2) * 1.0 / distance
			new_x = -(self.center_x - x) * new_distance
			new_x = int(self.center_x + new_x)
			new_y = -(self.center_y - y) * new_distance
			new_y = int(self.center_y + new_y)
			self.ids.pad.center_x = new_x
			self.ids.pad.center_y = new_y
		else:
			self.ids.pad.center = (x,y)
		
	
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
			rgba: 0.75,0.75,0.75,0.75
		Rectangle:
			pos: self.pos
			size: self.size
		Color:
			rgba: 0,0,0,0.75
		Line:
			circle: self.center_x, self.center_y, self.width/2 - 3
			width: 6
	size: (200,200)
	size_hint: None, None
	Pad:
		id: pad

<Pad>:
	canvas:
		Color:
			rgba: 1,1,1,1
		Ellipse:
			pos: self.center_x - self.diameter/2, self.center_y - self.diameter/2
			size: self.diameter,self.diameter
			id: pad
""")

