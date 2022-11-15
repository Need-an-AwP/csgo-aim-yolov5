import random
import threading
import torch
from PIL import ImageGrab
import pynput
from pynput import keyboard
import pandas
from ctypes import CDLL
import time

model = torch.hub.load(r'D:\AIII\test\yolov5-master(original)\yolov5-master', 'custom',
                       path=r'D:\AIII\test\yolov5-master(original)\yolov5-master\runs\train\354exp9\weights\best'
                            r'.engine',
                       source='local')  # tenorrt model
model.conf = 0.7
press = False
autoaim_switch = False
gm_switch = False
choice_df = pandas.DataFrame()
dataframe = pandas.DataFrame()
gm = CDLL('ghub_device.dll')


def on_activate_w():
    global autoaim_switch
    if autoaim_switch:
        autoaim_switch = False
    else:
        autoaim_switch = True
    print('autoaim state {}'.format(autoaim_switch))


def on_activate_q():
    global gm_switch
    if gm_switch:
        gm_switch = False

    else:
        gm_switch = True


def keyboard_listener():
    with keyboard.GlobalHotKeys({'<ctrl>+<alt>+w': on_activate_w, '<ctrl>+<alt>+q': on_activate_q}) as h:
        h.join()


def on_click(x, y, button, pressed):
    global press
    if pressed and button == button.x1:  # autoshot hotkey
        press = not press
        print('button.x1 pressed' if press else 'button.x1 released')


def key_down(key=''):
    gm.key_down(key.encode('utf-8'))


def key_up(key=''):
    gm.key_up(key.encode('utf-8'))


def mouse_move(x, y, abs_move=False):
    gm.moveR(x, y, abs_move)  # int only


def mouse_click(key):
    gm.mouse_down(key)
    time.sleep(0.001)
    gm.mouse_up(key)


def inference(model, img, size):
    results = model(img, size=size)
    df = results.pandas().xyxy[0]
    # print(df)
    return df


def nonstop_detect():
    global dataframe
    global choice_df
    while 1:
        df_head = pandas.DataFrame()
        df_body = pandas.DataFrame()
        fullscreen = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        dataframe = inference(model, fullscreen, 1056)
        # print(dataframe)
        if not dataframe.empty:
            df_body = df_body.append(dataframe[dataframe['class'] == 0], ignore_index=True)
            df_head = df_head.append(dataframe[dataframe['class'] == 1], ignore_index=True)
            if df_head.empty:
                distance_list_body = []
                for i in range(df_body.shape[0]):
                    center_position_x_body = (df_body.iat[i, 0] + df_body.iat[i, 2]) / 2
                    center_position_y_body = (df_body.iat[i, 1] + df_body.iat[i, 3]) / 2
                    distance_body = ((center_position_x_body - 1920 / 2) ** 2 + (
                            center_position_y_body - 1080 / 2) ** 2) ** 0.5
                    distance_list_body.append(distance_body)
                if len(distance_list_body) == 0:
                    pass
                else:
                    choice_row_body = distance_list_body.index(min(distance_list_body))
                    choice_df = df_body.loc[[choice_row_body]]
            if not df_head.empty:
                distance_list = []
                for i in range(df_head.shape[0]):
                    center_position_x = (df_head.iat[i, 0] + df_head.iat[i, 2]) / 2
                    center_position_y = (df_head.iat[i, 1] + df_head.iat[i, 3]) / 2
                    distance = ((center_position_x - 1920 / 2) ** 2 + (center_position_y - 1080 / 2) ** 2) ** 0.5
                    distance_list.append(distance)
                if len(distance_list) == 0:
                    pass
                else:
                    choice_row = distance_list.index(min(distance_list))
                    choice_df = df_head.loc[[choice_row]]
        if dataframe.empty:
            pass


a = 2.5


# when a=5 m_yaw 0.0165 correct in y
# a=3
# a=2.5


def aim_once():
    if dataframe.empty:
        pass
    else:
        x = ((choice_df.iat[0, 0] + choice_df.iat[0, 2]) / 2) * a - 960 * a
        y = ((choice_df.iat[0, 1] + choice_df.iat[0, 3]) / 2) * a - 540 * a
        mouse_move(int(x), int(y))


def loop1():  # ctrl+alt+w
    while True:
        time.sleep(0.1)  # work normally in 0.1
        if autoaim_switch:
            aim_once()
            # print('autoaim_switch on')
            if not autoaim_switch:
                pass
        else:
            print('autoaim_switch off')
            pass


'''def loop2():  # ctrl+alt+q
    while True:
        if gm_switch:
            gm.device_open()
            print('gm on')
            time.sleep(0.3)
            if not gm_switch:
                pass
        else:
            gm.device_close()
            time.sleep(0.3)
            pass'''


def loop3():
    while True:
        if press:
            mouse_click(1)
            time.sleep(0.452886)
        if not press:
            print('k')
            pass


if __name__ == '__main__':
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()  # mouse listener on
    threading.Thread(target=keyboard_listener).start()  # keyboard listener on
    # threading.Thread(target=loop2).start()  # gm_switch

    threading.Thread(target=nonstop_detect).start()  # output choice_df_head
    threading.Thread(target=loop1).start()  # autoaim_switch ctrl+alt+w
    # threading.Thread(target=loop3).start()  # press than shot press again stop shotting

    # threading.Thread(target=shot).start()
