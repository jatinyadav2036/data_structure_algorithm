#Simple Pig Latin
# Simple Pig Latin

def pig_it(text):
    n = []
    g = []
    for i in text :
      n = text.split()
    f = []
    m = []
    for j in n :
      j = list(j)

      l = len(j)
      
      for k in range(1,l):

        f += "".join(j[k])

      f += " ".join(j[0])
      if j[0] == '!' or j[0] == '?':
        continue
      else:
        f+= "".join('ay')
      
      f += "".join(" ")
    f = "".join(f) 
    f = f.rstrip()
    
    
    return f
print(pig_it('Pig latin is cool'))