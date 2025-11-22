from patch import apply_fix_textinput

apply_fix_textinput()

from kivy.core.window import Window
Window.softinput_mode="below_target"

from kivy.app import runTouchApp
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import  BoxLayout

bx=BoxLayout(orientation="vertical")
bx.add_widget(TextInput(input_type="number", size_hint_y=None))
bx.add_widget(TextInput(size_hint_y=None))

runTouchApp(bx)



