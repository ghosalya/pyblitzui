from time import sleep


def print_name():
    return "nama"


def add(a, b):
    return a + b


def print_add(a, b, longe=True):
    return str(a + b), str(longe)


def print_intervals(a):
    for i in range(a):
        print(i)
        sleep(1)
    return a
