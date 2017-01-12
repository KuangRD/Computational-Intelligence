"""
import matplotlib.pyplot

idat_file = open("berlin52.csv")
idat = idat_file.read()
idat_file.close()

idat_str_list = idat.split("\r\n")

x_location_list = []
y_location_list = []

idat_2d_list =[]
for element in idat_str_list:
    idat_2d_list.append(element.split(","))
idat_2d_list.pop(-1)
#print idat_2d_list


for element in idat_2d_list:
    x_location_list.append(float(element[0]))
    y_location_list.append(float(element[1]))


#for i in range(len(x_location_list)):
    #matplotlib.pyplot.plot(x_location_list[i],y_location_list[i])

matplotlib.pyplot.plot(x_location_list,y_location_list)
matplotlib.pyplot.show()
"""
"""
def candidater_generator(candidate_choose_num):
    priority_list = range(location_num)

    for i in range(candidate_choose_num):
        random.shuffle(priority_list)
        trans_list = [priority_list[i] for i in range(len(priority_list))]
        candidate_choose_list.append(trans_list)



candidater_generator(candidate_choose_num)
print "candidate_choose",candidate_choose
"""
"""
import random

a_list = range(10)
random.shuffle(a_list)
a_list.sort()
print a_list
"""
import math

idat_file = open("berlin52.csv")
idat = idat_file.read()
idat_file.close()

idat_str_list = idat.split("\n")

x_location_list = []
y_location_list = []

idat_2d_list =[]
for element in idat_str_list:
    idat_2d_list.append(element.split(","))
idat_2d_list.pop(-1)

for element in idat_2d_list:
    x_location_list.append(float(element[0]))
    y_location_list.append(float(element[1]))


def sum_distance(a_priority):
    sum_distance = 0.0

    for i in range(1, len(a_priority)):
        sum_distance += math.sqrt(
            math.pow((x_location_list[a_priority[i]] - x_location_list[a_priority[i - 1]]), 2) + math.pow(
                (y_location_list[a_priority[i]] - y_location_list[a_priority[i - 1]]), 2))

    return sum_distance

test_priority = [8, 11, 34, 21, 36, 50, 33, 12, 37, 7, 35, 42, 38, 24, 3, 40, 2, 0, 6, 1, 15, 19, 39, 44, 5, 31, 10, 18, 17, 51, 43, 9, 29, 16, 22, 4, 26, 13, 46, 25, 23, 20, 41, 49, 32, 47, 14, 28, 30, 27, 48, 45]
#26185.3046024
print sum_distance(test_priority
