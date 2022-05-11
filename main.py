import datetime
import time

import role_action

time.sleep(3)

# role_action.buy_map()
# role_action.open_map()
# role_action.prepare_to_find()
# role_action.find_boxs()
# role_action.clear_map()
# role_action.back_to_store()

for i in range(0, 100):
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        break
    elif current_time.hour == 5 and current_time.minute > 45:
        if current_time.isoweekday() == 4:  # 周四退出
            break
        time.sleep(16 * 60)  # 等到六点
        role_action.close_dialog()

    if not role_action.buy_map():
        role_action.try_reset()
        continue
    open_map_count = role_action.open_map()    
    if not open_map_count:
        role_action.try_reset()
        continue
    if not role_action.prepare_to_find():
        role_action.try_reset()
        continue
    open_box_count = role_action.find_boxs()    
    if not open_box_count:
        role_action.try_reset()
        continue
    clear_map_count = role_action.clear_map()    
    if not clear_map_count:
        role_action.try_reset()
        continue
    if not role_action.back_to_store():
        role_action.try_reset()
        continue
    time_now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')     
    report_data = {
        '当前时间':time_now,
        '开图数量':open_map_count,
        '开盒数量':open_box_count,
        '丢图数量':clear_map_count
    }
    role_action.send_message_briefing(report_data,i+1)
    print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " 第" + str(i + 1) + "次")
