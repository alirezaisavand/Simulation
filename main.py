import Simulator


if __name__ == '__main__':
    N, lam, mu, alpha = map(int, input().split())
    MUs = []

    for i in range(N):
        MUs.append(list(map(int, input().split())))

    simulator = Simulator.Simulator(N, lam, alpha, mu, MUs, 4, 100 * 1000)
    simulator.simulate()
