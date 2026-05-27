# 19 First non-repeating character 

def first_non_repeating_letter(s):
    l = list(s.lower())
    for i in range(len(l)) :
        if l.count(l[i]) == 1:
            return s[i]
    return ''