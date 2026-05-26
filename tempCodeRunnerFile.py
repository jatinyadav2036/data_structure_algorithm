# nums = [3,1,4,1,5,9,2]
# print(sorted(nums, key=lambda x: -x))

# with open('notes.txt', 'w') as f:
#     f.write('Hello Python!\n')
#     f.write('File Handling is easy.\n')

# with open('notes.txt', 'r') as f:
#     content = f.read() # Read all at once
#     print(content)

# with open('notes.txt', 'r') as f:
#     line = f.readline() # Read one line at a time
#     print(line)

# with open('notes.txt', 'r') as f:
#     lines = f.readlines() # Returns list of all lines
#     for l in lines:
#         print(l.strip())

# with open('notes.txt', 'a') as f:
#     f.write('Appended line\n')

# import os
# if os.path.exists('notes.txt'):
#     # os.remove('notes.txt')
#     print("Path exists")

# import csv
# with open('data.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Name', 'Score'])
#     writer.writerow(['Alice', 95])

# with open('data.csv', 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)

import numpy as np
# rr = np.random.rand(3, 4) # 3x4 uniform random [0,1)
# rn = np.random.randn(3, 4) # 3x4 standard normal (mean=0, std=1)
# ri = np.random.randint(1, 10, (3,3)) # 3x3 random integers 1-9
# print(ri)
# T = np.array([[[1,2],[3,4]],
# [[5,6],[7,8]]],dtype="int64")
# # print(T.shape)
# a = T.reshape(4,2)
# print(a)
# a[1][1] = 100
# print(T)

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# axis=0: Arrays are stacked as "layers"
stacked = np.stack((arr1, arr2), axis=0)
# Result: [[[1, 2], [3, 4]], 
#          [[5, 6], [7, 8]]] (Shape: 2, 2, 2)
print(stacked)