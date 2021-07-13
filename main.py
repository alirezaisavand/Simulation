import Simulator
import matplotlib.pyplot as plt


def calc_server_rates(N, number_of_servers, lam, mu, alpha):
    rates = [i for i in range(1, 11)]
    lengths_of_queues = []
    for rate in rates:
        Simulator.Simulator.reset()
        Mus = []
        for i in range(N):
            Mus.append([rate] * number_of_servers)
        simulator = Simulator.Simulator(N, lam, alpha, mu, Mus, 4, 100 * 1000)
        simulator.simulate(report=False)
        lengths_of_queues.append(Simulator.Simulator.get_sum_of_lengths_of_queues())

    plt.plot(rates, lengths_of_queues)
    plt.xlabel("rate of service time (customer per time)")
    plt.ylabel("sum of lengths of queues")
    plt.show()


if __name__ == '__main__':
    Simulator.Simulator.reset()
    N, lam, mu, alpha = map(int, input().split())
    MUs = []

    avg_servers = 0

    for i in range(N):
        MUs.append(list(map(int, input().split())))
        avg_servers += len(MUs[-1]) / N

    simulator = Simulator.Simulator(N, lam, alpha, mu, MUs, 4, 100 * 1000)
    simulator.simulate()

    calc_server_rates(N, int(avg_servers), lam, mu, alpha)
