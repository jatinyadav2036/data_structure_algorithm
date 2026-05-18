# 13. Return pyramids

# def pyramid(n):
#     for i in range(n-1,-1,-1):
#         print(" "*i,end='')
#         print("/",end='')
#         if i == 0:
#             print("_"*((n-1)*2),end='')
#         else:
#             print(" "*((n-1-i)*2),end='')
#         print("\\")
# pyramid(6)

def pyramid(n):
    lines = []

    for i in range(n):
        spaces_before = n - i - 1

        row = " " * spaces_before
        row += "/"

        if i == n - 1:
            row += "_" * (2 * i)
        else:
            row += " " * (2 * i)

        row += "\\"

        lines.append(row)

    return "\n".join(lines) + "\n"

print(pyramid(6))