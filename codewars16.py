#How many numbers III?

def find_all(sum_dig, digs):
    nums = []

    def backtrack(rem_sum, rem_digs, start, path):
        if rem_digs == 0:
            if rem_sum == 0:
                nums.append(int("".join(map(str, path))))
            return

        # pruning
        if rem_sum < start * rem_digs or rem_sum > 9 * rem_digs:
            return

        for d in range(start, 10):
            if d > rem_sum:
                break
            backtrack(rem_sum - d, rem_digs - 1, d, path + [d])

    backtrack(sum_dig, digs, 1, [])

    if not nums:
        return []

    return [len(nums), nums[0], nums[-1]]