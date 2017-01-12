"""
Add a distance matrix to accelerate sum_distance calculation iteration
"""
import math

"""
File Read
"""
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

"""
build up distance matrix
"""
def p2p_distance(a,b):
    return math.sqrt(math.pow((x_location_list[a] - x_location_list[b]), 2) + math.pow((y_location_list[a] - y_location_list[b]), 2))

distance_matrix = []
length = len(x_location_list)
for row in range(length):
    row_distance = []
    for col in range(length):
        row_distance.append(p2p_distance(row,col))
    distance_matrix.append(row_distance)
"""
calculate the sum distance of a possible choose
"""
def sum_distance(a_priority):
    sum_distance = 0.0

    for i in range(1, len(a_priority)):
        a = a_priority[i]
        b = a_priority[i-1]
        sum_distance += distance_matrix[a][b]
    return sum_distance

test_priority = [8, 11, 34, 21, 36, 50, 33, 12, 37, 7, 35, 42, 38, 24, 3, 40, 2, 0, 6, 1, 15, 19, 39, 44, 5, 31, 10, 18, 17, 51, 43, 9, 29, 16, 22, 4, 26, 13, 46, 25, 23, 20, 41, 49, 32, 47, 14, 28, 30, 27, 48, 45]
#26185.3046024
print sum_distance(test_priority)