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

map_in_store = cv2.imread('img/map_in_store.png')
open_map_btn = cv2.imread('img/open_map.png')
map_title = cv2.imread('img/map_title.png')
buy_map_tip = cv2.imread('img/buy_map_tip.png')
confirm_btn = cv2.imread('img/confirm_btn.png')
bag_left = cv2.imread('img/bag_left.png')
store_npc = cv2.imread('img/store_npc.png')
open_map_error = cv2.imread('img/open_map_error.png')
home_door_btn = cv2.imread('img/home_door_btn.png')
home_main_btn = cv2.imread('img/home_main_btn.png')
back_origin_btn = cv2.imread('img/back_origin_btn.png')
new_day_tip = cv2.imread('img/new_day_tip.png')
close_btn = cv2.imread('img/close_btn.png')
horse = cv2.imread('img/horse.png')
isdead = cv2.imread('img/isdead.png')


# 点开藏宝地图模式位置
open_box_map_pos = [537, 51]

# 要丢掉的首张图位值
first_map_pos = [1750, 350]

# 确定按钮位置
confirm_pos = [880, 450]

# 打开藏宝图等待时间（当前等级）
wait_open_time1 = 131
# 打开藏宝图等待时间（50张）
wait_open_time2 = 163
# 藏宝图探查吟唱时间减少
decreased_percent = 0.4

# 开始挖宝的坐标方向和大小
begin_find_loc_1 = [-825, -540]
begin_find_direct_1 = 0.6
find_area_1 = [65, 42]

# 挖宝区域大小
begin_find_loc_2 = [-975, -525]
begin_find_direct_2 = -0.5
find_area_2 = [61, 34]

# 背包格子大小
bag_item_size = 36
bag_width = 12

# 家园走到门口的位移距离
home_to_door = [-4, -1]

# 复活至龙星阵的具体坐标
resurrect_loc = [970,800]


def match_img(template):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val, max_loc


def clear_map():
    pyautogui.press('m')
    time.sleep(0.5)
    max_val, max_loc = match_img(map_title)
    #print(max_val)
    if max_val < 0.95:
        pyautogui.moveTo(open_box_map_pos[0], open_box_map_pos[1])
        pyautogui.leftClick()
    #time.sleep(0.1)    
    count = role_loc.get_clear_map_count()
    print('丢图数量 = '+str(count))
    for i in range(0, count):
        pyautogui.moveTo(first_map_pos[0], first_map_pos[1])
        pyautogui.rightClick()
        pyautogui.moveTo(first_map_pos[0] + 50, first_map_pos[1] + 30)
        pyautogui.leftClick()
        pyautogui.press('enter')
        # pyautogui.moveTo(confirm_pos[0], confirm_pos[1])
        # pyautogui.leftClick()
    pyautogui.moveTo(first_map_pos[0] - 50, first_map_pos[1] - 50)
    pyautogui.leftClick()
    pyautogui.press('m')
    max_val, max_loc = match_img(isdead)
    if max_val > 0.95:
        time.sleep(15)
        print("isdead的max_val = " + str(max_val))
        resurrect()
    return count


def buy_map():
    max_val = 0
    for i in range(0, 10):
        time.sleep(0.2)
        max_val, max_loc = match_img(store_npc)
        # print(max_val)
        if max_val > 0.9:
            break
        role_move.move_to([-803, -721])
        role_move.move_to([-803, -716], None, 1)
    if max_val <= 0.9:
        send_message_with_loc("Find Map NPC Error")
        return False
    pyautogui.press('f')
    time.sleep(0.5)
    max_val, max_loc = match_img(map_in_store)
    if max_val <= 0.9:
        send_message_with_loc("Open Map Store Error")
        return False
    clear_bag()
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.keyDown('shift')
    pyautogui.rightClick()
    pyautogui.keyUp('shift')
    max_val, max_loc = match_img(buy_map_tip)
    if max_val > 0.9:
        pyautogui.press('4')
        pyautogui.press('1')
        pyautogui.press('enter')
        pyautogui.click(x=None, y=None, clicks=9, interval=0.001, button='right', duration=0.0, tween=pyautogui.linear)
        # max_val, max_loc = match_img(confirm_btn)
        # if max_val > 0.9:
        #     pyautogui.moveTo(max_loc[0] + 50, max_loc[1] + 15)
        #     pyautogui.leftClick()
    time.sleep(0.5)
    return True


