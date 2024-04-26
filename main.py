from gui import Window
from pdf_merger import DocSelector
import sys


def main():
    screen_x = 500
    screen_y = 600

    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)
    docs = DocSelector(win)
    docs.update_mergedlist()
    
    win.wait_for_close()

main()