import time

import pytesseract
import cv2
from PIL import Image
import numpy as np
import imutils
import math
import re
import pyautogui
import role_move

# 获取绝对坐标的屏幕位置
current_loc_area = [1810, 30, 110, 30]
# 获取绝对坐标二值化参数
loc_threshold_param = 220

# 小地图的屏幕位置
small_map_area = [1650, 60, 250, 240]
# 小地图箭头颜色范围
arrow_color_high = [120, 255, 255]
arrow_color_low = [20, 140, 190]
# 小地图箭头区域大小
arrow_area_max = 500
arrow_area_min = 200
#丢图藏宝图坐标
clear_map_area = [1698, 158, 52, 27]
# 获取丢图计数二值化参数
clear_map_count_param = 230

re_cmp = re.compile('-?[1-9]\d*')


def get_clear_map_count(try_times=5):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=clear_map_area)), cv2.COLOR_RGB2GRAY)
    cv2.imshow("截屏",image)
    cv2.waitKey(0)
    ret, binary = cv2.threshold(image, clear_map_count_param, 255, cv2.THRESH_BINARY)
    cv2.bitwise_not(binary)
    cv2.imshow("截屏", binary)
    cv2.waitKey(0)
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    text = text.replace('B', '8')
    #print(f'位置：{text}')
    count_str = re_cmp.findall(text)
    if count_str == []:
        clear_map_count = int(50)
    else:
        clear_map_count = int(count_str[0])

    print(count_str)
    print(str(clear_map_count))
    return clear_map_count

time.sleep(0.5)
get_clear_map_count()