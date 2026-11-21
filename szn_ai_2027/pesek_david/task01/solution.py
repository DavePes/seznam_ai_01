import sys
#print("Hello World!", file=sys.stderr)
class Solution:
    def solve(self, nums):
        d = {}
        for num in nums:
            # always put the larger number first
            if num[0] < num[1]:
                num = num[1] + num[0]
            d[num] = d.get(num, 0) + 1
          


    
        