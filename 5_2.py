import numpy as np
import matplotlib.pyplot as plt

LAMBDA = 8 / 24
T_MAX = 100.0

WAGONS_AVG = 10
WAGONS_DEVIATION = 4

SEED = 228


def simulate_trains(
    t_max: float = T_MAX,
    lam: float = LAMBDA,
    avg_wagons: float = WAGONS_AVG,
    deviation_wagons: float = WAGONS_DEVIATION,
    seed: int | None = SEED,
):
    rng = np.random.default_rng(seed)

    arrival_times: list[float] = []
    train_sizes: list[int] = []

    t = 0.0

    while True:        
        delta_t = rng.exponential(scale=1.0 / lam)
        t += delta_t

        if t > t_max:
            break
        
        wagons = rng.normal(loc=avg_wagons, scale=deviation_wagons)

        # округление и отсечение снизу
        wagons = max(0, int(round(wagons)))

        arrival_times.append(t)
        train_sizes.append(wagons)

    return np.array(arrival_times), np.array(train_sizes)


def model():
    arrival_times, train_sizes = simulate_trains()

    n_trains = len(arrival_times)
    sim_avg_wagons = train_sizes.mean() if n_trains > 0 else 0.0
    sim_deviation_wagons = train_sizes.std(ddof=1) if n_trains > 1 else 0.0

    # теоретически ожидаемое число поездов за T_MAX:
    expected_trains = LAMBDA * T_MAX

    print("--- Результаты имитации ---")
    print(f"Горизонт моделирования: {T_MAX} ч")
    print(f"Интенсивность (лямбда): {LAMBDA:.4f} поездов/ч")
    print()
    print(f"Фактически пришло поездов: {n_trains}")
    print(f"Теоретически ожидается: {expected_trains:.2f}")
    print()
    print(f"Среднее число вагонов (симуляция): {sim_avg_wagons:.2f}")
    print(f"Заданное Mx: {WAGONS_AVG}")
    print()
    print(f"Ст. отклонение вагонов (симуляция): {sim_deviation_wagons:.2f}")
    print(f"Заданное стан. отклон: {WAGONS_DEVIATION}")
    print()
    
    print("Все поезда за 100 часов (время, вагоны):")
    for t, k in list(zip(arrival_times, train_sizes)):
        print(f"t = {t:6.2f} ч, вагонов = {k}")


def graph():
    arrival_times, train_sizes = simulate_trains()

    # 1. Кумулятивное число поездов
    cum_trains = np.arange(1, len(arrival_times) + 1)

    plt.figure(figsize=(10, 4))
    plt.step(arrival_times, cum_trains, where="post")
    plt.xlabel("Время, ч")
    plt.ylabel("Число поездов")
    plt.title("Кумулятивный поток поездов за 100 часов")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Кумулятивное число вагонов
    cum_wagons = np.cumsum(train_sizes)

    plt.figure(figsize=(10, 4))
    plt.step(arrival_times, cum_wagons, where="post")
    plt.xlabel("Время, ч")
    plt.ylabel("Суммарное число вагонов")
    plt.title("Кумулятивный поток вагонов за 100 часов")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 3. Обычный поток вагонов
    plt.figure(figsize=(10, 4))
    plt.step(arrival_times, train_sizes, where="post")
    plt.xlabel("Время, ч")
    plt.ylabel("Суммарное число вагонов")
    plt.title("Кумулятивный поток вагонов за 100 часов")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    model()
    graph()