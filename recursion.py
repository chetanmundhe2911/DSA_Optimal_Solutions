# Generating all possible Subsequences using Recursion including the empty one.

def backtrack(subset: list, index: int):
    if index >= len(nums):
        result.append(subset.copy())
        return
    subset.append(nums[index])
    backtrack(subset, index + 1)
    subset.pop()
    backtrack(subset, index + 1)

  
result = []
nums = [1,2,3]
backtrack([], 0)
print(result)
