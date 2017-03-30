''' import module here '''
import pythoncom, pyHook
import auto_complete

app = auto_complete.LIST_GUI()

def monitor():
    '''
    Input: None
    Functionality: Monitor the signal from keypad. Hold the signal once received.
    Return: input event
    '''
    # create a hook manager
    hm = pyHook.HookManager()
    # call interpret when keydown
    hm.KeyDown = app.keyDown
    hm.KeyUp = app.keyUp
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()