def open_map():
    role_move.move_to([-802, -703])
    role_move.move_to([-791, -702])
    role_move.move_to([-777, -701])
    role_move.move_to([-756, -703], None, 0, 5)
    max_val, max_loc = match_img(open_map_btn)
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    down_horse()
    pyautogui.leftClick()
    pyautogui.sleep(1)
    max_val, max_loc = match_img(open_map_error)
    open_map_count = 0
    if max_val < 0.9:
        pyautogui.press('m')
        time.sleep(0.5)
        max_val, max_loc = match_img(map_title)
        #print(max_val)
        if max_val < 0.95:
            pyautogui.moveTo(open_box_map_pos[0], open_box_map_pos[1])
            pyautogui.leftClick()   
        open_map_count = role_loc.get_clear_map_count()
        pyautogui.press('m')
        print('开图数量 = '+str(open_map_count))
        wait_open_time = 5*(1-decreased_percent)*open_map_count-1
        #print('开图时间 = '+str(wait_open_time))
        pyautogui.sleep(wait_open_time)
        pyautogui.moveRel(0, -100) 
        up_horse()    
        return open_map_count
    else:
        close_dialog()
        up_horse()
        send_message_with_loc("Open Map Error")
        return False
    

def down_horse():
    if not is_on_horse():
        return
    pyautogui.press('t')
    pyautogui.press('shift')
    pyautogui.sleep(3)


def up_horse():
    if is_on_horse():
        return
    pyautogui.press('t')
    pyautogui.sleep(3)


def close_dialog():
    max_val, max_loc = match_img(close_btn)
    if max_val > 0.9:
        pyautogui.moveTo(max_loc[0] + 6, max_loc[1] + 6)
        pyautogui.leftClick()


def prepare_to_find():
    role_move.move_to([-779, -701])
    role_move.move_to([-793, -703])
    role_move.move_to([-793, -677])
    role_move.move_to([-795, -666])
    role_move.move_to([-795, -640])
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    loc = role_loc.get_current_loc()
    if loc is not None and abs(loc[0] - begin_find_loc_1[0]) < 5 and abs(loc[1] - begin_find_loc_1[1]) < 5:
        return True
    else:
        send_message_with_loc("Go to Find Box Error")
        return False


def find_boxs():
    count = 0
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    count += role_move.move_map(find_area_1[0], find_area_1[1], find_box.find_box_under_footer)
    role_move.move_to(begin_find_loc_2, None, 1, 5)
    role_move.turn_to(begin_find_direct_2)
    count += role_move.move_map(find_area_2[0], find_area_2[1], find_box.find_box_under_footer)
    role_move.move_to([-850, -560], None, 5, 3)
    print("开盒次数" + str(count))
    if count <= 0:
        reset_keys()
        send_message_with_loc("Find No Box")
    max_val, max_loc = match_img(isdead)
    if max_val > 0.95:
        time.sleep(15)
        print("isdead的max_val = " + str(max_val))
        resurrect()
    return count


def back_to_store():
    role_move.move_to([-795, -644])
    role_move.move_to([-795, -667])
    role_move.move_to([-795, -702])
    role_move.move_to([-802, -702])
    role_move.move_to([-803, -721])
    role_move.move_to([-803, -716], None, 0, 5)
    loc = role_loc.get_current_loc()
    if loc is not None and abs(-803 - loc[0]) < 5 and abs(-716 - loc[1]) < 5:
        return True
    else:
        send_message_with_loc("Back To Store Error")
        return False


