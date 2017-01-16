"""
Modified the roulette selection formula
"""

# Parameter
candidate_choose_num = 10
generation_num = 1000
mutation_rate = 0.0001


import matplotlib.pyplot as plt
import random
import math
import time

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




#**************************************
#[verification] sum_distance
#**************************************
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



# build up distance matrix

def p2p_distance(a,b):
    return math.sqrt(math.pow((x_location_list[a] - x_location_list[b]), 2) + math.pow((y_location_list[a] - y_location_list[b]), 2))

distance_matrix = []
length = len(x_location_list)
for row in range(length):
    row_distance = []
    for col in range(length):
        row_distance.append(p2p_distance(row,col))
    distance_matrix.append(row_distance)

# calculate the sum distance of a possible choose

def sum_distance1(a_priority):
    sum_distance = 0.0

    for i in range(1, len(a_priority)):
        a = a_priority[i]
        b = a_priority[i-1]
        sum_distance += distance_matrix[a][b]
    return sum_distance

def sum_distance(a_priority):
    sum_distance = 0.0

    for i in range(1, len(a_priority)):
        sum_distance += math.sqrt(
            math.pow((x_location_list[a_priority[i]] - x_location_list[a_priority[i - 1]]), 2) + math.pow(
                (y_location_list[a_priority[i]] - y_location_list[a_priority[i - 1]]), 2))

    return sum_distance


def GA(generation_num):

    mutation_prob_cumu = 0.0
    global mutation_rate

    for generation_idx in range(generation_num):
        #p1rint "Generation",generation_idx
        fitness_list = []
        fitness_list1= []
        selected_list = []

        for candidate_choose in candidate_choose_list:
            fitness_list.append(sum_distance(candidate_choose))

        assert len(fitness_list)== candidate_choose_num,"FL initial failed"
        sigma_distance = sum(fitness_list)
        if sigma_distance <1.0:
            sigma_distance = 1.0
            #mutation_rate = mutation_rate*1.1
           # print "training stop"


        #print " Distance", min(fitness_list_origin)
        # print "Len fitness_list",len(fitness_list),"Len candidate_choose_list",len(candidate_choose_list)

        select_prob = [fitness_list[i] / sigma_distance for i in range(len(fitness_list))]

        """
        fitness_sort_list = [fitness_list[fl] for fl in range(len(fitness_list))]
        fitness_sort_list.sort()

        select_prob = [inverse_select_prob[9 - fitness_list.index(fitness_sort_list.pop(0))] for j in
                       range(len(fitness_list))]
        """
        # print "sp",select_prob

        cumulative_prob = [0 for cp in range(len(select_prob))]
        cumulative_prob[0] = select_prob[0]

        for k in range(1, len(fitness_list)):
            cumulative_prob[k] = cumulative_prob[k - 1] + select_prob[k]

        assert len(fitness_list) == candidate_choose_num, "len fitness_list != CCN before select, generation %r " % generation_idx

        random_point_list = [random.random() for m in range(len(fitness_list))]
        assert len(random_point_list) == candidate_choose_num,"len random_point_list != CCN"
        # print "rpl",random_point_list
        # print "cp",cumulative_prob

        for random_point in random_point_list:
            choose_flag = 0

            if (random_point <= cumulative_prob[0]):
                selected_list.append(candidate_choose_list[0])
                # candidate_choose_list.pop(p)
                #assert len(selected_list[-1]) == 10, "selected list failed in idx_0, generation %r " % generation_idx
                choose_flag += 1

            for p in range(1, len(fitness_list) - 1):
                if (random_point <= cumulative_prob[p]) and (random_point > cumulative_prob[p - 1]):
                    # print "p",p
                    # print "Idx len",len(candidate_choose_list)
                    selected_list.append(candidate_choose_list[p])
                    # candidate_choose_list.pop(p)
                    #assert len(selected_list[-1]) == 10, "selected list failed in idx_1+,generation %r,cp %r,sl %r" % generation_idx
                    choose_flag += 1
            if (random_point > cumulative_prob[len(fitness_list)-2]):
                selected_list.append(candidate_choose_list[9])
                # candidate_choose_list.pop(p)
                #assert len(selected_list[-1]) == 10, "selected list failed in idx_0, generation %r " % generation_idx
                choose_flag += 1

            if choose_flag == 0:
                print "Unselectd Point:", random_point
                # for a_list in selected_list:
                # print "SL",a_list
        assert len(selected_list)== candidate_choose_num,"len SL!= ccn after select, generation %r,cp %r,sl %r " % (generation_idx,len(cumulative_prob),len(selected_list))

        # print "len SL", len(selected_list)

        if len(selected_list) < 10:
            print "len(selected_list)", len(selected_list)
            print "Len RPL", len(random_point_list), "RPL", random_point_list
            print "CP", len(cumulative_prob), cumulative_prob

        while len(candidate_choose_list) > 0:
            candidate_choose_list.pop()

        assert len(candidate_choose_list) == 0,"candidate_choose_list claear failed, generation %r" % generation_idx

        q = 0
        while (q * 2 + 1) < len(selected_list):
        #    print "Q",q
        #    print "Len Selected_list",len(selected_list)

            a = selected_list[q * 2]
            b = selected_list[(q * 2)+1]
            c = crossover(a,b)
            candidate_choose_list.append(c)

            if sum_distance(a) < sum_distance(b):
                candidate_choose_list.append(a)
            else:
                candidate_choose_list.append(b)

            q+=1

        assert len(candidate_choose_list) == candidate_choose_num,"len candidate_choose_list = %r after [crossover],generation %r"  % (len(candidate_choose_list),generation_idx)

        mutation_prob_cumu += mutation_rate * len(candidate_choose_list) * len(candidate_choose_list[0])
        #print mutation_prob_cumu

        while mutation_prob_cumu >= 5.0:
            #print "mutation actived"
            idx = random.choice(range(10))
            candidate_choose_list[idx] = mutation(candidate_choose_list[idx])
            mutation_prob_cumu =  mutation_prob_cumu-1.0

        for candidate_choose in candidate_choose_list:
            fitness_list1.append(sum_distance(candidate_choose))
        #assert len(candidate_choose_list)==10,"len candidate_choose_list != 10 after [mutation],generation %r" % generation_idx


        distance_list.append(min(fitness_list1))

    return candidate_choose_list[fitness_list1.index(min(fitness_list1))]


