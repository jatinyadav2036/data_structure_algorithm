# Valid Braces

def valid_braces(string):
    stack = []
    for i in string :
        if i == "(" or  i == "["  or i == "{":
            stack.append(i)
        elif i == ")" or i == "]" or i == "}":
            if not stack :
                return False 
            top = stack[-1]
            if (i == ")" and top != "(") or (i== "]" and top != "[") or (i == "}" and top != "{"):
                return False 
            stack.pop()
    return not stack
# string = "[({})](]"
# print(True if valid_braces(string) else False )
    