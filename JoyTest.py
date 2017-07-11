from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.app import App
from joystick import Joystick

class JoyTest (FloatLayout):
    
    def addJoystick(self):
        pass
        js = Joystick()
        self.add_widget(js)

class JoyTestApp (App):
    def build(self):
        game = JoyTest()
        game.addJoystick()
        return game
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        pass

if __name__ == "__main__":
    app = JoyTestApp()
    app.run()
