import time
import numpy as np
import pyautogui
import cv2
import role_loc
import role_action
import role_move
import math


open_map_error = cv2.imread('img/open_map_error.png')
gold = cv2.imread('img/gold.png')
gold_800 = cv2.imread('img/gold_800.png')




time.sleep(0.5)
# role_action.reset_to_store()
role_action.clear_map()
# role_action.buy_map()


