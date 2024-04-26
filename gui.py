from tkinter import Tk

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("The PDF merger")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f"{width}x{height}")
        self.__running = False
        # root.mainloop()

    def get_root(self):
        return self.__root

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False
