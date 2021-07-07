import enum


class State(enum.Enum):
    in_reception_queue = 0
    reception = 1
    in_department_queue = 2
    preparing_order = 3
