def GA(generation_num):

    mutation_prob_cumu = 0.0

    for generation_idx in range(generation_num):
        fitness_list = []
        fitness_list1= []
        selected_list = []

        for candidate_choose in candidate_choose_list:
            fitness_list.append(sum_distance(candidate_choose))
        print candidate_choose_list
        sigma_distance = sum(fitness_list)
        print "Generation", generation_idx, " Distance", min(fitness_list)
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

            if (random_point <= cumulative_prob[0]):
                selected_list.append(candidate_choose_list[0])
                #candidate_choose_list.pop(p)
                assert len(selected_list[-1]) == 10,"selected list failed in idx_0, generation %r " % generation_idx

            for p in range(1,len(fitness_list)):
                if (random_point <= cumulative_prob[p]) and (random_point > cumulative_prob[p-1]):
                    #print "p",p
                    #print "Idx len",len(candidate_choose_list)
                    selected_list.append(candidate_choose_list[p])
                    #candidate_choose_list.pop(p)
                    assert len(selected_list[-1]) == 10, "selected list failed in idx_1+,generation %r,cp %r,sl %r" % generation_idx
        #for a_list in selected_list:
            #print "SL",a_list
        assert len(selected_list)==10,"len SL <10 after select, generation %r,cp %r,sl %r " % (generation_idx,len(cumulative_prob),len(selected_list))


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

        assert len(candidate_choose_list) == 10,"len candidate_choose_list != 10 after [crossover],generation %r"  % generation_idx

        mutation_prob_cumu += mutation_rate * len(candidate_choose_list) * len(candidate_choose_list[0])
        #print mutation_prob_cumu

        while mutation_prob_cumu >= 1.0:
            print "mutation actived"
            idx = random.choice(range(10))
            candidate_choose_list[idx] = mutation(candidate_choose_list[idx])
            mutation_prob_cumu =  mutation_prob_cumu-1.0

        for candidate_choose in candidate_choose_list:
            fitness_list1.append(sum_distance(candidate_choose))
        assert len(candidate_choose_list)==10,"len candidate_choose_list != 10 after [mutation],generation %r" % generation_idx

#        if min(fitness_list1) > min(fitness_list):
#            print "*********************"
#            print fitness_list
#            print fitness_list1
#            print "*********************"

        print "After One Generation Distance",min(fitness_list1)


candidater_generator(10)
GA(10)