# Hashing


# Frequency
arr = [1, 2, 2, 3, 1, 1]

freq = {}

for num in arr:
    freq[num] = freq.get(num, 0) + 1

print(freq)

# Finding the duplicates

arr = [1, 2, 3, 2, 5]

seen = set()

for x in arr:
    if x in seen:
        print(x)
    else:
        seen.add(x)

# First Non-Repeating Character

s = "aabbcd"

freq = {}

for ch in s:
    freq[ch] = freq.get(ch, 0) + 1

for ch in s:
    if freq[ch] == 1:
        print(ch)
        break


# Two Sum (Most Famous Hashing Problem)


nums = [2, 7, 11, 15]
target = 9

mp = {}

for i, num in enumerate(nums):
    complement = target - num

    if complement in mp:
        print(mp[complement], i)
        break

    mp[num] = i