def GA1(generation_num):

    mutation_prob_cumu = 0.0
    global mutation_rate

    for generation_idx in range(generation_num):
        #p1rint "Generation",generation_idx
        fitness_list = []
        fitness_list1= []
        selected_list = []

        for candidate_choose in candidate_choose_list:
            fitness_list.append(sum_distance1(candidate_choose))

        assert len(fitness_list)== candidate_choose_num,"FL initial failed"
        sigma_distance = sum(fitness_list)
        if sigma_distance <1.0:
            sigma_distance = 1.0
            #mutation_rate = mutation_rate*1.1
           # print "training stop"


        #print " Distance", min(fitness_list_origin)
        # print "Len fitness_list",len(fitness_list),"Len candidate_choose_list",len(candidate_choose_list)

        select_prob = [fitness_list[i] / sigma_distance for i in range(len(fitness_list))]

        """
        fitness_sort_list = [fitness_list[fl] for fl in range(len(fitness_list))]
        fitness_sort_list.sort()

        select_prob = [inverse_select_prob[9 - fitness_list.index(fitness_sort_list.pop(0))] for j in
                       range(len(fitness_list))]
        """
        # print "sp",select_prob

        cumulative_prob = [0 for cp in range(len(select_prob))]
        cumulative_prob[0] = select_prob[0]

        for k in range(1, len(fitness_list)):
            cumulative_prob[k] = cumulative_prob[k - 1] + select_prob[k]

        assert len(fitness_list) == candidate_choose_num, "len fitness_list != CCN before select, generation %r " % generation_idx

        random_point_list = [random.random() for m in range(len(fitness_list))]
        assert len(random_point_list) == candidate_choose_num,"len random_point_list != CCN"
        # print "rpl",random_point_list
        # print "cp",cumulative_prob

        for random_point in random_point_list:
            choose_flag = 0

            if (random_point <= cumulative_prob[0]):
                selected_list.append(candidate_choose_list[0])
                # candidate_choose_list.pop(p)
                #assert len(selected_list[-1]) == 10, "selected list failed in idx_0, generation %r " % generation_idx
                choose_flag += 1

            for p in range(1, len(fitness_list) - 1):
                if (random_point <= cumulative_prob[p]) and (random_point > cumulative_prob[p - 1]):
                    # print "p",p
                    # print "Idx len",len(candidate_choose_list)
                    selected_list.append(candidate_choose_list[p])
                    # candidate_choose_list.pop(p)
                    #assert len(selected_list[-1]) == 10, "selected list failed in idx_1+,generation %r,cp %r,sl %r" % generation_idx
                    choose_flag += 1
            if (random_point > cumulative_prob[len(fitness_list)-2]):
                selected_list.append(candidate_choose_list[9])
                # candidate_choose_list.pop(p)
                #assert len(selected_list[-1]) == 10, "selected list failed in idx_0, generation %r " % generation_idx
                choose_flag += 1

            if choose_flag == 0:
                print "Unselectd Point:", random_point
                # for a_list in selected_list:
                # print "SL",a_list
        assert len(selected_list)== candidate_choose_num,"len SL!= ccn after select, generation %r,cp %r,sl %r " % (generation_idx,len(cumulative_prob),len(selected_list))

        # print "len SL", len(selected_list)

        if len(selected_list) < 10:
            print "len(selected_list)", len(selected_list)
            print "Len RPL", len(random_point_list), "RPL", random_point_list
            print "CP", len(cumulative_prob), cumulative_prob

        while len(candidate_choose_list) > 0:
            candidate_choose_list.pop()

        assert len(candidate_choose_list) == 0,"candidate_choose_list claear failed, generation %r" % generation_idx

        q = 0
        while (q * 2 + 1) < len(selected_list):
        #    print "Q",q
        #    print "Len Selected_list",len(selected_list)

            a = selected_list[q * 2]
            b = selected_list[(q * 2)+1]
            c = crossover(a,b)
            candidate_choose_list.append(c)

            if sum_distance(a) < sum_distance(b):
                candidate_choose_list.append(a)
            else:
                candidate_choose_list.append(b)

            q+=1

        assert len(candidate_choose_list) == candidate_choose_num,"len candidate_choose_list = %r after [crossover],generation %r"  % (len(candidate_choose_list),generation_idx)

        mutation_prob_cumu += mutation_rate * len(candidate_choose_list) * len(candidate_choose_list[0])
        #print mutation_prob_cumu

        while mutation_prob_cumu >= 5.0:
            #print "mutation actived"
            idx = random.choice(range(10))
            candidate_choose_list[idx] = mutation(candidate_choose_list[idx])
            mutation_prob_cumu =  mutation_prob_cumu-1.0

        for candidate_choose in candidate_choose_list:
            fitness_list1.append(sum_distance1(candidate_choose))
        #assert len(candidate_choose_list)==10,"len candidate_choose_list != 10 after [mutation],generation %r" % generation_idx


        distance_list.append(min(fitness_list1))

    return candidate_choose_list[fitness_list1.index(min(fitness_list1))]

time_list = []
time_list1 = []
candidater_generator(candidate_choose_num)
for i in range(20):
    time_a = time.time()
    final_choose = GA(generation_num+i*1000)
    time_b = time.time()
    time_list.append(time_b-time_a)
    time_c = time.time()
    final_choose1 = GA1(generation_num + i * 1000)
    time_d = time.time()
    time_list1.append(time_d - time_c)

#print len(final_choose)
"""
x_plot = [x_location_list[i] for i in final_choose]
y_plot = [y_location_list[i] for i in final_choose]
plt.plot(x_plot,y_plot)
plt.plot(x_location_list,y_location_list,'ro')
plt.show()
"""
"""
plt.plot(distance_list)
plt.ylabel("Distance")
plt.xlabel("Iteration")
plt.show()
"""
plt.plot(time_list,'r',time_list1,'b')
plt.ylabel("Time")
plt.xlabel("Iteration")
plt.show()