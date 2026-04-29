#Stop gninnipS My sdroW!

def spin_words(sentence):
    # Your code goes here
    s = sentence.split()
    a = []
    for i in s:
        if len(i) >= 5 :
            a.append(i[::-1])
        else:
            a.append(i)
            
    return " ".join(a)