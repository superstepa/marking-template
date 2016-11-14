try:
    # Python 2 support.
    from Tkinter import Tk
except ImportError:
    from tkinter import Tk


class PyClipboard(Tk):

    def __enter__(self):
        self.withdraw()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.destroy()

    def clear_clipboard(self):
        try:
            # Python2
            self.clipboard.clear()
        except AttributeError:
            self.clipboard_clear()

    def copy_to_clipboard(self, text):
        """Copies the passed text to the users clipboard"""
        try:
            # Python2
            self.clipboard.append(text)
        except AttributeError:
            # Python3
            self.clipboard_append(text)

    def paste(self):
        try:
            # Python2
            return self.clipboard.get()
        except AttributeError:
            # Python3
            return self.clipboard_get()
