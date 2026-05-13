from tkinterdnd2 import TkinterDnD

from ui.main_window import main

class TSNOVAApp(TkinterDnD.Tk):

    def __init__(self):

        super().__init__()

        main(self)


if __name__ == "__main__":

    app = TSNOVAApp()

    app.mainloop()