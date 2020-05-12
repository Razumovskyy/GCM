# -*- coding: utf-8 -*-
"""
Created on Wed May 29 21:07:42 2019
Created by Razumovskiy Mikhail, Infrared Spectroscopy Lab, MIPT.

In this script horizontal wind map on fixed longitude is build up.
WARNING: the grid is not uniform. Number of latitudes is 2 much higher than longitudes.
"""

import numpy as np
import struct
from math import pi
import matplotlib.pyplot as plt
import matplotlib.cm as cm

"""defyning constants of the grid:"""

height_num = 480 #number of nodes in height from the zero level
latitude_num = 768 #number of nodes in latitudes = number of latitudes
aux_height_num = -9 #number of auxilary "negative" nodes in height in order to specify the surface
longitude_num = 384 #number of nodes in longitudes = number of longitudes
height_step = 0.25 #step in height in kilometers
full_height_num = height_num + 2 - aux_height_num #full number of nodes in height
fix_longitude = 2 #fixed current longitude from 2 to 385.

""" reading from .DAT files """

offset = 4*fix_longitude
skipped_bytes = (longitude_num - 1) * 4

def create_velocity_array(array_path='', offset=offset , skipped_bytes=skipped_bytes):
    with open (array_path, 'rb') as V:
        V_array = []
        V.seek(offset)
        while True:
            raw_data = V.read(4)
            if not raw_data:
                break
            struct_data = struct.unpack('f', raw_data)
            V_array.append(struct_data[0])
            V.seek(skipped_bytes, 1)
    V_array = np.array(V_array)
    V_array = V_array.reshape(full_height_num, latitude_num)
    return V_array

""" arrays initializations for meshgrid """

H = np.arange(aux_height_num, height_num + 2) * height_step #length of H is b
S = np.arange(1, latitude_num + 1)
S = pi * (S/latitude_num - 0.5 * (1 + 1/latitude_num))* 180 / pi
H, S = np.meshgrid(H, S) #creating grid
H = np.transpose(H)
S = np.transpose(S)

""" crafting first experiment map"""
Vx_arr1 = [[], []]
Vy_arr1 = [[], []]
Vhoriz_arr1 = [[], []]

