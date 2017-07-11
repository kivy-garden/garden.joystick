from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty
import math


class Pad(Widget):
    '''This widget represents the controller's pad, the part that the user will
    actively interact with and moves with their touches. What the user will
    think of as the joystick.
    '''
    diameter = NumericProperty(50)
    pad_color = ListProperty([1, 1, 1, 1])
    pad_width = NumericProperty(0)


class Joystick (Widget):
    '''Joystick Widget, intended to get analog like input from the user via a
    touch screen. The input can then be used as a control of some sort.
    '''

    background_color = ListProperty([0.75, 0.75, 0.75, 0.75])
    '''Background color of entire widget. The square background area behind the
    pad and perimeter. Format is (r, g, b, a)

    :attr:`background_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [0.75, 0.75, 0.75, 0.75].
    '''

    perimeter_color = ListProperty([0, 0, 0, 0.75])
    '''Color for circle that will mark the limits of the joystick's pad's
    movement. Format is (r, g, b, a)

    :attr:`perimeter_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [0, 0, 0, 0.75].
    '''

    perimeter_line_width = NumericProperty(6)
    '''Line width for the perimeter circle that marks the limits of the
    joystick's pad's movement. Just a number.

    :attr:`perimeter_line_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `6`.
    '''

    pad_color = ListProperty([1, 1, 1, 1])
    '''Color for the pad of the joystick. The pad being the part the user
    actually interacts with. Format is (r, g, b, a)

    :attr:`pad_color` is a :class:`~kivy.properties.ListProperty` and defaults
    to [0, 0, 0, 0.75].
    '''

    pad_width = NumericProperty(50)
    '''Size of the pad of the joystick. The pad being the part the user
    actually interacts with. This will set the diameter of the pad. It must be
    smaller than the widget's width - perimeter_line_width. If it is larger the
    pad won't be able to move and there will be no input from the user. The
    closer pad_width and the widget's width are to each other, the less
    movement, and therefore the less granulairty of input. Choose size wisely.

    :attr:`pad_width` is a :class:`~kivy.properties.NumericProperty` and
    defaults to `50`.
    '''

    pad_x = NumericProperty(0.0)
    '''Output variable. This variable provides the percent position of the pad
    on the x axis. writing to this variable will be ignored. You should only
    use this to read the position of the joystick. Value ranges from -1.0 to
    1.0

    :attr:`pad_x` is a :class:`~kivy.properties.NumericProperty` and defaults
    to `0.0`.
    '''

    pad_y = NumericProperty(0.0)
    '''Output variable. This variable provides the percent position of the pad
    on the y axis.writing to this variable will be ignored. You should only use
    this to read the position of the joystick. Value ranges from -1.0 to 1.0

    :attr:`pad_y` is a :class:`~kivy.properties.NumericProperty` and defaults
    to `0.0`.
    '''

    magnitude = NumericProperty(0.0)
    '''Output variable. This variable provides the extend, from 0 to 1.0 that
    the joystick is moved off of the center. Combined with radians or angle you
    can create a polar coordinate.

    :attr:`magnitude` is a :class:`~kivy.properties.NumericProperty` and
    defaults to `0.0`.
    '''

    radians = NumericProperty(0.0)
    '''Output variable. This variable provides the position, in radians, that
    the joystick is at counter / anti clockwise relative to the x axis.

    :attr:`radians` is a :class:`~kivy.properties.NumericProperty` and defaults
    to `0.0`.
    '''

    angle = NumericProperty(0.0)
    '''Output variable. This variable provides the position, in degrees, that
    the joystick is at counter / anti clockwise relative to the x axis.

    :attr:`angle` is a :class:`~kivy.properties.NumericProperty` and defaults
    to `0.0`.
    '''

    pad_callback = ListProperty([])
    '''Because I'm not yet that great at properties yet. This is a list of
    callbacks that will be called whenever the pad moves.

    :attr:`pad_callback` is a :class:`~kivy.properties.ListProperty` and
    defaults to [].
    '''

    _reach = NumericProperty(0)
    '''The maximum reach of the pad with in the joystick. Used to keep the
    joystick inside the perimeter so it feels and behaves like a normal
    joystick.
    '''

    _perimeter_diameter = NumericProperty(0)
    '''The size of the circle to be drawn to create the perimeter of the
    joystick area. It is computed by taking the heighth or width of the widget,
    which ever is smaller, and subtracting from that the width of the perimeter
    line.
    '''

    def init(self, **kwargs):
        super(Joystick, self).__init__()

    def do_layout(self):
        # This check is done to make sure the pad exists.
        if len(self.ids) > 0:
            self.ids.pad.center = self.center
            self.ids.pad.pad_color = self.pad_color
            self.ids.pad.pad_width = self.pad_width

        self._reach = self.width / 2 \
            if self.width < self.height else self.height / 2
        self._perimeter_diameter = self.width / 2 \
            if self.width < self.height else self.height / 2
        self._perimeter_diameter -= self.perimeter_line_width / 2

    def on_size(self, *args):
        self.do_layout()

    def on_pos(self, *args):
        self.do_layout()

    def add_widget(self, widget):
        super(Joystick, self).add_widget(widget)
        self.do_layout()

    def remove_widget(self, widget):
        super(Joystick, self).remove_widget(widget)
        self.do_layout()

    def move_pad(self, x, y):
        # Get the relative distance from the touch to the joystick's center.
        distance = (
            (self.center_x - x) ** 2 + (self.center_y - y) ** 2) ** (0.5)

        # If the distance is greater than the reach of the joystick,
        # we must trunkate it to the limit of the circle
        if distance > self._reach - self.ids.pad.diameter / 2:
            # in this case, the magnitude must alwasy be 1.
            self.magnitude = 1.0

            # Get the amount to adjust the distance by.
            new_distance = (self._reach - self.ids.pad.diameter / 2) \
                * 1.0 / distance

            # get the distance from the joystick's center, with the adjustment.
            new_x = (x - self.center_x) * new_distance
            # add the joystick's center to get the position absolutely.
            new_x = int(self.center_x + new_x)

            # get the distance from the joystick's center, with the adjustment.
            new_y = (y - self.center_y) * new_distance
            # add the joystick's center to get the position absolutely.
            new_y = int(self.center_y + new_y)

            # place the pad.
            self.ids.pad.center_x = new_x
            self.ids.pad.center_y = new_y

            # Output values, I think this could be optomized...
            self.pad_x = (x - self.center_x) * new_distance \
                / (1.0 * self._reach - self.pad_width / 2.0)
            self.pad_y = (y - self.center_y) * new_distance \
                / (1.0 * self._reach - self.pad_width / 2.0)

        else:
            # magnitude is the percent of the reach.
            self.magnitude = distance / self._reach
            # move the pad to it's new position.
            self.ids.pad.center = (x, y)
            # Output values
            self.pad_x = (x - self.center_x) \
                / (1.0 * self._reach - self.pad_width / 2.0)
            self.pad_y = (y - self.center_y) \
                / (1.0 * self._reach - self.pad_width / 2.0)

        if self.pad_x == 0 and self.pad_y == 0:  # centered.
            pass
        elif self.pad_x == 0:  # not on the y axis, but squarly on the X.
            pass
        elif self.pad_y == 0:  # not on the x axis, but squarly on the Y.
            pass
        else:  # when the joystick is somewhere out and about.
            if self.pad_x > 0 and self.pad_y > 0:  # First Quadrant.
                self.radians = math.atan(1.0 * self.pad_y / self.pad_x)
            elif self.pad_x < 0 and self.pad_y > 0:  # Second Quadrant
                self.radians = math.pi \
                    + math.atan(1.0 * self.pad_y / self.pad_x)
            elif self.pad_x < 0 and self.pad_y < 0:  # Third Quadrant
                self.radians = math.pi \
                    + math.atan(1.0 * self.pad_y / self.pad_x)
            else:  # Fourth Quadrant
                self.radians = math.pi * 2 \
                    + math.atan(1.0 * self.pad_y / self.pad_x)

        # Convert the radians into degrees.
        self.angle = math.degrees(self.radians)

        # call the callback for the joystick moving. The only way I could
        # figure out how to get updates out. I believe this should be doable
        # via properties, but this works for now.
        for callback in self.pad_callback:
            callback()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.move_pad(touch.x, touch.y)
            # save myself in the touch for later reference.
            touch.ud['pad'] = self
            return True
        return super(Joystick, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        # check that this is a touch related to joysticks.
        if 'pad' in touch.ud:
            # check that this touch is related to me.
            if touch.ud['pad'] == self:
                self.move_pad(touch.x, touch.y)

    def on_touch_up(self, touch):
        # check that this is a touch related to joysticks.
        if 'pad' in touch.ud:
            # check that this touch is related to me.
            if touch.ud['pad'] == self:
                self.move_pad(self.center_x, self.center_y)


Builder.load_string('''
<Joystick>:
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
            width: root.perimeter_line_width
    Pad:
        id: pad

<Pad>:
    canvas:
        Color:
            rgba: root.pad_color
        Ellipse:
            pos:
                (self.center_x - root.pad_width / 2,
                self.center_y - root.pad_width / 2)
            size: root.pad_width, root.pad_width
            id: pad
''')

# To the King!
