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
j = 32
""" reading from .DAT files """

offset = 4 * j
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


D = j * 2 * pi/longitude_num

Name_x = 'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/14.06.2019_third_experiment_tidal-lock_aqua/Vx.DAT'
Name_y = 'C:/Users/Пользователь/Documents/GCM Modelling/venus-cuda/14.06.2019_third_experiment_tidal-lock_aqua/Vy.DAT'

Vx_arr = create_velocity_array(Name_x, offset, skipped_bytes)
Vy_arr = create_velocity_array(Name_y, offset, skipped_bytes)
Vhoriz_arr = Vy_arr * np.cos(D) - Vx_arr * np.sin(D)
fig, ax = plt.subplots()
im = ax.contourf(S, H, Vhoriz_arr, 60, cmap=cm.jet)
fig.colorbar(im)
ax.set_title ('j=%i' %j)
plt.show()