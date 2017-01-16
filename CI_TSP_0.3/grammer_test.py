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

def candidater_generator(candidate_choose_num):
    priority_list = range(location_num)

    for i in range(candidate_choose_num):
        random.shuffle(priority_list)
        trans_list = [priority_list[i] for i in range(len(priority_list))]
        candidate_choose_list.append(trans_list)



candidater_generator(candidate_choose_num)
print "candidate_choose",candidate_choose

