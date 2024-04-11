class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        ans = []
        index={}
        for i in range(len(nums)):
            if target-nums[i] not in index:
                index[nums[i]] = i
            else:
                ans = [index[target - nums[i]],i]
        return ans