# Kivy Garden: Joystick  

Joystick Widget, intended to get analog like input from the user via a touch screen. The input can then be used as a control of some sort.  

![Example](https://raw.githubusercontent.com/Narcolapser/garden.joystick/master/Joystick%20screenshot.png)  

## Usage:  

Import it into your project like any other garden widget:  

``` python
from kivy.garden.joystick import Joystick
```

## Widget Properties:  

**Joystick Data:**  

- `pad_x` & `pad_y`: The percent position of the pad.  
- `magnitude`: Percent position from origin to perimeter line. mash together with radians or angle to get polar coordinates.  
- `radians` & `angle`:  The radians/degrees around the joystick that the current position is at. It is solved first for radians, but the angle in degrees is included for simplicity for the implementer.  

**Style:**  

- `background_color`: The color for the whole background of the widget.  
- `perimeter_color`: Color of the perimeter line.  
- `perimeter_line_width`: The width of the perimeter line of the joystick's control area.  
- `pad_color`: Color of the control pad.  
- `pad_width`: Size of the control pad.  
