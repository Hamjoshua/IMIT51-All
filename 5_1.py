import numpy as np
import math

FIRST_LIFETIME_AVG = 2
SECOND_LIFETIME_AVG = 1

LIFETIME = 1.5

def get_block_p():
    first_lambda = 1 / FIRST_LIFETIME_AVG
    second_lambda = 1 /SECOND_LIFETIME_AVG

    first_live_p = math.exp(-first_lambda * LIFETIME)
    second_live_p = math.exp(-second_lambda * LIFETIME)

    first_death_p = 1 - first_live_p
    second_death_p = 1 - second_live_p

    return first_live_p, second_live_p, first_death_p, second_death_p


def analytic_p() -> tuple[float, float, float]:
    first_live_p, second_live_p, first_death_p, second_death_p = get_block_p()

    event_a = first_live_p * second_live_p
    event_b = first_live_p * second_death_p
    event_c = first_death_p * second_death_p

    header = "--- Аналитический блок ---"
    print(header)
    print(f"а) Не откажет ни один из блоков\n{first_live_p} \
* {second_live_p} = \n{first_live_p * second_live_p}")
    print(f"б) Откажет только 2-й блок\n{first_live_p} \
* {second_death_p} = \n{first_live_p * second_death_p}")
    print(f"в) Откажут оба блока\n{first_death_p} \
* {second_death_p} = \n{first_death_p * second_death_p}")
    print("-" * len(header))

    return event_a, event_b, event_c



if __name__ == "__main__":
    n_runs = 100

    event_a, event_b, event_c = analytic_p()
    first_live_p, second_live_p, first_death_p, second_death_p = get_block_p()

    arr = np.random.uniform(0, 1, (n_runs, 2))   

    counter_event_a = 0
    counter_event_b = 0
    counter_event_c = 0

    for p_block1, p_block2 in arr:
        block1_dead = p_block1 > first_live_p
        block2_dead = p_block2 > second_live_p

        if(not block1_dead and not block2_dead):
            counter_event_a += 1

        elif(not block1_dead and block2_dead):
            counter_event_b += 1

        elif(block1_dead and block2_dead):
            counter_event_c += 1



    # counter_event_a = np.count_nonzero(arr[(arr[:, 0] < first_live_p) & 
    #                              (arr[:, 1] < second_live_p)])
    # counter_event_b = np.count_nonzero(arr[(arr[:, 0] < first_live_p) & 
    #                              (arr[:, 1] > second_live_p)])
    # counter_event_c = np.count_nonzero(arr[(arr[:, 0] > first_live_p) & 
    #                              (arr[:, 1] > second_live_p)])
    
    print(arr[(arr[:, 0] > first_live_p) & 
                                 (arr[:, 1] > second_live_p)])
    
    fact_event_a = counter_event_a / n_runs
    fact_event_b = counter_event_b / n_runs
    fact_event_c = counter_event_c / n_runs
    
    header = "--- Блок Монте-Карло ---"
    print(header)
    print(f"а) Не откажет ни один из блоков\
          \n- теор. P = {event_a}\
          \n- факт. P = {fact_event_a}\
          \n- абс. погрешность = {abs(fact_event_a - event_a)}")
    print(f"б) б) Откажет только 2-й блок\
          \n- теор. P = {event_b}\
          \n- факт. P = {fact_event_b}\
          \n- абс. погрешность = {abs(fact_event_b - event_b)}")
    print(f"в) Откажут оба блока\
          \n- теор. P = {event_c}\
          \n- факт. P = {fact_event_c}\
          \n- абс. погрешность = {abs(fact_event_c - event_c)}")
    print('-' * len(header))
