from pynput import keyboard

class ShortcutCallback:


    def __init__(self):


        # Collect events until released
        # with keyboard.Listener(
        #        on_press=on_press,
        #       on_release=on_release) as listener:
        #   listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()