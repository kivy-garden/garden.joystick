from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from kivy.app import App
from kivy.garden.joystick import Joystick
from kivy.uix.floatlayout import FloatLayout


class JoystickDemo(FloatLayout):
  pass


class JoystickDemoApp(App):
  def build(self):
    self.root = JoystickDemo()
    self._bind_joysticks()

  def _bind_joysticks(self):
    joysticks = self._get_joysticks(self.root)
    for joystick in joysticks:
      joystick.bind(pad=self._update_pad_display)

  def _get_joysticks(self, parent):
    joysticks = []
    if isinstance(parent, Joystick):
      joysticks.append(parent)
    elif hasattr(parent, 'children'):
      for child in parent.children:
        joysticks.extend(self._get_joysticks(child))
    return joysticks

  def _update_pad_display(self, instance, pad):
    x, y = pad
    x, y = (str(x)[0:5], str(y)[0:5])
    x, y = (('x: ' + x), ('\ny: ' + y))
    r = "radians: " + str(instance.radians)[0:5]
    m = "\nmagnitude: " + str(instance.magnitude)[0:5]
    a = "\nangle: " + str(instance.angle)[0:5]
    self.root.ids.pad_display_xy.text = "".join([x, y])
    self.root.ids.pad_display_rma.text = "".join([r, m, a])


JoystickDemoApp().run()
