import torch
import win32gui
from PIL import ImageGrab
import pynput
import pandas
from ctypes import CDLL
import time
import threading

csgo_handle = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
model = torch.hub.load(r'D:\AIII\test\yolov5-master(original)\yolov5-master', 'custom',
                       path=r'D:\AIII\test\yolov5-master(original)\yolov5-master\runs\train\354exp9\weights\best'
                            r'.engine',
                       source='local')  # tenorrt model
model.conf = 0.7
press = False
gm = CDLL('ghub_device.dll')
gm.device_open()
zero_object_times = 0
t = time.time()
click_times = 0


def key_down(key=''):
    gm.key_down(key.encode('utf-8'))


def key_up(key=''):
    gm.key_up(key.encode('utf-8'))


def mouse_move(x, y, abs_move=False):
    gm.moveR(x, y, abs_move)  # int only


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


aim_x = 0
aim_y = 0


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
        global aim_x
        global aim_y
        aim_x = int((xmin + xmax) / 2)
        aim_y = int((ymin + ymax) / 2)
    return aim_x, aim_y


def on_click(x, y, button, pressed):
    global press
    if pressed and button == button.x1:
        press = not press
        print('True' if press else 'False')


'''def lock():
    x = autoaim(df_head)[0]
    y = autoaim(df_head)[1]
    a = 2.5
    mouse_move(int((x - 1920 / 2) * a), int((y - 1080 / 2) * a))
    gm.mouse_down(1)
    time.sleep(0.0001)
    gm.mouse_up(1)'''


def aim():
    global click_times
    while 1:
        df_head = pandas.DataFrame()
        fullscreen = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        dataframe = inference(model, fullscreen, 1056)
        if press:
            if dataframe.empty:
                zero_object_times += 1
                print('{}, total leisure time {}'.format(zero_object_times, (time.time() - t)))
                key_down(key='l')
            if not dataframe.empty:
                key_up(key='l')
                df_head = df_head.append(dataframe[dataframe['class'] == 1], ignore_index=True)
                # print(df_head)
                a = 2.5
                mouse_move(int((autoaim(df_head)[0] - 1920 / 2) * a), int((autoaim(df_head)[1] - 1080 / 2) * a))
                click_times += 1
                time.sleep(0.001)
                t = time.time()
                zero_object_times = 0
        if not press:
            t = time.time()
            zero_object_times = 0
            key_up(key='l')
            pass


def loop3():
    while True:
        if press:
            gm.mouse_down(1)
            time.sleep(0.001)
            gm.mouse_up(1)
            time.sleep(0.452886)
        if not press:
            pass


if __name__ == '__main__':
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()
    threading.Thread(target=aim).start()
    threading.Thread(target=loop3).start()
