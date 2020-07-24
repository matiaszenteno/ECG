def required_ventilators(N,alpha,beta,p,tp,tq,t):
    # First case
    if (t >= 0 and t <= 7):

        first_sum = 0

        for i in range(0, t + 1):
            new_critic_infected, new_non_critic_infected = infections(
                                                            N,alpha,beta,p,i)
            first_sum += new_critic_infected

        return first_sum

    # Second case
    if (t > 7 and t < tp):

        first_sum =  0
        second_sum = 0

        for i in range(0, t + 1):
            new_critic_infected, new_non_critic_infected = infections(
                                                            N,alpha,beta,p,i)
            first_sum += new_critic_infected

        for i in range(t - 7, 1):
            new_critic_infected, new_non_critic_infected = infections(
                                                            N,alpha,beta,p,i)
            second_sum += new_critic_infected

        return first_sum - second_sum

    # Third case
    if (t >= tp and t <= simulation_time):

        first_sum =  0
        second_sum = 0
        third_sum = 0

        for i in range(0, t + 1):
            new_critic_infected, new_non_critic_infected = infections(
                                                            N,alpha,beta,p,i)
            first_sum += new_critic_infected

        for i in range(0, t - 7):
            new_critic_infected, new_non_critic_infected = infections(
                                                            N,alpha,beta,p,i)
            second_sum += new_critic_infected

        for i in range(tp, t):
            new_critic_recovered, new_non_critic_recovered = recoveries(
                                                        N,alpha,beta,p,tp,tq,i)
            third_sum += new_critic_recovered

        return first_sum - second_sum - third_sum

