# Moving zeros to end
def move_zeros(lst):
    return [i for i in lst if i != 0] + [0] * lst.count(0)