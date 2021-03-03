# """
# ------------------------------------------------------------------------------
# Course: CSE 251
# Lesson Week: 03
# File: assignment.py
# Author: Brother Comeau

# Purpose: Video Frame Processing

# Instructions:

# - Follow the instructions found in Canvas for this assignment
# - No other packages or modules are allowed to be used in this assignment.
#   Do not change any of the from and import statements.
# - Only process the given MP4 files for this assignment


# I implemented the code necessary to test the time of creating all the
# new frames for the processed video, all with different amounts of
# logical processors. I changed the create_new_frame function by
# having it accept a tuple, then breaking that tuple up inside
# the function. This allows for p.map() to work. The other code
# I wrote can be found on lines 95-104.

# 5. Made it my own

# Grade: 100%
# ------------------------------------------------------------------------------
# """

# from matplotlib.pylab import plt  # load plot library
# from PIL import Image
# import numpy as np
# import timeit
# import multiprocessing as mp

# # Include cse 251 common Python files
# import os, sys
# sys.path.append(r'C:\Users\matth\OneDrive\Desktop\Winter 2021\CSE251\code')
# from cse251 import *

# # 4 more than the number of cpu's on your computer
# CPU_COUNT = mp.cpu_count() + 4  

# # TODO Your final video need to have 300 processed frames.  However, while you are 
# # testing your code, set this much lower
# FRAME_COUNT = 300

# RED   = 0
# GREEN = 1
# BLUE  = 2


# def create_new_frame(tuple):

#     image_file = tuple[0]
#     green_file = tuple[1]
#     process_file = tuple[2]

#     # this print() statement is there to help see which frame is being processed
#     # print(f'{process_file[-7:-4]}', end=',', flush=True)

#     image_img = Image.open(image_file)
#     green_img = Image.open(green_file)

#     # Make Numpy array
#     np_img = np.array(green_img)

#     # Mask pixels 
#     mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

#     # Create mask image
#     mask_img = Image.fromarray((mask*255).astype(np.uint8))

#     image_new = Image.composite(image_img, green_img, mask_img)
#     image_new.save(process_file)


# # TODO add any functions to need here


# if __name__ == '__main__':
#     # single_file_processing(300)
#     # print('cpu_count() =', cpu_count())

#     all_process_time = timeit.default_timer()
#     log = Log(show_terminal=True)


#     # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
#     #      add results to xaxis_cores and yaxis_times

#     start_time = timeit.default_timer()

#     totalList=[(rf'elephant/image{image_number:03d}.png',rf'green/image{image_number:03d}.png',rf'processed/image{image_number:03d}.png') for image_number in range(1,301)]
#     xaxis_cores=[]
#     yaxis_times=[]
#     for i in range(1,CPU_COUNT+1):
#       start = timeit.default_timer()
#       with mp.Pool(i) as p:
#         p.map(create_new_frame, totalList)
#       xaxis_cores.append(i)
#       yaxis_times.append(timeit.default_timer() - start)
#       log.write(f'Time to process with {i} cores: {yaxis_times[i-1]}')

 

#     print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')

#     log.write(f'Total Time for ALL procesing: {timeit.default_timer() - all_process_time}')

#     # create plot of results and also save it to a PNG file
#     plt.plot(xaxis_cores, yaxis_times, label=f'{FRAME_COUNT}')
    
#     plt.title('CPU Core yaxis_times VS CPUs')
#     plt.xlabel('CPU Cores')
#     plt.ylabel('Seconds')
#     plt.legend(loc='best')

#     plt.tight_layout()
#     plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
#     plt.show()


import threading, queue

q = queue.Queue()

q.put('House')
q.put('tree')
q.put('Farm')
q.put('Truck')

print(f'Size of queue = {q.qsize()}')
print(q.get())

print(f'Size of queue = {q.qsize()}')
print(q.get())