Names1_Vx = ['C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/20.03.2019_paper_first_exp_Teq-pole=1/Vx.DAT', 
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/12.04.2019_paper_first_exp_Teq-pole=0.03/Vx.DAT']

Names1_Vy = ['C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/20.03.2019_paper_first_exp_Teq-pole=1/Vy.DAT', 
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/12.04.2019_paper_first_exp_Teq-pole=0.03/Vy.DAT']

#--------averaging over all longitudes-----------------------
j = 2 #starting longitude
for i in range(2):
    Vx_arr1[i] = create_velocity_array(Names1_Vx[i], offset, skipped_bytes)
    Vy_arr1[i] = create_velocity_array(Names1_Vy[i], offset, skipped_bytes)
    D = j * 2 * pi/longitude_num #current longitude angle
    Vhoriz_arr1[i] = Vy_arr1[i]*np.cos(D) - Vx_arr1[i]*np.sin(D)

j += 5
count = 1

while j<386:
    count+=1
    offset = 4*j
    for i in range(2):
        Vx_arr1[i] = create_velocity_array(Names1_Vx[i], offset, skipped_bytes)
        Vy_arr1[i] = create_velocity_array(Names1_Vy[i], offset, skipped_bytes)
        D = j * 2 * pi/longitude_num #current longitude angle
        Vhoriz_arr1[i] += Vy_arr1[i]*np.cos(D) - Vx_arr1[i]*np.sin(D)
    print ('first experiment data processing...', j)
    j+=5
print ('number of longitudes data averaged over:', count)     
Vhoriz_arr1[0] = Vhoriz_arr1[0]/count
Vhoriz_arr1[1] = Vhoriz_arr1[1]/count

#-------plotting the map--------------------------------------    
fig, axs = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
i=0
for ax in axs.ravel():
    im = ax.contourf(S, H, Vhoriz_arr1[i], 60, cmap=cm.jet)
    i+=1
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)
plt.show()

""" crafting second experiment multi-panel map """

Vx_arr2 = [[], [], [], []]
Vy_arr2 = [[], [], [], []]
Vhoriz_arr2 = [[], [], [], []]

Names2_Vx = ['C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/15.04.2019_paper_second_exp_carbon-dioxide/Vx.DAT', 
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/23.04.2019_paper_second_exp_nitrogen/Vx.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/25.04.2019_paper_second_exp_water/Vx.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/29.04.2019_paper_second_exp_8gr-mole/Vx.DAT']

Names2_Vy = ['C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/15.04.2019_paper_second_exp_carbon-dioxide/Vy.DAT', 
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/23.04.2019_paper_second_exp_nitrogen/Vy.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/25.04.2019_paper_second_exp_water/Vy.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/29.04.2019_paper_second_exp_8gr-mole/Vy.DAT']

#--------averaging over all longitudes-----------------------
j = 2 #starting longitude
offset = 4 * j
for i in range(4):
    Vx_arr2[i] = create_velocity_array(Names2_Vx[i], offset, skipped_bytes)
    Vy_arr2[i] = create_velocity_array(Names2_Vy[i], offset, skipped_bytes)
    D = j * 2 * pi/longitude_num #current longitude angle
    Vhoriz_arr2[i] = Vy_arr2[i]*np.cos(D) - Vx_arr2[i]*np.sin(D)

j += 5
count = 1

while j<386:
    count+=1
    offset = 4*j
    for i in range(4):
        Vx_arr2[i] = create_velocity_array(Names2_Vx[i], offset, skipped_bytes)
        Vy_arr2[i] = create_velocity_array(Names2_Vy[i], offset, skipped_bytes)
        D = j * 2 * pi/longitude_num #current longitude angle
        Vhoriz_arr2[i] += Vy_arr2[i] * np.cos(D) - Vx_arr2[i] * np.sin(D)
    print ('second experiment data processing...', j)
    j+=5

print ('number of longitudes data averaged over:', count)     
Vhoriz_arr2[0] = Vhoriz_arr2[0]/count
Vhoriz_arr2[1] = Vhoriz_arr2[1]/count
Vhoriz_arr2[2] = Vhoriz_arr2[2]/count
Vhoriz_arr2[3] = Vhoriz_arr2[3]/count

fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
i=0
for ax in axs.ravel():
    im = ax.contourf(S, H, Vhoriz_arr2[i], 60, cmap=cm.jet)
    i+=1
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)
plt.show()

""" crafting third experiment multi-panel map """

Vx_arr3 = [[], [], [], []]
Vy_arr3 = [[], [], [], []]
Vhoriz_arr3 = [[], [], [], []]

Names3_Vx = ['C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/09.06.2019_third_experiment_tidal-lock_carbon-dioxide/Vx.DAT', 
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/13.06.2019_third_experiment_tidal-lock_nitrogen/Vx.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/14.06.2019_third_experiment_tidal-lock_aqua/Vx.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/19.06.2019_third_experiment_tidal-lock_8gr-mole/Vx.DAT']

Names3_Vy = ['C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/09.06.2019_third_experiment_tidal-lock_carbon-dioxide/Vy.DAT', 
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda//13.06.2019_third_experiment_tidal-lock_nitrogen/Vy.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/14.06.2019_third_experiment_tidal-lock_aqua/Vy.DAT',
             'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/19.06.2019_third_experiment_tidal-lock_8gr-mole/Vy.DAT']

#--------averaging over all longitudes-----------------------
j = 2
offset = 4 * j
for i in range(4):
    Vx_arr3[i] = create_velocity_array(Names3_Vx[i], offset, skipped_bytes)
    Vy_arr3[i] = create_velocity_array(Names3_Vy[i], offset, skipped_bytes)
    D = j * 2 * pi/longitude_num #current longitude angle
    Vhoriz_arr3[i] = Vy_arr3[i]*np.cos(D) - Vx_arr3[i]*np.sin(D)

j += 5
count = 1

while (j<380):
    if (j == 3) or (j == 30) or (j == 32) or (j == 131) or (j == 256) or (j == 259) or (j == 277) or (j == 286) or (j == 288):
        j+=5
    count+=1
    offset = 4 * j
    for i in range(4):
        Vx_arr3[i] = create_velocity_array(Names3_Vx[i], offset, skipped_bytes)
        Vy_arr3[i] = create_velocity_array(Names3_Vy[i], offset, skipped_bytes)
        D = j * 2 * pi/longitude_num #current longitude angle
        Vhoriz_arr3[i] += Vy_arr3[i] * np.cos(D) - Vx_arr3[i] * np.sin(D)
    print ('third experiment data processing...', j)
    j += 5

print ('number of longitudes data averaged over:', count)      
Vhoriz_arr3[0] = Vhoriz_arr3[0]/count
Vhoriz_arr3[1] = Vhoriz_arr3[1]/count
Vhoriz_arr3[2] = Vhoriz_arr3[2]/count
Vhoriz_arr3[3] = Vhoriz_arr3[3]/count

fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
i=0
for ax in axs.ravel():
    im = ax.contourf(S, H, Vhoriz_arr3[i], 60, cmap=cm.jet)
    i+=1
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)
plt.show()



    
        
        
          