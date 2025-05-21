# Exercise 1

"""
for num in range(51, 100, 2):
    print(num)
"""
# Exercise 2


for num in range(1500, 2701):
    if num % 7 == 0 and num % 5 == 0 :
        print(num) 

# Exercise 3

"""
for num in range(21):
    if num == 16 or num == 3 :
        continue 
    print (num)
"""
# Exercise 4

"""
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
so_chan = 0
so_le = 0
for number in numbers:
    if number % 2 == 0: 
        so_chan += 1
    else:  
        so_le += 1
print("So so chan la: ",so_chan)
print("So so le la: ",so_le)
"""
# Exercises 5 

"""
m = 0 
for i in range (1,100):
    m += i / (i + 1)
print (m) 
"""
# Exercises 6 

"""
import numpy as np
mang = np.arange(12, 39)  
print(mang)
""" 
# Exercises 7 

""" 
import numpy as np
mang1 = np.array([1, 2, 3, 4, 5, 6])
mang2 = np.array([4, 5, 6, 7, 8, 9])
gia_tri_chung = np.intersect1d(mang1, mang2)
print("Các giá trị chung giữa hai mảng là:", gia_tri_chung)
"""