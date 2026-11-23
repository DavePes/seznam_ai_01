class Solution:
    def __init__(self):
        # we create a list of triplets that hold (a,b),(b,c),(a,c)  a > b > c
        self.triples = []
        for c in range(8):
            for b in range(c+1, 9):
                for a in range(b+1, 10):
                    num1 = str(a) + str(b)
                    num2 = str(b) + str(c)
                    num3 = str(a) + str(c)
                    triple = (num1, num2, num3)
                    self.triples.append(triple)
    def find_biggest_triple(self, frequency_dict):
        biggest_triple = 0
        for triple in self.triples:
            num1, num2, num3 = triple
            if num1 in frequency_dict and num2 in frequency_dict and num3 in frequency_dict:
                biggest_triple = max(biggest_triple, frequency_dict[num1] + frequency_dict[num2] + frequency_dict[num3])
        return biggest_triple

    
    def solve(self, nums):
        # count the frequency of each number in the list, note that x,y and y,x are considered the same number
        frequency_dict = {}
        # put the numbers into ten buckets based on their digits
        freq_each_digit = [0 for _ in range(10)]

        for num in nums:
            num = str(num)
            # always put the larger number first
            if num[0] < num[1]:
                num = num[1] + num[0]
            frequency_dict[num] = frequency_dict.get(num, 0) + 1
        for num, freq in frequency_dict.items():
            # put the number into the appropriate bucket based on digits
            freq_each_digit[int(num[0])] += freq
            if num[0] != num[1]:
                freq_each_digit[int(num[1])] += freq
        result = max(self.find_biggest_triple(frequency_dict), max(freq_each_digit))
        return result


    
solution = Solution().solve