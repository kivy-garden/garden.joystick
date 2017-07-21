# Kivy Garden: Joystick  

Touch-friendly, analog-gamepad style controls for Kivy.  

![Example](https://github.com/kivy-garden/garden.joystick/blob/master/example/Example.gif?raw=true)  

### [**Code for JoystickDemo**](https://github.com/kivy-garden/garden.joystick/tree/master/example)  

&nbsp;  

## Widget Properties:  

See [**joystick.py**](https://github.com/kivy-garden/garden.joystick/blob/master/joystick/joystick.py) for further reference.  

**Joystick Data:**  

- `pad`, `pad_x`, `pad_y`: The position of the pad, relative to the center of the joystick.  
- `magnitude`: The distance of the pad from the center of the joystick. Use with radians or angle to get polar coordinates.  
- `radians` & `angle`:  The radians/degrees of the joystick in relation to the x-axis.

**Options:**

- `sticky`: False by default. When True, the pad will maintain its final position after `on_touch_up`. Otherwise, the pad will rebound to the center of the joystick `on_touch_up`.

**Style:**  

* The joystick is composed of 3 circles, two for the base (*inner & outer*) and one for the pad. Each of the circles has properties for size, background color, outline color, & outline width.

&nbsp;  

## Usage:  

**@ Python:**  

``` python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.joystick import Joystick

class DemoApp(App):
  def build(self):
    self.root = BoxLayout()
    joystick = Joystick()
    joystick.bind(pad=lambda instance, pad: print("x:", pad[0], "  y:", pad[1]))
    self.root.add_widget(joystick)

DemoApp().run()
```

**@ KV:**  

``` yaml
#: import Joystick kivy.garden.joystick.Joystick

BoxLayout:

  Joystick:
    sticky: False
    outer_size: 1
    inner_size: 0.75
    pad_size:   0.5
    outer_line_width: 0.01
    inner_line_width: 0.01
    pad_line_width:   0.01
    outer_background_color: (0.75, 0.75, 0.75, 0.3)
    outer_line_color:       (0.25, 0.25, 0.25, 0.3)
    inner_background_color: (0.75, 0.75, 0.75, 0.1)
    inner_line_color:       (0.7,  0.7,  0.7,  0.1)
    pad_background_color:   (0.4,  0.4,  0.4,  0.3)
    pad_line_color:         (0.35, 0.35, 0.35, 0.3)
```
