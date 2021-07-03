import Department


class Simulator:
    def __init__(self, N, lam, alpha, MUs):
        self.Departments = []
        for i in range(N):
            self.Departments.add(Department.Department())  # todo

