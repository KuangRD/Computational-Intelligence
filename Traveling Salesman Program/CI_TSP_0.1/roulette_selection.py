from _initial_GA import sum_distance
import random

def roulette_selection(candidate_choose_list):

        fitness_list = []
        selected_list = []

        for candidate_choose in candidate_choose_list:
            fitness_list.append(sum_distance(candidate_choose))

        sigma_distance = sum(fitness_list)
        print " Distance", min(fitness_list)
        #print "Len fitness_list",len(fitness_list),"Len candidate_choose_list",len(candidate_choose_list)

        inverse_select_prob = [fitness_list[i] / sigma_distance for i in range(len(fitness_list))]

        fitness_sort_list = [fitness_list[fl] for fl in range(len(fitness_list))]
        fitness_sort_list.sort()


        select_prob = [inverse_select_prob[9 - fitness_list.index(fitness_sort_list.pop(0))] for j in range(len(fitness_list))]

        #print "sp",select_prob

        cumulative_prob = [0 for cp in range(len(select_prob)) ]
        cumulative_prob[0] = select_prob[0]


        for k in range(1, len(fitness_list)):
            cumulative_prob[k] = cumulative_prob[k - 1] + select_prob[k]

        assert len(fitness_list) == 10, "len fitness_list != 10 before select, generation %r " % generation_idx

        random_point_list = [random.random() for m in range(len(fitness_list))]
        assert len(random_point_list) == 10, "len random_point_list != 10"
        #print "rpl",random_point_list
        #print "cp",cumulative_prob

        for random_point in random_point_list:
            choose_flag = 0

            if (random_point <= cumulative_prob[0]):
                selected_list.append(candidate_choose_list[0])
                #candidate_choose_list.pop(p)
                assert len(selected_list[-1]) == 10,"selected list failed in idx_0, generation %r " % generation_idx
                choose_flag += 1

            for p in range(1,len(fitness_list)-1):
                if (random_point <= cumulative_prob[p]) and (random_point > cumulative_prob[p-1]):
                    #print "p",p
                    #print "Idx len",len(candidate_choose_list)
                    selected_list.append(candidate_choose_list[p])
                    #candidate_choose_list.pop(p)
                    assert len(selected_list[-1]) == 10, "selected list failed in idx_1+,generation %r,cp %r,sl %r" % generation_idx
                    choose_flag += 1
            if (random_point > cumulative_prob[8]):
                selected_list.append(candidate_choose_list[9])
                #candidate_choose_list.pop(p)
                assert len(selected_list[-1]) == 10,"selected list failed in idx_0, generation %r " % generation_idx
                choose_flag += 1

            if choose_flag == 0:
                print "Unselectd Point:",random_point
        #for a_list in selected_list:
            #print "SL",a_list
        #assert len(selected_list)==10,"len SL <10 after select, generation %r,cp %r,sl %r " % (generation_idx,len(cumulative_prob),len(selected_list))

        #print "len SL", len(selected_list)

        if len(selected_list) < 10:
            print "len(selected_list)",len(selected_list)
            print "Len RPL",len(random_point_list),"RPL",random_point_list
            print "CP",len(cumulative_prob),cumulative_prob

        return selected_list


candidate_choose_list = [[0, 5, 4, 6, 1, 9, 8, 2, 3, 7], [0, 7, 5, 4, 8, 6, 3, 9, 2, 1], [6, 1, 4, 2, 9, 7, 5, 3, 0, 8], [9, 7, 1, 3, 5, 8, 2, 6, 4, 0], [7, 0, 6, 5, 2, 4, 1, 3, 9, 8], [9, 3, 0, 6, 4, 2, 5, 7, 1, 8], [7, 1, 6, 8, 5, 9, 0, 3, 4, 2], [7, 6, 3, 2, 1, 9, 0, 8, 5, 4], [6, 4, 7, 1, 5, 9, 2, 3, 8, 0], [4, 7, 1, 3, 8, 2, 0, 6, 9, 5]]
for i in range(10):
    SL = roulette_selection(candidate_choose_list)
