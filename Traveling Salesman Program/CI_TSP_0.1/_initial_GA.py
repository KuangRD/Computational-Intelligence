import math

x_location_list = []
y_location_list = []

a = 0.0
for i in range(10):
    a = a + 1.0
    x_location_list.append(a)
    y_location_list.append(a)

ad = [i for i in range(10)]

def sum_distance(a_priority):
    sum_distance = 0.0

    for i in range(1, len(a_priority)):
        sum_distance += math.sqrt(
            math.pow((x_location_list[a_priority[i]] - x_location_list[a_priority[i - 1]]), 2) + math.pow(
                (y_location_list[a_priority[i]] - y_location_list[a_priority[i - 1]]), 2))

    return sum_distance