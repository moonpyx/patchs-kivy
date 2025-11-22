from kivy.utils import platform
from kivy.clock import Clock
import kivy.uix.textinput as textinput

if platform == 'android':
    import android
    from android import mActivity


class FixTextInput(textinput.TextInput):
    def __init__(self, **kwargs):
        super(FixTextInput, self).__init__(**kwargs)

    def action_keyboard(self, instance, value, *largs):
        if self.keyboard_mode == 'auto':
            if value:
                self._bind_keyboard()
            else:
                self._unbind_keyboard()
        

    def _on_focus(self, *args):   
        #print("FixTextInput _on_focus called")
        if platform == 'android':
            self.apply_fix(*args)
        else:
            self.action_keyboard(*args)
    
    def _unbind_keyboard(self):        
        keyboard = self._keyboard
        if keyboard:
            keyboard.unbind(on_key_down=self.keyboard_on_key_down,
                            on_key_up=self.keyboard_on_key_up,
                            on_textinput=self.keyboard_on_textinput)
            
                
            if self._requested_keyboard:                             
                self._keyboard = None
                self._requested_keyboard = False
                if keyboard in self._keyboards:
                    if self in self._keyboards.values():
                        keyboard.release() 
                        del self._keyboards[keyboard]
               
            else:
                self._keyboards[keyboard] = None

    def active_focus(self, *args):
        self.action_keyboard(*args)
        
        

    def on__keyboard(self, ins, keyboard):
        if keyboard:
            print("_keyboard ",  keyboard)
            print(self.order_ch)
            mActivity.changeKeyboard(self.order_ch[0])
            Clock.schedule_once(lambda x: mActivity.changeKeyboard(self.order_ch[1]), .1)
        

    def apply_fix(self, *args):
        self.order_ch=[1,2]
        if args[1]:
            self.order_ch=[2,1] if self.input_type in ["text","null"] else [1,2]
            Clock.schedule_once(lambda dt: self.active_focus(*args), .4)
            
        else:
            mActivity.changeKeyboard(2)
            Clock.schedule_once(lambda x: self._unbind_keyboard(),1/24.)


def apply_fix_textinput():
    print("Applying Patch TextInput fix for Android")
    from kivy.uix.textinput import TextInput
    TextInput.active_focus = FixTextInput.active_focus
    TextInput.apply_fix = FixTextInput.apply_fix
    TextInput.action_keyboard = FixTextInput.action_keyboard
    TextInput._unbind_keyboard = FixTextInput._unbind_keyboard
    TextInput._on_focus = FixTextInput._on_focus
    TextInput.on__keyboard = FixTextInput.on__keyboard