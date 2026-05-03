#Find the Middle of the Product

def find_middle(st):
    if type(st) == list or not st:
      return -1

    l = list(st)
    nums = ["0","1","2","3","4","5","6","7","8","9"]
    pro = []
    for i in l:
      if i in nums:
        pro.append(int(i))

    if not pro:
      return -1
    
    p = 1
    
    for j in pro:
      p = p*j
    
    n = len(str(p))//2
    po = str(p)
    
    if len(str(p)) == 0:
      return int(po[0])
    
    if n ==1:
      if len(str(p)) == 2:
        return (int(po[0]+po[1]))
    
    if len(str(p))%2 != 0 :
        return int(po[n])
    else:
      if po[n-1] =="0":
        return (int(po[n])+int(po[n-1]))
      else:
        return(int(po[n-1]+po[n]))


s = find_middle('sf}b-?b)$/``v,$mv**sl$wth `gg(')
print(s)