def clear_bag():
    max_val, max_loc = match_img(bag_left)
    if max_val < 0.9:
        return
    first_loc = [max_loc[0] + 100, max_loc[1] - 90]
    pyautogui.keyDown('shift')
    for j in range(0, 4):
        for i in range(0, bag_width):
            pyautogui.moveTo(first_loc[0] + i * bag_item_size, first_loc[1] + j * bag_item_size)
            pyautogui.rightClick()
    # for i in range(0, 10):
    #     pyautogui.moveTo(first_loc[0] + i * bag_item_size, first_loc[1] + 3 * bag_item_size + 25)
    #     pyautogui.rightClick()
    pyautogui.keyUp('shift')


def reset_to_store():
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    # 处理在商店附近情况
    if abs(-803 - current_loc[0]) < 5 and abs(-716 - current_loc[1]) < 5:
        role_move.move_to([-803, -721])
    down_horse()
    max_val, max_loc = match_img(home_door_btn)
    if max_val < 0.9:
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.leftClick()
    pyautogui.sleep(5)
    pyautogui.press('f')
    pyautogui.moveRel(-100, -100)
    time.sleep(1)

    max_val, max_loc = match_img(home_main_btn)
    if max_val < 0.9:
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 30, max_loc[1] + 15)
    pyautogui.leftClick()
    pyautogui.sleep(30)

    role_move.move(home_to_door[0], home_to_door[1])
    pyautogui.press('f')
    time.sleep(1)
    max_val, max_loc = match_img(back_origin_btn)
    if max_val < 0.9:
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 30, max_loc[1] + 15)
    pyautogui.leftClick()
    pyautogui.sleep(60)

    reset_visual_field()

    loc = role_loc.get_current_loc()
    up_horse()
    if loc is not None and abs(-803 - loc[0]) < 5 and abs(-715 - loc[1]) < 5:
        return True
    return False


def reset_keys():
    pyautogui.keyDown('shift')
    pyautogui.keyUp('shift')
    pyautogui.sleep(2)
    pyautogui.moveTo(find_box.footer_pos[0], find_box.footer_pos[1])
    pyautogui.sleep(2)
    pyautogui.mouseDown(button='left')
    pyautogui.sleep(2)
    pyautogui.mouseUp(button='left')
    pyautogui.sleep(2)
    pyautogui.mouseDown(button='right')
    pyautogui.sleep(2)
    pyautogui.mouseUp(button='right')
    pyautogui.sleep(2)


def try_reset():
    if not deal_new_day():
        return
    count = 0
    while not reset_to_store():
        count += 1
        send_message_with_loc("Try reset count " + str(count))
        role_move.move(-10, -10)
        time.sleep(600)
        if not deal_new_day():
            return


def deal_new_day():
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        # 关服了
        return False
    max_val, max_loc = match_img(new_day_tip)
    if max_val > 0.9:
        close_dialog()
    return True


def is_on_horse():
    max_val, max_loc = match_img(horse)
    return max_val > 0.9


def reset_visual_field():
    reset_look_down()

    x, y = 1000, 700
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.1)
    for i in range(0, 3):
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -100)
        time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)


def reset_look_down():
    x, y = 1000, 120
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.1)
    for i in range(0, 9):
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 100)
        time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)


def send_message_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    send_message.send_message(message + " " + str(loc) + " " + str(direct))


def print_log_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    log_message.log_error(message + " " + str(loc) + " " + str(direct))
    
    
def send_message_briefing(message:list,index = 0):
    send_text = '简报第{0}次：'.format(index)+'\n'
    for index,key in enumerate(message):
        send_text = send_text+str(key)+':'+str(message[key])+'\n'
    send_message.send_message(send_text)
    
def resurrect(count = 3):
    for i in range(0,count):
        pyautogui.moveTo(resurrect_loc[0],resurrect_loc[1])
        pyautogui.leftClick()
        time.sleep(3)
        max_val, max_loc = match_img(isdead)
        if max_val < 0.95:
            print("复活后的max_val = " + str(max_val))
            break
    reset_to_store()
    send_message.send_message()("try to resurrect" + i + "次")