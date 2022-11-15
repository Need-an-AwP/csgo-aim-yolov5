import win32gui
from PIL import ImageGrab
import pyautogui
import pandas
import numpy
import matplotlib.pyplot as plt

csgo_handle = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')


def csgo_screenshot(csgo_handle):
    left, top, right, bottom = win32gui.GetWindowRect(csgo_handle)
    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    return im


if __name__ == '__main__':
    im = csgo_screenshot(csgo_handle)
    plt.imshow(im)
    plt.show()
    print(type(im))
