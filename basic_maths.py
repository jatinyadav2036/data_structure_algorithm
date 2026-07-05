# digits of number
n = int(input("Enter the number: "))
# lst = []
# while n > 0:
#     last_digit = n % 10 
#     lst.insert(0,last_digit)
#     n= n // 10
# print(" ".join(map(str,lst)))
# print("-".join(str(i) for i in lst))

# Count all Digits of a Number
 
# if n == 0:
#     print(0)
# cnt = 0 
# while n > 0:
#     last_digit = n % 10 
#     cnt += 1
#     n= n // 10
# print(cnt)

# Reverse a number and Palindrome

# reversed_number = 0
# temp = n
# while n > 0:
#     last_digit = n % 10
#     reversed_number = (reversed_number * 10) + last_digit
#     n = n // 10
# print(reversed_number)
# if temp == reversed_number:
#     print("The number is Palindrome.")


# Armstrong Number

# cnt = len(str(n))
# temp = n
# arm = 0
# while n > 0:
#     last_digit = n % 10
#     arm += last_digit ** cnt
#     n = n // 10
# if temp == arm:
#     print("The number is Armstrong Number.")

# All Divisor
# lst = []
# for i in range(1,n+1):
#     if n % i == 0:
#         lst.append(i)
# for i in range(1,int(n**0.5)+1):
#     if n % i == 0:
#         lst.append(i)
#         if (n//i) != i:
#             lst.append(n//i)
# lst.sort()
# print(lst)
# if len(lst) == 2:
#     print("The Number is Prime Number.")

# GCD (Greatest Common Divisor)
m = int(input("Enter the Second Number: "))
gcd = 0
for i in range(1,min(n,m)+1):
    if n % i == 0 and m % i == 0:
        gcd = i 
print(gcd)
if n == m :
    print(n)

while n > 0 and m > 0:
    if n > m : n = n % m
    else: m = m % n
    if n == 0 : print(m)
    elif m == 0 : print(n)

