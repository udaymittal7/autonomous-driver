import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# The code provides two functions PressKey and ReleaseKey to simulate the pressing and releasing of keys on a keyboard using Windows API's SendInput function.
# The following constants are defined to represent the virtual key codes for the keys 'W', 'A', 'S', and 'D':

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)

# to hold the information related to the keyboard input
class KeyBdInput(ctypes.Structure):
    _fields_ = [
        # Virtual-key code of the key
        ("wVk", ctypes.c_ushort),
        # Hardware scan code of the key.
                ("wScan", ctypes.c_ushort),
                # Flags that specify various aspects of the keystroke. Here 0x0008 indicates that the key is being pressed.
                ("dwFlags", ctypes.c_ulong),
                # Time stamp for the event, in milliseconds.
                ("time", ctypes.c_ulong),
                # Pointer to an extra value associated with the keystroke.
                ("dwExtraInfo", PUL)]

# to hold the information related to hardware events
class HardwareInput(ctypes.Structure):
    _fields_ = [
        # Type of hardware message
        ("uMsg", ctypes.c_ulong),
        # Low-order word of the wParam value.
                ("wParamL", ctypes.c_short),
               # High-order word of the wParam value.
                ("wParamH", ctypes.c_ushort)]

# to hold the information related to the mouse input
class MouseInput(ctypes.Structure):
    _fields_ = [
        # The horizontal motion distance
        ("dx", ctypes.c_long),
        # The vetical motion distance
                ("dy", ctypes.c_long),
                # The amount of data associated with the mouse event
                ("mouseData", ctypes.c_ulong),
                # Flags that specify various aspects of the mouse event
                ("dwFlags", ctypes.c_ulong),
                # Time stamp for the event, in milliseconds
                ("time",ctypes.c_ulong),
                # Pointer to an extra value associated with the mouse event
                ("dwExtraInfo", PUL)]

# to combine the three structs mentioned above. It has three fields, one for each struct type.
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

# to hold the type of input (Hardware, Keyboard or Mouse) and an instance of the Input_I union.
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

# takes a hex key code as an argument and uses SendInput to simulate the key press event. The function creates an instance of the Input struct, fills it with the appropriate values and sends it to SendInput.
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#  takes a hex key code as an argument and uses SendInput to simulate the key release event. The function creates an instance of the Input struct, fills it with the appropriate values and sends it to SendInput.
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    PressKey(0x11)
    time.sleep(1)
    ReleaseKey(0x11)
    time.sleep(1)