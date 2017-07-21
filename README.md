# Kivy Garden: Joystick  

Joystick Widget, intended to get analog like input from the user via a touch screen. The input can then be used as a control of some sort.  

![Example](https://github.com/kivy-garden/garden.joystick/blob/master/example/Example.gif?raw=true)  


## Widget Properties:  

**Joystick Data:**  

- 'pad', `pad_x`, `pad_y`: The position of the pad, relative to the center of the joystick.  
- `magnitude`: The distance of the pad from the center of the joystick. Use with radians or angle to get polar coordinates.  
- `radians` & `angle`:  The radians/degrees around the joystick that the current position is at.

- `is_active`: True during `on_touch_down` & `on_touch_move`. Remains False after on_touch_up until the next touch event.

**Options:**

- `sticky`: Enabled by default - causes the pad to rebound to the center of the joystick `on_touch_up`. When `False`, the pad will maintain its final position after `on_touch_up`.

**Style:**  

The joystick is composed 3 circles, two for the base (*inner & outer*) and one for the pad. Each of the circles has properties for size, background color, outline color, & outline width. There

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
    joystick.bind(pad=lambda instance, pad: print("x:", pad[0], "   y:", pad[1]))
    self.root.add_widget(joystick)

DemoApp().run()
```

**@ KV:**  

``` yaml
#: import Joystick kivy.garden.joystick.Joystick

BoxLayout:

  Joystick:
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
