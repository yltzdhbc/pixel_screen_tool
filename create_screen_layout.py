import numpy as np
import cv2

PARTITION_SEZE = 50

TOTAL_LED_NUM = 1216
ring_num = [120, 115, 105, 102, 92, 90, 80, 78,
            70, 65, 57, 52, 45, 40, 32, 27, 19, 15, 8, 4]
ring_r = [146, 139.5, 130.5, 124.5, 115.5, 109.5, 100.5, 94.5, 85.5,
          79.5, 70.5, 64.5, 55.5, 49.5, 40.5, 34.5, 25.5, 20.24, 10.5, 5.5]
ring_num_sum = {}
arr5 = np.array([0, 0])

x_buff = [0 for x in range(TOTAL_LED_NUM)]
y_buff = [0 for x in range(TOTAL_LED_NUM)]

res = []

led_i_to_martix_id = np.zeros((TOTAL_LED_NUM, 2), dtype=int)
latest_ledbuff = [0 for x in range(TOTAL_LED_NUM)]
led_xy_buff = np.zeros((TOTAL_LED_NUM, 2), dtype=float)

Xori = -146
yori = 146
L = 146*2/PARTITION_SEZE
print("L", L)


def search_calum(led_x, led_y, led_i):
    for j in range(PARTITION_SEZE):
        for i in range(PARTITION_SEZE):
            x1 = Xori + L * i
            y1 = yori - L*j
            x2 = x1 + L
            y2 = y1 - L
            # for led_iin range(TOTA_L_LED_NUM):
            if led_x >= x1 and led_x <= x2 and led_y >= y2 and led_y <= y1:
                # print("i.%d,j:%d,x1:%.2f,y1:%.2f,x2:%.2f,y2:%.2f” % (ij,×1,y1,x2,y2))
                led_i_to_martix_id[led_i][0] = j
                led_i_to_martix_id[led_i][1] = i

def calctmp(i, dijitiaohuan):
    # print("dijitiaohuan:",dijitiaohuan)
    tmp_r = ring_r[dijitiaohuan]
    # print("tmp_r",tmp_r)
    tmp_num = ring_num[dijitiaohuan]
    # print("tmp_num:", tmp_num)
    # print("ring_num_sum[dijitiaohuan]:",ring_num_sum[dijitiaohuan])
    reltive_id = i - ring_num_sum[dijitiaohuan]
    # print("reltive_id:",reltive_id)
    theta_div = 360.0 / tmp_num
    # print("theta_div:", theta_div)
    tmp_theta = 270 - theta_div * reltive_id
    # print("tmp_theta1:",tmp_theta)
    if tmp_theta < 0:
        tmp_theta = tmp_theta + 360
    # print("tmp_theta2:", tmp_theta)
    return tmp_r, tmp_theta

def find_pos():
    for i in range(0, 21):
        ring_num_sum[i] = sum(ring_num[:(i)])

    print(ring_num_sum)
    # print(ring_num_sum[0])
    # print(ring_num_sum[1])

    for id in range(TOTAL_LED_NUM):
        # print("                           id:",id)
        if id >= ring_num_sum[0] and id < ring_num_sum[1]:
            tmp_r, tmp_theta = calctmp(id, 0)
        elif id >= ring_num_sum[1] and id < ring_num_sum[2]:
            tmp_r, tmp_theta = calctmp(id, 1)
        elif id >= ring_num_sum[2] and id < ring_num_sum[3]:
            tmp_r, tmp_theta = calctmp(id, 2)
        elif id >= ring_num_sum[3] and id < ring_num_sum[4]:
            tmp_r, tmp_theta = calctmp(id, 3)
        elif id >= ring_num_sum[4] and id < ring_num_sum[5]:
            tmp_r, tmp_theta = calctmp(id, 4)
        elif id > ring_num_sum[5] and id < ring_num_sum[6]:
            tmp_r, tmp_theta = calctmp(id, 5)
        elif id >= ring_num_sum[6] and id < ring_num_sum[7]:
            tmp_r, tmp_theta = calctmp(id, 6)
        elif id >= ring_num_sum[7] and id < ring_num_sum[8]:
            tmp_r, tmp_theta = calctmp(id, 7)
        elif id >= ring_num_sum[8] and id < ring_num_sum[9]:
            tmp_r, tmp_theta = calctmp(id, 8)
        elif id >= ring_num_sum[9] and id < ring_num_sum[10]:
            tmp_r, tmp_theta = calctmp(id, 9)
        elif id >= ring_num_sum[10] and id < ring_num_sum[11]:
            tmp_r, tmp_theta = calctmp(id, 10)
        elif id >= ring_num_sum[11] and id < ring_num_sum[12]:
            tmp_r, tmp_theta = calctmp(id, 11)
        elif id >= ring_num_sum[12] and id < ring_num_sum[13]:
            tmp_r, tmp_theta = calctmp(id, 12)
        elif id >= ring_num_sum[13] and id < ring_num_sum[14]:
            tmp_r, tmp_theta = calctmp(id, 13)
        elif id >= ring_num_sum[14] and id < ring_num_sum[15]:
            tmp_r, tmp_theta = calctmp(id, 14)
        elif id >= ring_num_sum[15] and id < ring_num_sum[16]:
            tmp_r, tmp_theta = calctmp(id, 15)
        elif id >= ring_num_sum[16] and id < ring_num_sum[17]:
            tmp_r, tmp_theta = calctmp(id, 16)
        elif id >= ring_num_sum[17] and id < ring_num_sum[18]:
            tmp_r, tmp_theta = calctmp(id, 17)
        elif id > ring_num_sum[18] and id < ring_num_sum[19]:
            tmp_r, tmp_theta = calctmp(id, 18)
        elif id >= ring_num_sum[19] and id < ring_num_sum[20]:
            tmp_r, tmp_theta = calctmp(id, 19)

        r = np.array([tmp_r], np.float32)
        theta = np.array([tmp_theta], np.float32)
        x, y = cv2.polarToCart(r, theta, angleInDegrees=True)
        xy = np.append(x, y)
        # print(xy)
        x_buff[id] = xy[0]
        y_buff[id] = xy[1]
        led_xy_buff[id][0] = xy[0]
        led_xy_buff[id][1] = xy[1]
        search_calum(xy[0], xy[1], id)


# 生成图形，保存数组
find_pos()
# np.save("x_buff.npy",x_buff)
# np.save("y_buff.npy",y_buff)

np.save("ring_pixel_layout.npy",led_xy_buff)
