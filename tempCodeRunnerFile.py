def pyramid(n):
    for i in range(n-1,-1,-1):
        print(" "*i,end='')
        print("/",end='')
        if i == 0:
            print("_"*((n-1)*2),end='')
        else:
            print(" "*((n-1-i)*2),end='')
        print("\\")
        
    
    

pyramid(6)