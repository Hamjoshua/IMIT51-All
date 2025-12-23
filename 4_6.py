import numpy as np
import random

ERROR_P = 0.1

COMPONENTS_COUNT = 5

MIN_REVIEW_TIME = 2
MAX_REVIEW_TIME = 5

REPLACE_TIME_AVG = 5
REPLACE_TIME_DEVIATION = 1

SMALL_FIX_AVG = 10
FULL_FIX_AVG = 15


def simulate_one_robot() -> tuple[float, int]:
    time_score = 0.0
    replaced_comps = 0

    # 1. Осмотр всех компонентов
    for i in range(COMPONENTS_COUNT):       
        review_time = np.random.uniform(MIN_REVIEW_TIME, MAX_REVIEW_TIME)
        time_score += review_time

        is_error_p = random.random() < ERROR_P

        if(is_error_p):
            replace_time = np.random.normal(REPLACE_TIME_AVG,
                                             REPLACE_TIME_DEVIATION)
            time_score += replace_time
            replaced_comps += 1

    # 2. Наладка
    if replaced_comps == 0:
        # мелкая наладка
        time_score += np.random.exponential(scale=SMALL_FIX_AVG)    
    else:
        # полная наладка
        time_score += np.random.exponential(scale=FULL_FIX_AVG)    

    return time_score, replaced_comps


def check_for(n_robots, seed=228):
    rng = np.random.default_rng(seed)

    times = np.empty(n_robots, dtype=float)
    full_flags = np.empty(n_robots, dtype=bool)
    replaced_counts = np.empty(n_robots, dtype=int)

    for i in range(n_robots):
        time, comps = simulate_one_robot()
        times[i] = time
        full_flags[i] = comps > 0       
        replaced_counts[i] = comps

    avg_time = times.mean()
    percent_full = full_flags.mean() * 100.0
    avg_replaced = replaced_counts.mean()

    print(f"--- Результаты за {n_robots} роботов ---")
    print(f"Среднее время ремонта одного робота: {avg_time:.2f} мин")
    print(f"Процент случаев полной наладки: {percent_full:.2f} %")
    print(f"Среднее количество заменённых компонентов: {avg_replaced:.3f}")    
    print()
        

if __name__ == "__main__":
    check_for(10)
    check_for(100)
    check_for(1000)
    check_for(10000)
    check_for(100_000)
    check_for(1_000_000)
