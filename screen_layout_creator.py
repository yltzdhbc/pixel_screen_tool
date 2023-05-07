import numpy as np

TOTAL_LED_NUM = (16*16)
# 单位mm
SCREEN_LEN_X = 150
SCREEN_LEN_Y = 150
LED_NUM_X = 16
LED_NUM_Y = 16

DISTANCE_DIV_NODE_X =  SCREEN_LEN_X / (LED_NUM_X - 1)
DISTANCE_DIV_NODE_Y =  SCREEN_LEN_Y / (LED_NUM_Y - 1)

led_xy_buff = np.zeros((TOTAL_LED_NUM, 2), dtype=float)

def find_pos():
    for id in range(TOTAL_LED_NUM):
        # 每列的第几个
        temp_row_id = id % LED_NUM_Y
        # 第几列
        temp_column_id = int(id / LED_NUM_Y)

        if temp_column_id % 2 == 0: #是 0 2 4 6 8 10 12 14 16 灯珠顺序是从上到下的
            temp_x = - SCREEN_LEN_X / 2 + temp_column_id * DISTANCE_DIV_NODE_X
            temp_y = + SCREEN_LEN_Y / 2 - temp_row_id * DISTANCE_DIV_NODE_Y
        elif temp_column_id % 2 == 1: #是 1 3 5 7 9 11 13 15 灯珠顺序是从下到上的
            temp_x = - SCREEN_LEN_X / 2 + temp_column_id * DISTANCE_DIV_NODE_X
            temp_y = - SCREEN_LEN_Y / 2 + temp_row_id * DISTANCE_DIV_NODE_Y
        
        led_xy_buff[id][0] = temp_x
        led_xy_buff[id][1] = temp_y

# 生成图形，保存数组
find_pos()
np.save("screen_layout_rec16x16.npy",led_xy_buff)
