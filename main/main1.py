import torch
import win32gui
from PIL import ImageGrab
import pyautogui
import pynput
import pandas
from ctypes import CDLL
import time
from pynput.mouse import Button, Controller



csgo_handle = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
model = torch.hub.load(r'D:\AIII\test\yolov5-master(original)\yolov5-master', 'custom',
                       path=r'D:\AIII\test\yolov5-master(original)\yolov5-master\runs\train\354exp9\weights\best'
                            r'.engine',
                       source='local')  # tenorrt model
model.conf = 0.5
press = False
mouse = Controller()
pyautogui.FAILSAFE = False
gm = CDLL('ghub_device.dll')
gm.device_open()


def key_down(key=''):
    gm.key_down(key.encode('utf-8'))


def key_up(key=''):
    gm.key_up(key.encode('utf-8'))


def mouse_move(x, y, abs_move=False):
    gm.moveR(x, y, abs_move)
# int only


def mouse_down(key):
    gm.mouse_down(key)


def mouse_up(key):
    gm.mouse_up(key)


def inference(model, img, size):
    # im = csgo_screenshot(csgo_handle)
    results = model(img, size=size)
    df = results.pandas().xyxy[0]
    # print(df)
    return df


def autoaim(df_head):
    distance_list = []
    for i in range(df_head.shape[0]):
        xmin = df_head.iat[i, 0]
        xmax = df_head.iat[i, 2]
        ymin = df_head.iat[i, 1]
        ymax = df_head.iat[i, 3]
        center_position_x = (xmin + xmax) / 2
        center_position_y = (ymin + ymax) / 2
        distance = ((center_position_x - 1920 / 2) ** 2 + (center_position_y - 1080 / 2) ** 2) ** 0.5
        distance_list.append(distance)
    if len(distance_list) == 0:
        pass
    else:
        choice_row = distance_list.index(min(distance_list))
        choice_df_head = df_head.loc[[choice_row]]
        xmin = choice_df_head.iat[0, 0]
        xmax = choice_df_head.iat[0, 2]
        ymin = choice_df_head.iat[0, 1]
        ymax = choice_df_head.iat[0, 3]
        aim_x = int((xmin + xmax) / 2)
        aim_y = int((ymin + ymax) / 2)
        a = 2.5
        #a = 2
        if press:
            mouse_move(int((aim_x - 1920 / 2) * a), int((aim_y - 1080 / 2) * a))
            gm.mouse_down(1)
            time.sleep(0.0001)
            gm.mouse_up(1)
            #mouse.move((aim_x - 1920 / 2) * a, (aim_y - 1080 / 2) * a)
            #pyautogui.mouseDown()
            #pyautogui.mouseUp()
        if not press:
            pass


def on_click(x, y, button, pressed):
    global press
    if pressed and button == button.x1:
        press = not press
        print('True' if press else 'False')


if __name__ == '__main__':
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()
    while 1:
        df_head = pandas.DataFrame()
        fullscreen = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        dataframe = inference(model, fullscreen, 1056)

        if dataframe.empty:
            print('no object')
            pass
        else:
            x = time.time()
            zero_object_times = 0
            df_head = df_head.append(dataframe[dataframe['class'] == 1], ignore_index=True)
            # print(df_head)
            autoaim(df_head)


