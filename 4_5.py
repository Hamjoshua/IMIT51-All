import numpy
import random


MATERIAL_COST = 20
WORK_COST = 5
POLISH_COST = 4
FIX_FAT_COST = 3
POLISH_FIX_COST = 2

NORM_WORK_P = 0.8
BROKEN_WORK_P = 0.08
FAT_WORK_P = 0.12

POLISH_UP_MISTAKE_P = 0.03
POLISH_DOWN_MISTAKE_P = 0.06

DETAIL_PROFIT = 35


def simulate_one() -> float:
    # 1. Токарка
    cost = MATERIAL_COST + WORK_COST 
    work_p = random.random()

    if work_p < BROKEN_WORK_P:
        return -cost
    elif work_p < FAT_WORK_P + BROKEN_WORK_P:
        cost += FIX_FAT_COST
    
    # 2. Шлифовка
    cost += POLISH_COST
    polish_mistake_up_p = random.random() < POLISH_UP_MISTAKE_P
    polish_mistake_down_p = random.random() < POLISH_DOWN_MISTAKE_P

    # сразу две сломалось -> произведение вероятностей
    if(polish_mistake_up_p and polish_mistake_down_p):
        return -cost
    
    # возникновение одного или другого -> сумма вероятностей
    if(polish_mistake_down_p ^ polish_mistake_up_p):
        cost += POLISH_FIX_COST

    return DETAIL_PROFIT - cost


def check_for(n_runs):
    good_count = 0
    total_profit = 0.0
    is_debug_on = False

    for _ in range(n_runs):
        profit = simulate_one()
        if profit > 0:
            good_count += 1
        total_profit += profit

    good_prob = good_count / n_runs
    avg_profit = (total_profit / n_runs)
    print(f"--- Результаты за {n_runs} испытаний ---")
    print(f"Вероятность годной детали: {good_prob:.4f}")
    print(f"Средняя прибыль на деталь: {avg_profit:.4f}")
    print()


if __name__ == "__main__":
    check_for(10)
    check_for(100)
    check_for(1000)
    check_for(10000)
    check_for(100_000)
    check_for(1_000_000)
    