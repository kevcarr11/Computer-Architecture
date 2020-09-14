# Given the following array of values, print out all the elements in reverse order, with each element on a new line.
# For example, given the list
# [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
# Your output should be
# 0
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.

arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# loop through list and print each num in reverse order 

# reversed() return a reversed list 

reversed_arr = reversed(arr)

for i in reversed_arr:
    print(i)


# stretch

# Given a hashmap where the keys are integers, print out all of the values of the hashmap in reverse order, ordered by the keys.
# For example, given the following hashmap:
# {
#   14: "vs code",
#   3: "window",
#   9: "alloc",
#   26: "views",
#   4: "bottle",
#   15: "inbox",
#   79: "widescreen",
#   16: "coffee",
#   19: "tissue",
# }
# The expected output is:
# widescreen
# views
# tissue
# coffee
# inbox
# vs code
# alloc
# bottle
# window
# since "widescreen" has the largest integer key, "views" has the second largest, etc.
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.



hash = {
  14: "vs code",
  3: "window",
  9: "alloc",
  26: "views",
  4: "bottle",
  15: "inbox",
  79: "widescreen",
  16: "coffee",
  19: "tissue",
}



l = list(hash.items())
l.sort(reverse=True)

d = dict(l)

for key in d:
    print(d[key])




a = 0b01011010
b = 0b10101111

print(bin(a & b))