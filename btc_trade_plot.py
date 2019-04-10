# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:43:02 2019

@author: lil39
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

df_btc = pd.read_excel("C:/temp/plot_sam/1m-epsilon-activity-1march-22march.xlsx")

BTC_ORANGE    = "#F7931A"
window = 300

# BTC price view limits
x = 1551358800000
y = 3816.5
price= 3816.5
z = 1


data = deque([(x, y)], maxlen=window)
long_points = deque([(x, y)], maxlen=window)
short_points = deque([(x, y)], maxlen=window)
order_list = deque([(x, 3816.5, 0)], maxlen=window)
profit_points = deque([(x,0)], maxlen=window)
total_profit = deque(maxlen=window)


##########################################################
def animate(i):
    global x
    x = df_btc.ix[:, "date"].get(i)
    y = df_btc.ix[:, "close_BMXBTCUSD"].get(i)
    data.append((x, y))
    
    global data_x
    global data_y
    data_x = [j1[0] for j1 in data]
    data_y = [k2[1] for k2 in data]

    # set long short flg and limit
    long_flg = df_btc.ix[:, "LongFlg"].get(i)

    # Check if direction flipped
    if long_flg != df_btc.ix[:, "LongFlg"].get(i-1) and len(data) > 2:
        if long_flg == 1:
            long_points.append( (x, y) )

        
            if len(order_list) > 2:
                profit_points.append((x, (y-max(order_list)[1])*max(order_list)[2]))
            order_list.append( (x, y, 1) )
            
        else:
            short_points.append( (x, y) )
            
            if len(order_list) > 2:
                profit_points.append((x, (y-max(order_list)[1])*max(order_list)[2]))
            order_list.append( (x, y, -1) )
    
    # dynamic profit
    dym_profit = (y-max(order_list)[1])*max(order_list)[2]
    
    # make sure all order points are framed within the current view limit        
    if len(long_points) > 0 and len(short_points) > 0:
        if min(long_points)[0] < min(data)[0]:
            long_points.popleft()
    
        if min(short_points)[0] < min(data)[0]:
            short_points.popleft()
        
        if min(order_list)[0] < min(data)[0]:
            order_list.popleft()
            

    total_profit.append( (x,sum([k2[1] for k2 in profit_points])+dym_profit) )

    # get data for order dot line
    global order_x
    global order_y
    order_x = [j1[0] for j1 in order_list]
    order_y = [k2[1] for k2 in order_list]

    ax[0].relim()
    ax[1].relim()
#    if len(data) < 10:
#        ax[0].set_ylim(3770, 3890)
    ax[0].autoscale_view()
    ax[1].autoscale_view()
    
    line.set_data(data_x, data_y)
    long_order_dot.set_data(*zip(*long_points))
    short_order_dot.set_data(*zip(*short_points))
    order_dot_line.set_data(order_x, order_y)
    total_profit_line.set_data(*zip(*total_profit))
    

######## END OF ANIMAT #############


fig, ax = plt.subplots(2, 1, sharex=True)
fig.subplots_adjust(hspace=0)

line, = ax[0].plot([], [], c=BTC_ORANGE)
long_order_dot, =  ax[0].plot([k1[0] for k1 in long_points], [k2[1] for k2 in long_points], "X", c='green', alpha= 1)
short_order_dot, = ax[0].plot([j1[0] for j1 in short_points], [j2[1] for j2 in short_points], "X", c='red', alpha= 1)
order_dot_line, = ax[0].plot([j1[0] for j1 in order_list], [j2[1] for j2 in order_list], linestyle=':', c='b', alpha= 0.6)

total_profit_line, = ax[1].plot([j1[0] for j1 in total_profit], [j2[1] for j2 in total_profit], c='b', alpha= 1)

ani = animation.FuncAnimation(fig, animate, interval=4)
plt.show()

























