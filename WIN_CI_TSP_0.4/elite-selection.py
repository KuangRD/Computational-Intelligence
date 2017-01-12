"""
Modified to elite selection
"""

# Parameter
candidate_choose_num = 20
generation_num = 1
mutation_rate = 0.0001


import matplotlib.pyplot as plt
import random
import math

"""
initial
"""
candidate_choose_list = []
trave_list = []
distance_list=[]
location_num = 52

def crossover(a_list, b_list):
    pop_list = [a for a in a_list]
    mum_list = [b for b in b_list]
    #print "pop",pop_list
    #print "mum",mum_list

    cross_part = []
    son_list = []

    idx_list = range(len(pop_list))
    point_a = idx_list.pop(random.choice(idx_list))
    point_b = random.choice(idx_list)

    if point_a > point_b:
        point_a, point_b = point_b, point_a

    #print "point_a", point_a
    #print "point_b", point_b

    for j in range(point_a, point_b + 1):
        cross_part.append(pop_list[j])

    #print "cross_part:", cross_part

    for m in cross_part:
        mum_list.pop(mum_list.index(m))

    #print "mum_list", mum_list

    for k0 in range(point_a):
        son_list.append(mum_list.pop(0))

    for k1 in cross_part:
        son_list.append(k1)

    for k2 in range(len(mum_list)):
        son_list.append(mum_list.pop(0))

    return son_list


def mutation(a_list):
    idx_list = range(len(a_list))
    point_a = idx_list.pop(random.choice(idx_list))
    point_b = random.choice(idx_list)

    a_list[point_a], a_list[point_b] = a_list[point_b], a_list[point_a]

    return a_list


"""
**********************************
[verification] crossover & mutation
**********************************

a_list = range(7)

print "a_list",a_list
print "mutation",mutation(a_list)



random.shuffle(a_list)
list_a = [a_list[i] for i in range(len(a_list))]
random.shuffle(a_list)
list_b = [a_list[i] for i in range(len(a_list))]


print "list_a",list_a
print "list_b",list_b
print crossover(list_a,list_b)
"""


def candidater_generator(candidate_choose_num):
    priority_list = range(location_num)

    for i in range(candidate_choose_num):
        random.shuffle(priority_list)
        trans_list = [priority_list[i] for i in range(len(priority_list))]
        candidate_choose_list.append(trans_list)


"""
*************************************
[verification] candidater_generator
*************************************

candidater_generator(candidate_choose_num)
print "candidate_choose",candidate_choose
"""


def sum_distance(a_priority):
    sum_distance = 0.0

    for i in range(1, len(a_priority)):
        sum_distance += math.sqrt(
            math.pow((x_location_list[a_priority[i]] - x_location_list[a_priority[i - 1]]), 2) + math.pow(
                (y_location_list[a_priority[i]] - y_location_list[a_priority[i - 1]]), 2))

    return sum_distance



#**************************************
#[verification] sum_distance
#**************************************

"""
File read
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


def GA(generation_num):

    mutation_prob_cumu = 0.0
    now_best_distance = 100000000000
    now_best_choice = []

    for generation_idx in range(generation_num):
        #print "Generation",generation_idx
        fitness_list = []
        fitness_list1= []
        fitness_list_origin = []
        selected_list = []

        for candidate_choose in candidate_choose_list:
            fitness_list_origin.append(sum_distance(candidate_choose))
            selected_list.append(candidate_choose)

       # now_best_choice = candidate_choose_list[fitness_list_origin.index(sorted_fitness_list[0])]
        now_best_distance = min(fitness_list_origin)
        # min2nd_choice= candidate_choose_list[fitness_list_origin.index(sorted_fitness_list[1])]

        now_best_choice = candidate_choose_list[fitness_list_origin.index(min(fitness_list_origin))]
        #max_element = max(fitness_list_origin)

        while len(candidate_choose_list) > 0:
            candidate_choose_list.pop()

        assert len(candidate_choose_list) == 0,"candidate_choose_list claear failed, generation %r" % generation_idx

        for idx in range(1,len(selected_list)):
            a = selected_list[idx]
            b = now_best_choice
            c = crossover(a,b)
            candidate_choose_list.append(c)
        candidate_choose_list.append(now_best_choice)
        assert len(candidate_choose_list) == candidate_choose_num,"len candidate_choose_list = %r after [crossover],generation %r"  % (len(candidate_choose_list),generation_idx)

        mutation_prob_cumu += mutation_rate * len(candidate_choose_list) * len(candidate_choose_list[0])
        #print mutation_prob_cumu

        while mutation_prob_cumu >= 10.0:
            #print "mutation actived"
            idx = random.choice(range(10))
            candidate_choose_list[idx] = mutation(candidate_choose_list[idx])
            mutation_prob_cumu =  mutation_prob_cumu-1.0

        for candidate_choose in candidate_choose_list:
            fitness_list1.append(sum_distance(candidate_choose))
        #assert len(candidate_choose_list)==10,"len candidate_choose_list != 10 after [mutation],generation %r" % generation_idx

#        if min(fitness_list1) > min(fitness_list):
#            print "*********************"
#            print fitness_list
#            print fitness_list1
#            print "*********************"


        #print "Generation",generation_idx,"Distance",min(fitness_list1)
        if now_best_distance >min(fitness_list1):

            #print "FL1 len",len(fitness_list1)
            # print "CCL len",len(candidate_choose_list)

            now_best_distance = min(fitness_list1)
            now_best_choice = candidate_choose_list[fitness_list1.index(min(fitness_list1))]

        distance_list.append(now_best_distance)

    return now_best_choice


candidater_generator(candidate_choose_num)
final_choose = GA(generation_num)
print final_choose
print distance_list[-1]
"""
x_plot = [x_location_list[i] for i in final_choose]
y_plot = [y_location_list[i] for i in final_choose]
plt.plot(x_plot,y_plot)
plt.plot(x_location_list,y_location_list,'ro')
plt.show()

plt.plot(distance_list)
plt.show()
"""