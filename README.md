# csgo-aim-yolov5
only can do a nice performence in killing bot

this project is base on yolov5

most of my tests are run in windowed fullscreen csgo

the main1.py in mian directory can work like the video blow

using these commands in game:
```
sv_cheats 1 
weapon_accuracy_nospread 1
weapon_recoil_scale 0
```
>otherwise the speed is too fast for recoil controling

https://user-images.githubusercontent.com/113933967/201880664-0a1f356e-23c6-48ff-83db-2f05dc85fa0b.mp4

compare to human aiming from bilibili-大东彦

https://www.bilibili.com/video/BV1nU4y1G73M


https://user-images.githubusercontent.com/113933967/201891582-8663593a-8e57-41cd-add5-287474d7a382.mp4

the ghub_device.dll is used to control keyboard and mouse by logitech driver, so it works when raw-input on 

***ghub_device.dll require logitech ghub version below 2021.6***

the video above was using a model i trained from 600+ images with 350 epoch

screenshot.py can take a screenshot when press the second mouse side key
>to get image to label

roboflow is my labeling workspace
https://universe.roboflow.com/lz-k-eigsu/csgo-ql8ba
now it got almost 1000 pictures

training model use yolov5s

- main1.py will auto aim and shot if mouse side botton pressed, and press again can stop

- main2.py is my attempt to realize full auto afk in deathmatch (failed)
>i throught locate enemies by voice, but this is far beyound my capacity, using +left instaed

>in game command ```bind "l" "+left"```

- main3.py trying to use threads to sperate detect&aim function and mouse auto-click funtion with hotkeys (pynput's keyboard and mouse listener may conflict, fail)

>there's a problem when i using threading in mouse control func

>the mouse control thread is a loop, and when i add a time.sleep(0.1) into it, it will work normally

>but when change the time of sleep less than 0.1, the mouse will flow about

>when i delet time.sleep(), it will randomly move to two pole very quick

>still unsloved

- main4.py let detect work from beginning to the end, using hotkey to control autoaim switch and +left

install requirment just the same like yolov5 offical tutorial

also need to install cudatoolkit, tensorrt, pynput, 

tensoRT installing follow offical page
https://docs.nvidia.com/deeplearning/tensorrt/quick-start-guide/index.html#install

```
conda install cudatoolkit
pip install pynput
```


the codes isn't very long, they are all less than 200 lines, so i don't have too many things to explain










### some useless info
im a beginner in coding, a noob actuaclly. the learing curve last for about 2 mouthes, from writing a list in python.
so those codes are immatrue obviously, and my english is still bad :rofl:

i do this just because interest, than the interest became some kinds of wild ambition. i was always thinking of how to make this project batter, so i used tensorRT, learned deepsort try to track characters in game. the last thing failed because i can't trans grabed images to a video stream as a input.
https://github.com/mikel-brostrom/Yolov5_StrongSORT_OSNet


millions of thanks to every opensource community

millions of thanks to yolo develpors

millions of thanks to csdn and stack overflow for sloving many weird problems

millions of thanks to my pc

screenshot from my pc when train the last model
![Screenshot 2022-11-15 165919](https://user-images.githubusercontent.com/113933967/201890782-095593d2-f8e2-481e-9f87-191548ad3f32.png)
