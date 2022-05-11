import time
import pyautogui
import cv2
import numpy as np
import datetime
import win32api
import win32con

import find_box
import log_message
import role_loc
import role_move
import send_message



#丢图藏宝图坐标
clear_map_area = [1698, 158, 52, 27]
# 获取绝对坐标二值化参数
loc_threshold_param = 230

#走廊脚下可开盒子区域
box_under_footer_area_passageway = [710, 580, 10, 10]

#走廊挖宝坐标方向和大小
begin_find_loc_passageway1 = [-794, -720]
begin_find_loc_passageway2 = [-793, -681]
begin_find_direct_passageway1 = -0.48
begin_find_direct_passageway2 = -0.50
find_area_passageway1 = [0,39]
find_area_passageway2 = [0,24]


gold = cv2.imread('img/gold.png')


def prepare_to_find():
    count = 0
    role_move.move_to([-779, -701])
    role_move.move_to([-793, -703])
    role_move.move_to(begin_find_loc_passageway1, None, 1, 5)
    role_move.turn_to(begin_find_direct_passageway1)
    count += role_move.move_map(find_area_passageway1[0], find_area_passageway1[1], find_box.find_box_under_footer)
    role_move.move_to(begin_find_loc_passageway2, None, 1, 5)
    role_move.turn_to(begin_find_direct_passageway2)
    count += role_move.move_map(find_area_passageway2[0], find_area_passageway2[1], find_box.find_box_under_footer)
    role_move.move_to([-795, -655])

time.sleep(0.5)
    
prepare_to_find()


