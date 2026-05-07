# Pete, the baker
def cakes(recipe, available):
    lst =[]
    for key , value in recipe.items():
        if key not in available:
            return 0
        lst.append(available[key] // value)
    return min(lst)
    