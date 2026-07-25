# 2525. Categorize Box According to Criteria

class Solution(object):
    def categorizeBox(self, length, width, height, mass):
        arr = []
        if length >= 10000 or width >= 10000 or height >= 10000 or mass >= 10000 or length * width * height >= 10 ** 9 :
            arr.append("Bulky")
        if mass >= 100 :
            arr.append("Heavy")
        if len(arr) == 0:
            return "Neither"
        if len(arr) == 2:
            return "Both"
        if arr[0] == "Bulky":
            return "Bulky"
        if arr[0] == "Heavy":
            return "Heavy"
