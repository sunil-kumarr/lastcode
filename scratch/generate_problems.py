import os
import sys
import textwrap

problems_dir = "/Users/sunilkumar/Downloads/neonodes/neonodes/problems"
os.makedirs(problems_dir, exist_ok=True)

problems_data = []

# =========================================================================
# SLIDING WINDOW (10)
# =========================================================================

problems_data.append({
    "id": "longest_substring_no_repeat",
    "title": "Longest Substring No Repeat",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "Given a string s, find the length of the longest substring without repeating characters.",
    "default_input": '"abcabcbb"',
    "params": "s",
    "code_lines": [
        "def longest_substring(s):",
        "    char_map = {}",
        "    left = 0",
        "    max_len = 0",
        "    for right in range(len(s)):",
        "        char = s[right]",
        "        if char in char_map and char_map[char] >= left:",
        "            left = char_map[char] + 1",
        "        char_map[char] = right",
        "        max_len = max(max_len, right - left + 1)",
        "    return max_len",
    ],
    "line_map": "{1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11}",
    "instrumented_body": """
char_map = {}
left = 0
max_len = 0
for right in range(len(s)):
    char = s[right]
    if char in char_map and char_map[char] >= left:
        left = char_map[char] + 1
        _viz_update(left, right)
    char_map[char] = right
    max_len = max(max_len, right - left + 1)
    _viz_compare(left, right)
return max_len
""",
    "input_unpack": "s = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_longest_substring_no_repeat_instrumented",
    _longest_substring_no_repeat_instrumented,
    s,
    marker_fns={"_viz_compare", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
    }
)
"""
})

problems_data.append({
    "id": "min_size_subarray_sum",
    "title": "Minimum Size Subarray Sum",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target.",
    "default_input": "([2, 3, 1, 2, 4, 3], 7)",
    "params": "nums, target",
    "code_lines": [
        "def min_subarray_len(nums, target):",
        "    left = 0",
        "    curr_sum = 0",
        "    min_len = float('inf')",
        "    for right in range(len(nums)):",
        "        curr_sum += nums[right]",
        "        while curr_sum >= target:",
        "            min_len = min(min_len, right - left + 1)",
        "            curr_sum -= nums[left]",
        "            left += 1",
        "    return min_len if min_len != float('inf') else 0",
    ],
    "line_map": "{1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11}",
    "instrumented_body": """
left = 0
curr_sum = 0
min_len = float('inf')
for right in range(len(nums)):
    curr_sum += nums[right]
    _viz_compare(left, right)
    while curr_sum >= target:
        min_len = min(min_len, right - left + 1)
        _viz_found(left, right)
        curr_sum -= nums[left]
        left += 1
        _viz_update(left, right)
return min_len if min_len != float('inf') else 0
""",
    "input_unpack": "nums, target = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "window_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_min_size_subarray_sum_instrumented",
    _min_size_subarray_sum_instrumented,
    nums, target,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "max_consecutive_ones_iii",
    "title": "Max Consecutive Ones III",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "Given a binary array nums and an integer k, return the maximum number of consecutive 1s in the array if you can flip at most k 0s.",
    "default_input": "([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2)",
    "params": "nums, k",
    "code_lines": [
        "def longest_ones(nums, k):",
        "    left = 0",
        "    zeros = 0",
        "    max_len = 0",
        "    for right in range(len(nums)):",
        "        if nums[right] == 0:",
        "            zeros += 1",
        "        while zeros > k:",
        "            if nums[left] == 0:",
        "                zeros -= 1",
        "            left += 1",
        "        max_len = max(max_len, right - left + 1)",
        "    return max_len",
    ],
    "line_map": "{i: i for i in range(1, 15)}",
    "instrumented_body": """
left = 0
zeros = 0
max_len = 0
for right in range(len(nums)):
    if nums[right] == 0:
        zeros += 1
    _viz_compare(left, right)
    while zeros > k:
        if nums[left] == 0:
            zeros -= 1
        left += 1
        _viz_update(left, right)
    max_len = max(max_len, right - left + 1)
return max_len
""",
    "input_unpack": "nums, k = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_max_consecutive_ones_iii_instrumented",
    _max_consecutive_ones_iii_instrumented,
    nums, k,
    marker_fns={"_viz_compare", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
    }
)
"""
})

problems_data.append({
    "id": "permutation_in_string",
    "title": "Permutation in String",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.",
    "default_input": '("ab", "eidbaooo")',
    "params": "s1, s2",
    "code_lines": [
        "def check_inclusion(s1, s2):",
        "    if len(s1) > len(s2): return False",
        "    c1 = {}; c2 = {}",
        "    for c in s1: c1[c] = c1.get(c, 0) + 1",
        "    for i in range(len(s1)): c2[s2[i]] = c2.get(s2[i], 0) + 1",
        "    if c1 == c2: return True",
        "    left = 0",
        "    for right in range(len(s1), len(s2)):",
        "        c2[s2[right]] = c2.get(s2[right], 0) + 1",
        "        c2[s2[left]] -= 1",
        "        if c2[s2[left]] == 0: del c2[s2[left]]",
        "        left += 1",
        "        if c1 == c2: return True",
        "    return False",
    ],
    "line_map": "{i: i for i in range(1, 15)}",
    "instrumented_body": """
if len(s1) > len(s2): return False
c1 = {}; c2 = {}
for c in s1: c1[c] = c1.get(c, 0) + 1
for i in range(len(s1)): c2[s2[i]] = c2.get(s2[i], 0) + 1

left = 0
_viz_compare(left, len(s1) - 1)
if c1 == c2: return True

for right in range(len(s1), len(s2)):
    c2[s2[right]] = c2.get(s2[right], 0) + 1
    c2[s2[left]] -= 1
    if c2[s2[left]] == 0: del c2[s2[left]]
    left += 1
    _viz_update(left, right)
    if c1 == c2:
        _viz_found(left, right)
        return True
return False
""",
    "input_unpack": "s1, s2 = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "window_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_permutation_in_string_instrumented",
    _permutation_in_string_instrumented,
    s1, s2,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "find_all_anagrams",
    "title": "Find All Anagrams in String",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "Given two strings s and p, return an array of all the start indices of p's anagrams in s.",
    "default_input": '("cbaebabacd", "abc")',
    "params": "s, p",
    "code_lines": [
        "def find_anagrams(s, p):",
        "    res = []",
        "    if len(p) > len(s): return res",
        "    pc = {}; sc = {}",
        "    for char in p: pc[char] = pc.get(char, 0) + 1",
        "    for i in range(len(p)): sc[s[i]] = sc.get(s[i], 0) + 1",
        "    if sc == pc: res.append(0)",
        "    left = 0",
        "    for right in range(len(p), len(s)):",
        "        sc[s[right]] = sc.get(s[right], 0) + 1",
        "        sc[s[left]] -= 1",
        "        if sc[s[left]] == 0: del sc[s[left]]",
        "        left += 1",
        "        if sc == pc: res.append(left)",
        "    return res",
    ],
    "line_map": "{i: i for i in range(1, 16)}",
    "instrumented_body": """
res = []
if len(p) > len(s): return res
pc = {}; sc = {}
for char in p: pc[char] = pc.get(char, 0) + 1
for i in range(len(p)): sc[s[i]] = sc.get(s[i], 0) + 1

left = 0
_viz_compare(left, len(p) - 1)
if sc == pc: res.append(0)

for right in range(len(p), len(s)):
    sc[s[right]] = sc.get(s[right], 0) + 1
    sc[s[left]] -= 1
    if sc[s[left]] == 0: del sc[s[left]]
    left += 1
    _viz_update(left, right)
    if sc == pc:
        _viz_found(left, right)
        res.append(left)
return res
""",
    "input_unpack": "s, p = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "window_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_find_all_anagrams_instrumented",
    _find_all_anagrams_instrumented,
    s, p,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "min_window_substring",
    "title": "Minimum Window Substring",
    "topic": "sliding_window",
    "difficulty": "hard",
    "renderer": "sliding_window",
    "desc": "Given two strings s and t, return the minimum window substring of s such that every character in t (including duplicates) is included in the window.",
    "default_input": '("ADOBECODEBANC", "ABC")',
    "params": "s, t",
    "code_lines": [
        "def min_window(s, t):",
        "    if not s or not t: return ''",
        "    dict_t = {}",
        "    for c in t: dict_t[c] = dict_t.get(c, 0) + 1",
        "    required = len(dict_t)",
        "    left = 0; formed = 0",
        "    window_counts = {}",
        "    ans = (float('inf'), None, None)",
        "    for right in range(len(s)):",
        "        char = s[right]",
        "        window_counts[char] = window_counts.get(char, 0) + 1",
        "        if char in dict_t and window_counts[char] == dict_t[char]:",
        "            formed += 1",
        "        while left <= right and formed == required:",
        "            if right - left + 1 < ans[0]:",
        "                ans = (right - left + 1, left, right)",
        "            char = s[left]",
        "            window_counts[char] -= 1",
        "            if char in dict_t and window_counts[char] < dict_t[char]:",
        "                formed -= 1",
        "            left += 1",
        "    return '' if ans[0] == float('inf') else s[ans[1]:ans[2]+1]",
    ],
    "line_map": "{i: i for i in range(1, 23)}",
    "instrumented_body": """
if not s or not t: return ""
dict_t = {}
for c in t: dict_t[c] = dict_t.get(c, 0) + 1
required = len(dict_t)
left = 0; formed = 0
window_counts = {}
ans = (float('inf'), None, None)
for right in range(len(s)):
    char = s[right]
    window_counts[char] = window_counts.get(char, 0) + 1
    if char in dict_t and window_counts[char] == dict_t[char]:
        formed += 1
    _viz_compare(left, right)
    while left <= right and formed == required:
        if right - left + 1 < ans[0]:
            ans = (right - left + 1, left, right)
            _viz_found(left, right)
        char = s[left]
        window_counts[char] -= 1
        if char in dict_t and window_counts[char] < dict_t[char]:
            formed -= 1
        left += 1
        _viz_update(left, right)
return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]
""",
    "input_unpack": "s, t = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "window_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_min_window_substring_instrumented",
    _min_window_substring_instrumented,
    s, t,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "longest_repeating_char_replace",
    "title": "Longest Repeating Char Replace",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "Given a string s and an integer k, you can choose any character of the string and change it to any other uppercase English character. Return the length of the longest substring containing all repeating letters you can get after performing at most k operations.",
    "default_input": '("AABABBA", 1)',
    "params": "s, k",
    "code_lines": [
        "def character_replacement(s, k):",
        "    counts = {}",
        "    max_count = 0",
        "    left = 0",
        "    max_len = 0",
        "    for right in range(len(s)):",
        "        counts[s[right]] = counts.get(s[right], 0) + 1",
        "        max_count = max(max_count, counts[s[right]])",
        "        while (right - left + 1) - max_count > k:",
        "            counts[s[left]] -= 1",
        "            left += 1",
        "        max_len = max(max_len, right - left + 1)",
        "    return max_len",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
counts = {}
max_count = 0
left = 0
max_len = 0
for right in range(len(s)):
    counts[s[right]] = counts.get(s[right], 0) + 1
    max_count = max(max_count, counts[s[right]])
    _viz_compare(left, right)
    while (right - left + 1) - max_count > k:
        counts[s[left]] -= 1
        left += 1
        _viz_update(left, right)
    max_len = max(max_len, right - left + 1)
return max_len
""",
    "input_unpack": "s, k = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_longest_repeating_char_replace_instrumented",
    _longest_repeating_char_replace_instrumented,
    s, k,
    marker_fns={"_viz_compare", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
    }
)
"""
})

problems_data.append({
    "id": "sliding_window_maximum",
    "title": "Sliding Window Maximum",
    "topic": "sliding_window",
    "difficulty": "hard",
    "renderer": "sliding_window",
    "desc": "Given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. Return the max sliding window.",
    "default_input": "([1, 3, -1, -3, 5, 3, 6, 7], 3)",
    "params": "nums, k",
    "code_lines": [
        "def max_sliding_window(nums, k):",
        "    res = []",
        "    q = []",
        "    left = 0",
        "    for right in range(len(nums)):",
        "        while q and nums[q[-1]] < nums[right]:",
        "            q.pop()",
        "        q.append(right)",
        "        if left > q[0]:",
        "            q.pop(0)",
        "        if right >= k - 1:",
        "            res.append(nums[q[0]])",
        "            left += 1",
        "    return res",
    ],
    "line_map": "{i: i for i in range(1, 15)}",
    "instrumented_body": """
res = []
q = []
left = 0
for right in range(len(nums)):
    while q and nums[q[-1]] < nums[right]:
        q.pop()
    q.append(right)
    _viz_compare(left, right)
    if left > q[0]:
        q.pop(0)
    if right >= k - 1:
        res.append(nums[q[0]])
        _viz_found(left, right)
        left += 1
        _viz_update(left, right)
return res
""",
    "input_unpack": "nums, k = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "window_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_sliding_window_maximum_instrumented",
    _sliding_window_maximum_instrumented,
    nums, k,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "subarrays_k_different",
    "title": "Subarrays with K Diff Ints",
    "topic": "sliding_window",
    "difficulty": "hard",
    "renderer": "sliding_window",
    "desc": "Given an integer array nums and an integer k, return the number of good subarrays of nums. A good subarray is an array where the number of different integers in that subarray is exactly k.",
    "default_input": "([1, 2, 1, 2, 3], 2)",
    "params": "nums, k",
    "code_lines": [
        "def subarrays_with_k_distinct(nums, k):",
        "    def at_most(k_val):",
        "        count = {}",
        "        left = 0; ans = 0",
        "        for right in range(len(nums)):",
        "            count[nums[right]] = count.get(nums[right], 0) + 1",
        "            while len(count) > k_val:",
        "                count[nums[left]] -= 1",
        "                if count[nums[left]] == 0: del count[nums[left]]",
        "                left += 1",
        "            ans += right - left + 1",
        "        return ans",
        "    return at_most(k) - at_most(k-1)",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
def at_most(k_val):
    count = {}
    left = 0; ans = 0
    for right in range(len(nums)):
        count[nums[right]] = count.get(nums[right], 0) + 1
        _viz_compare(left, right)
        while len(count) > k_val:
            count[nums[left]] -= 1
            if count[nums[left]] == 0: del count[nums[left]]
            left += 1
            _viz_update(left, right)
        ans += right - left + 1
    return ans
return at_most(k) - at_most(k-1)
""",
    "input_unpack": "nums, k = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_subarrays_k_different_instrumented",
    _subarrays_k_different_instrumented,
    nums, k,
    marker_fns={"_viz_compare", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
    }
)
"""
})

problems_data.append({
    "id": "fruit_into_baskets",
    "title": "Fruit Into Baskets",
    "topic": "sliding_window",
    "difficulty": "medium",
    "renderer": "sliding_window",
    "desc": "You are visiting a farm that has a single row of fruit trees arranged from left to right. You have two baskets, and each basket can only hold a single type of fruit. Return the maximum number of fruits you can collect.",
    "default_input": "[1, 2, 1, 2, 3]",
    "params": "fruits",
    "code_lines": [
        "def total_fruit(fruits):",
        "    counts = {}",
        "    left = 0",
        "    max_fruits = 0",
        "    for right in range(len(fruits)):",
        "        counts[fruits[right]] = counts.get(fruits[right], 0) + 1",
        "        while len(counts) > 2:",
        "            counts[fruits[left]] -= 1",
        "            if counts[fruits[left]] == 0: del counts[fruits[left]]",
        "            left += 1",
        "        max_fruits = max(max_fruits, right - left + 1)",
        "    return max_fruits",
    ],
    "line_map": "{i: i for i in range(1, 13)}",
    "instrumented_body": """
counts = {}
left = 0
max_fruits = 0
for right in range(len(fruits)):
    counts[fruits[right]] = counts.get(fruits[right], 0) + 1
    _viz_compare(left, right)
    while len(counts) > 2:
        counts[fruits[left]] -= 1
        if counts[fruits[left]] == 0: del counts[fruits[left]]
        left += 1
        _viz_update(left, right)
    max_fruits = max(max_fruits, right - left + 1)
return max_fruits
""",
    "input_unpack": "fruits = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "window_check", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "window_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_fruit_into_baskets_instrumented",
    _fruit_into_baskets_instrumented,
    fruits,
    marker_fns={"_viz_compare", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
    }
)
"""
})


# =========================================================================
# TWO POINTER (10)
# =========================================================================

problems_data.append({
    "id": "valid_palindrome",
    "title": "Valid Palindrome",
    "topic": "two_pointer",
    "difficulty": "easy",
    "renderer": "two_pointer",
    "desc": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
    "default_input": '"A man, a plan, a canal: Panama"',
    "params": "s",
    "code_lines": [
        "def is_palindrome(s):",
        "    clean_s = ''.join(c.lower() for c in s if c.isalnum())",
        "    left, right = 0, len(clean_s) - 1",
        "    while left < right:",
        "        if clean_s[left] != clean_s[right]:",
        "            return False",
        "        left += 1; right -= 1",
        "    return True",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
clean_s = "".join(c.lower() for c in s if c.isalnum())
left, right = 0, len(clean_s) - 1
while left < right:
    _viz_compare(left, right)
    if clean_s[left] != clean_s[right]:
        return False
    left += 1; right -= 1
    _viz_update(left, right)
_viz_found(left, right)
return True
""",
    "input_unpack": "s = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
clean_s = "".join(c.lower() for c in s if c.isalnum())
return recorder.record(
    "_valid_palindrome_instrumented",
    _valid_palindrome_instrumented,
    clean_s,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "two_sum_sorted",
    "title": "Two Sum II - Sorted Array",
    "topic": "two_pointer",
    "difficulty": "medium",
    "renderer": "two_pointer",
    "desc": "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.",
    "default_input": "([2, 7, 11, 15], 9)",
    "params": "numbers, target",
    "code_lines": [
        "def two_sum(numbers, target):",
        "    left = 0",
        "    right = len(numbers) - 1",
        "    while left < right:",
        "        sum_val = numbers[left] + numbers[right]",
        "        if sum_val == target:",
        "            return [left + 1, right + 1]",
        "        elif sum_val < target:",
        "            left += 1",
        "        else:",
        "            right -= 1",
        "    return []",
    ],
    "line_map": "{i: i for i in range(1, 13)}",
    "instrumented_body": """
left = 0
right = len(numbers) - 1
while left < right:
    sum_val = numbers[left] + numbers[right]
    _viz_compare(left, right)
    if sum_val == target:
        _viz_found(left, right)
        return [left + 1, right + 1]
    elif sum_val < target:
        left += 1
    else:
        right -= 1
    _viz_update(left, right)
return []
""",
    "input_unpack": "numbers, target = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_two_sum_sorted_instrumented",
    _two_sum_sorted_instrumented,
    numbers, target,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "three_sum",
    "title": "3Sum",
    "topic": "two_pointer",
    "difficulty": "medium",
    "renderer": "two_pointer",
    "desc": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.",
    "default_input": "[-1, 0, 1, 2, -1, -4]",
    "params": "nums",
    "code_lines": [
        "def three_sum(nums):",
        "    nums.sort()",
        "    res = []",
        "    for i in range(len(nums) - 2):",
        "        if i > 0 and nums[i] == nums[i-1]: continue",
        "        left, right = i + 1, len(nums) - 1",
        "        while left < right:",
        "            sum_val = nums[i] + nums[left] + nums[right]",
        "            if sum_val == 0:",
        "                res.append([nums[i], nums[left], nums[right]])",
        "                left += 1; right -= 1",
        "            elif sum_val < 0: left += 1",
        "            else: right -= 1",
        "    return res",
    ],
    "line_map": "{i: i for i in range(1, 15)}",
    "instrumented_body": """
nums.sort()
res = []
for i in range(len(nums) - 2):
    if i > 0 and nums[i] == nums[i-1]: continue
    left = i + 1
    right = len(nums) - 1
    while left < right:
        sum_val = nums[i] + nums[left] + nums[right]
        _viz_compare(left, right)
        if sum_val == 0:
            res.append([nums[i], nums[left], nums[right]])
            _viz_found(left, right)
            left += 1; right -= 1
        elif sum_val < 0:
            left += 1
        else:
            right -= 1
        _viz_update(left, right)
return res
""",
    "input_unpack": "nums = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_three_sum_instrumented",
    _three_sum_instrumented,
    nums,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "container_water",
    "title": "Container With Most Water",
    "topic": "two_pointer",
    "difficulty": "medium",
    "renderer": "two_pointer",
    "desc": "You are given an integer array height of length n. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.",
    "default_input": "[1, 8, 6, 2, 5, 4, 8, 3, 7]",
    "params": "height",
    "code_lines": [
        "def max_area(height):",
        "    left = 0",
        "    right = len(height) - 1",
        "    max_area = 0",
        "    while left < right:",
        "        width = right - left",
        "        h = min(height[left], height[right])",
        "        max_area = max(max_area, width * h)",
        "        if height[left] < height[right]:",
        "            left += 1",
        "        else:",
            "            right -= 1",
        "    return max_area",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
left = 0
right = len(height) - 1
max_area = 0
while left < right:
    width = right - left
    h = min(height[left], height[right])
    max_area = max(max_area, width * h)
    _viz_compare(left, right)
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
    _viz_update(left, right)
_viz_found(left, right)
return max_area
""",
    "input_unpack": "height = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_container_water_instrumented",
    _container_water_instrumented,
    height,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "trapping_rain_water",
    "title": "Trapping Rain Water",
    "topic": "two_pointer",
    "difficulty": "hard",
    "renderer": "two_pointer",
    "desc": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
    "default_input": "[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]",
    "params": "height",
    "code_lines": [
        "def trap(height):",
        "    if not height: return 0",
        "    left, right = 0, len(height) - 1",
        "    left_max, right_max = height[left], height[right]",
        "    water = 0",
        "    while left < right:",
        "        if height[left] < height[right]:",
        "            left += 1",
        "            left_max = max(left_max, height[left])",
        "            water += left_max - height[left]",
        "        else:",
        "            right -= 1",
        "            right_max = max(right_max, height[right])",
        "            water += right_max - height[right]",
        "    return water",
    ],
    "line_map": "{i: i for i in range(1, 16)}",
    "instrumented_body": """
if not height: return 0
left, right = 0, len(height) - 1
left_max, right_max = height[left], height[right]
water = 0
while left < right:
    _viz_compare(left, right)
    if height[left] < height[right]:
        left += 1
        left_max = max(left_max, height[left])
        water += left_max - height[left]
    else:
        right -= 1
        right_max = max(right_max, height[right])
        water += right_max - height[right]
    _viz_update(left, right)
_viz_found(left, right)
return water
""",
    "input_unpack": "height = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_trapping_rain_water_instrumented",
    _trapping_rain_water_instrumented,
    height,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "sort_colors",
    "title": "Sort Colors",
    "topic": "two_pointer",
    "difficulty": "medium",
    "renderer": "two_pointer",
    "desc": "Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue (0, 1, and 2).",
    "default_input": "[2, 0, 2, 1, 1, 0]",
    "params": "nums",
    "code_lines": [
        "def sort_colors(nums):",
        "    left = 0",
        "    curr = 0",
        "    right = len(nums) - 1",
        "    while curr <= right:",
        "        if nums[curr] == 0:",
        "            nums[left], nums[curr] = nums[curr], nums[left]",
        "            left += 1; curr += 1",
        "        elif nums[curr] == 2:",
        "            nums[right], nums[curr] = nums[curr], nums[right]",
        "            right -= 1",
        "        else:",
        "            curr += 1",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
left = 0
curr = 0
right = len(nums) - 1
while curr <= right:
    _viz_compare(curr, right)
    if nums[curr] == 0:
        nums[left], nums[curr] = nums[curr], nums[left]
        left += 1; curr += 1
    elif nums[curr] == 2:
        nums[right], nums[curr] = nums[curr], nums[right]
        right -= 1
    else:
        curr += 1
    _viz_update(left, right)
_viz_found(left, right)
""",
    "input_unpack": "nums = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_sort_colors_instrumented",
    _sort_colors_instrumented,
    nums,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "remove_duplicates",
    "title": "Remove Duplicates from Sorted",
    "topic": "two_pointer",
    "difficulty": "easy",
    "renderer": "two_pointer",
    "desc": "Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.",
    "default_input": "[1, 1, 2]",
    "params": "nums",
    "code_lines": [
        "def remove_duplicates(nums):",
        "    if not nums: return 0",
        "    left = 0",
        "    for right in range(1, len(nums)):",
        "        if nums[right] != nums[left]:",
        "            left += 1",
        "            nums[left] = nums[right]",
        "    return left + 1",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
if not nums: return 0
left = 0
for right in range(1, len(nums)):
    _viz_compare(left, right)
    if nums[right] != nums[left]:
        left += 1
        nums[left] = nums[right]
        _viz_update(left, right)
_viz_found(left, left)
return left + 1
""",
    "input_unpack": "nums = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_remove_duplicates_instrumented",
    _remove_duplicates_instrumented,
    nums,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "move_zeroes",
    "title": "Move Zeroes",
    "topic": "two_pointer",
    "difficulty": "easy",
    "renderer": "two_pointer",
    "desc": "Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.",
    "default_input": "[0, 1, 0, 3, 12]",
    "params": "nums",
    "code_lines": [
        "def move_zeroes(nums):",
        "    left = 0",
        "    for right in range(len(nums)):",
        "        if nums[right] != 0:",
        "            nums[left], nums[right] = nums[right], nums[left]",
        "            left += 1",
    ],
    "line_map": "{i: i for i in range(1, 7)}",
    "instrumented_body": """
left = 0
for right in range(len(nums)):
    _viz_compare(left, right)
    if nums[right] != 0:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        _viz_update(left, right)
_viz_found(left, right)
""",
    "input_unpack": "nums = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_move_zeroes_instrumented",
    _move_zeroes_instrumented,
    nums,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "backspace_compare",
    "title": "Backspace String Compare",
    "topic": "two_pointer",
    "difficulty": "easy",
    "renderer": "two_pointer",
    "desc": "Given two strings s and t, return true if they are equal when both are typed into empty text editors. '#' means a backspace character.",
    "default_input": '("ab#c", "ad#c")',
    "params": "s, t",
    "code_lines": [
        "def backspace_compare(s, t):",
        "    def next_valid(string, index):",
        "        backspaces = 0",
        "        while index >= 0:",
        "            if string[index] == '#': backspaces += 1",
        "            elif backspaces > 0: backspaces -= 1",
        "            else: break",
        "            index -= 1",
        "        return index",
        "    i, j = len(s) - 1, len(t) - 1",
        "    while i >= 0 or j >= 0:",
        "        i = next_valid(s, i); j = next_valid(t, j)",
        "        if i >= 0 and j >= 0 and s[i] != t[j]: return False",
        "        if (i >= 0) != (j >= 0): return False",
        "        i -= 1; j -= 1",
        "    return True",
    ],
    "line_map": "{i: i for i in range(1, 17)}",
    "instrumented_body": """
def next_valid(string, index):
    backspaces = 0
    while index >= 0:
        if string[index] == '#': backspaces += 1
        elif backspaces > 0: backspaces -= 1
        else: break
        index -= 1
    return index
i, j = len(s) - 1, len(t) - 1
while i >= 0 or j >= 0:
    _viz_compare(i, j)
    i = next_valid(s, i); j = next_valid(t, j)
    if i >= 0 and j >= 0 and s[i] != t[j]: return False
    if (i >= 0) != (j >= 0): return False
    i -= 1; j -= 1
    _viz_update(i, j)
_viz_found(i, j)
return True
""",
    "input_unpack": "s, t = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_backspace_compare_instrumented",
    _backspace_compare_instrumented,
    s, t,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})

problems_data.append({
    "id": "assign_cookies",
    "title": "Assign Cookies",
    "topic": "two_pointer",
    "difficulty": "easy",
    "renderer": "two_pointer",
    "desc": "Assume you are a awesome parent and want to give your cookies. But, you should give each child at most one cookie. Return the maximum number of children content.",
    "default_input": "([1, 2, 3], [1, 1])",
    "params": "g, s",
    "code_lines": [
        "def find_content_children(g, s):",
        "    g.sort(); s.sort()",
        "    left, right = 0, 0",
        "    while left < len(g) and right < len(s):",
        "        if s[right] >= g[left]:",
        "            left += 1",
        "        right += 1",
        "    return left",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
g.sort(); s.sort()
left, right = 0, 0
while left < len(g) and right < len(s):
    _viz_compare(left, right)
    if s[right] >= g[left]:
        left += 1
    right += 1
    _viz_update(left, right)
_viz_found(left, right)
return left
""",
    "input_unpack": "g, s = input_data",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_compare", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_found", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_assign_cookies_instrumented",
    _assign_cookies_instrumented,
    g, s,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
"""
})


# =========================================================================
# STACK (10)
# =========================================================================

problems_data.append({
    "id": "min_stack",
    "title": "Min Stack",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.",
    "default_input": '[("push", -2), ("push", 0), ("push", -3), "getMin", "pop", "top", "getMin"]',
    "params": "operations",
    "code_lines": [
        "class MinStack:",
        "    def __init__(self):",
        "        self.stack = []",
        "        self.min_stack = []",
        "    def push(self, val):",
        "        self.stack.append(val)",
        "        val = min(val, self.min_stack[-1] if self.min_stack else val)",
        "        self.min_stack.append(val)",
        "    def pop(self):",
        "        self.stack.pop(); self.min_stack.pop()",
        "    def top(self): return self.stack[-1]",
        "    def getMin(self): return self.min_stack[-1]",
    ],
    "line_map": "{i: i for i in range(1, 13)}",
    "instrumented_body": """
stack = []
min_stack = []
results = []
for op in operations:
    if isinstance(op, tuple):
        action, val = op
    else:
        action, val = op, None
    
    if action == "push":
        stack.append(val)
        if not min_stack or val <= min_stack[-1]:
            min_stack.append(val)
        else:
            min_stack.append(min_stack[-1])
        _viz_push(val)
    elif action == "pop":
        if stack:
            val = stack.pop()
            min_stack.pop()
            _viz_pop(val)
    elif action in ("top", "getMin"):
        val = min_stack[-1] if action == "getMin" else (stack[-1] if stack else None)
        _viz_peek(val)
        results.append(val)
return results
""",
    "input_unpack": "operations = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("val"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("val"), "locals": locs}
def handle_peek(locs: dict, depth: int) -> dict | None:
    return {"type": "peek", "val": locs.get("val"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_min_stack_instrumented",
    _min_stack_instrumented,
    operations,
    marker_fns={"_viz_push", "_viz_pop", "_viz_peek"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
        "_viz_peek": handle_peek,
    }
)
"""
})

problems_data.append({
    "id": "eval_rpn",
    "title": "Evaluate Reverse Polish Notation",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are +, -, *, and /.",
    "default_input": '["2", "1", "+", "3", "*"]',
    "params": "tokens",
    "code_lines": [
        "def eval_rpn(tokens):",
        "    stack = []",
        "    for token in tokens:",
        "        if token in ('+', '-', '*', '/'):",
        "            b = stack.pop(); a = stack.pop()",
        "            if token == '+': stack.append(a + b)",
        "            elif token == '-': stack.append(a - b)",
        "            elif token == '*': stack.append(a * b)",
        "            else: stack.append(int(a / b))",
        "        else: stack.append(int(token))",
        "    return stack[0]",
    ],
    "line_map": "{i: i for i in range(1, 12)}",
    "instrumented_body": """
stack = []
for token in tokens:
    if token in ("+", "-", "*", "/"):
        b = stack.pop()
        _viz_pop(b)
        a = stack.pop()
        _viz_pop(a)
        if token == "+": res = a + b
        elif token == "-": res = a - b
        elif token == "*": res = a * b
        else: res = int(a / b)
        stack.append(res)
        _viz_push(res)
    else:
        val = int(token)
        stack.append(val)
        _viz_push(val)
return stack[0] if stack else 0
""",
    "input_unpack": "tokens = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("res", locs.get("val")), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("b") if "b" in locs else locs.get("a"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_eval_rpn_instrumented",
    _eval_rpn_instrumented,
    tokens,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "generate_parentheses",
    "title": "Generate Parentheses",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
    "default_input": "3",
    "params": "n",
    "code_lines": [
        "def generate_parentheses(n):",
        "    ans = []",
        "    stack = []",
        "    def backtrack(op, cl):",
        "        if op == cl == n: ans.append(''.join(stack)); return",
        "        if op < n:",
        "            stack.append('(')",
        "            backtrack(op + 1, cl)",
        "            stack.pop()",
        "        if cl < op:",
        "            stack.append(')')",
        "            backtrack(op, cl + 1)",
        "            stack.pop()",
    ],
    "line_map": "{i: i for i in range(1, 16)}",
    "instrumented_body": """
ans = []
stack = []
def backtrack(open_c: int, close_c: int):
    if open_c == close_c == n:
        ans.append("".join(stack))
        _viz_peek("".join(stack))
        return
    if open_c < n:
        stack.append("(")
        _viz_push("(")
        backtrack(open_c + 1, close_c)
        stack.pop()
        _viz_pop("(")
    if close_c < open_c:
        stack.append(")")
        _viz_push(")")
        backtrack(open_c, close_c + 1)
        stack.pop()
        _viz_pop(")")
backtrack(0, 0)
return ans
""",
    "input_unpack": "n = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": "(", "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": ")", "locals": locs}
def handle_peek(locs: dict, depth: int) -> dict | None:
    return {"type": "peek", "val": locs.get("ans")[-1] if locs.get("ans") else "", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_generate_parentheses_instrumented",
    _generate_parentheses_instrumented,
    n,
    marker_fns={"_viz_push", "_viz_pop", "_viz_peek"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
        "_viz_peek": handle_peek,
    }
)
"""
})

problems_data.append({
    "id": "daily_temperatures",
    "title": "Daily Temperatures",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the i-th day to get a warmer temperature.",
    "default_input": "[73, 74, 75, 71, 69, 72, 76, 73]",
    "params": "temperatures",
    "code_lines": [
        "def daily_temperatures(temperatures):",
        "    ans = [0] * len(temperatures)",
        "    stack = []",
        "    for i, temp in enumerate(temperatures):",
        "        while stack and temperatures[stack[-1]] < temp:",
        "            idx = stack.pop()",
        "            ans[idx] = i - idx",
        "        stack.append(i)",
        "    return ans",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
ans = [0] * len(temperatures)
stack = []
for i, temp in enumerate(temperatures):
    while stack and temperatures[stack[-1]] < temp:
        idx = stack.pop()
        _viz_pop(idx)
        ans[idx] = i - idx
    stack.append(i)
    _viz_push(i)
return ans
""",
    "input_unpack": "temperatures = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("i"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("idx"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_daily_temperatures_instrumented",
    _daily_temperatures_instrumented,
    temperatures,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "next_greater_element",
    "title": "Next Greater Element I",
    "topic": "stack",
    "difficulty": "easy",
    "renderer": "stack",
    "desc": "The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.",
    "default_input": "([4, 1, 2], [1, 3, 4, 2])",
    "params": "nums1, nums2",
    "code_lines": [
        "def next_greater(nums1, nums2):",
        "    mapping = {}; stack = []",
        "    for num in nums2:",
        "        while stack and stack[-1] < num:",
        "            popped = stack.pop()",
        "            mapping[popped] = num",
        "        stack.append(num)",
        "    return [mapping.get(n, -1) for n in nums1]",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
mapping = {}
stack = []
for num in nums2:
    while stack and stack[-1] < num:
        popped = stack.pop()
        _viz_pop(popped)
        mapping[popped] = num
    stack.append(num)
    _viz_push(num)
res = [mapping.get(n, -1) for n in nums1]
return res
""",
    "input_unpack": "nums1, nums2 = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("num"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_next_greater_element_instrumented",
    _next_greater_element_instrumented,
    nums1, nums2,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "simplify_path",
    "title": "Simplify Path",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Given a string path, which is an absolute path (starting with a slash '/') to a file or directory in a Unix-style file system, convert it to the simplified canonical path.",
    "default_input": '"/home//foo/"',
    "params": "path",
    "code_lines": [
        "def simplify_path(path):",
        "    stack = []",
        "    for part in path.split('/'):",
        "        if part == '..':",
        "            if stack: stack.pop()",
        "        elif part and part != '.':",
        "            stack.append(part)",
        "    return '/' + '/'.join(stack)",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
stack = []
for part in path.split("/"):
    if part == "..":
        if stack:
            popped = stack.pop()
            _viz_pop(popped)
    elif part and part != ".":
        stack.append(part)
        _viz_push(part)
return "/" + "/".join(stack)
""",
    "input_unpack": "path = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("part"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_simplify_path_instrumented",
    _simplify_path_instrumented,
    path,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "asteroid_collision",
    "title": "Asteroid Collision",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "We are given an array asteroids of integers representing asteroids in a row. Find out the state of the asteroids after all collisions.",
    "default_input": "[5, 10, -5]",
    "params": "asteroids",
    "code_lines": [
        "def asteroid_collision(asteroids):",
        "    stack = []",
        "    for ast in asteroids:",
        "        while stack and ast < 0 < stack[-1]:",
        "            if stack[-1] < -ast: stack.pop(); continue",
        "            elif stack[-1] == -ast: stack.pop()",
        "            break",
        "        else: stack.append(ast)",
        "    return stack",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
stack = []
for ast in asteroids:
    while stack and ast < 0 < stack[-1]:
        if stack[-1] < -ast:
            popped = stack.pop()
            _viz_pop(popped)
            continue
        elif stack[-1] == -ast:
            popped = stack.pop()
            _viz_pop(popped)
        break
    else:
        stack.append(ast)
        _viz_push(ast)
return stack
""",
    "input_unpack": "asteroids = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("ast"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_asteroid_collision_instrumented",
    _asteroid_collision_instrumented,
    asteroids,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "online_stock_span",
    "title": "Online Stock Span",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.",
    "default_input": "[100, 80, 60, 70, 60, 75, 85]",
    "params": "prices",
    "code_lines": [
        "class StockSpanner:",
        "    def __init__(self):",
        "        self.stack = []",
        "    def next(self, price):",
        "        span = 1",
        "        while self.stack and self.stack[-1][0] <= price:",
        "            span += self.stack.pop()[1]",
        "        self.stack.append((price, span))",
        "        return span",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
stack = []
res = []
for price in prices:
    span = 1
    while stack and stack[-1][0] <= price:
        popped = stack.pop()
        _viz_pop(popped)
        span += popped[1]
    stack.append((price, span))
    _viz_push((price, span))
    res.append(span)
return res
""",
    "input_unpack": "prices = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("price"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_online_stock_span_instrumented",
    _online_stock_span_instrumented,
    prices,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "basic_calculator",
    "title": "Basic Calculator",
    "topic": "stack",
    "difficulty": "hard",
    "renderer": "stack",
    "desc": "Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.",
    "default_input": '"(1+(4+5+2)-3)+(6+8)"',
    "params": "s",
    "code_lines": [
        "def calculate(s):",
        "    stack = []; res = 0; sign = 1; op = 0",
        "    for ch in s:",
        "        if ch.isdigit(): op = op * 10 + int(ch)",
        "        elif ch == '+': res += sign * op; op = 0; sign = 1",
        "        elif ch == '-': res += sign * op; op = 0; sign = -1",
        "        elif ch == '(': stack.append(res); stack.append(sign); res = 0; sign = 1",
        "        elif ch == ')':: res += sign * op; op = 0; res = stack.pop() * res + stack.pop()",
        "    return res + sign * op",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
stack = []
operand = 0
res = 0
sign = 1
for ch in s:
    if ch.isdigit():
        operand = operand * 10 + int(ch)
    elif ch == '+':
        res += sign * operand
        operand = 0
        sign = 1
    elif ch == '-':
        res += sign * operand
        operand = 0
        sign = -1
    elif ch == '(':
        stack.append(res)
        _viz_push(res)
        stack.append(sign)
        _viz_push(sign)
        res = 0
        sign = 1
    elif ch == ')':
        res += sign * operand
        operand = 0
        p_sign = stack.pop()
        _viz_pop(p_sign)
        p_res = stack.pop()
        _viz_pop(p_res)
        res = p_res + p_sign * res
res += sign * operand
return res
""",
    "input_unpack": "s = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("res", locs.get("sign")), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("p_sign", locs.get("p_res")), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_basic_calculator_instrumented",
    _basic_calculator_instrumented,
    s,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})

problems_data.append({
    "id": "remove_k_digits",
    "title": "Remove K Digits",
    "topic": "stack",
    "difficulty": "medium",
    "renderer": "stack",
    "desc": "Given string num representing a non-negative integer num, and an integer k, return the smallest possible integer after removing k digits from num.",
    "default_input": '("1432219", 3)',
    "params": "num, k",
    "code_lines": [
        "def remove_k_digits(num, k):",
        "    stack = []",
        "    for digit in num:",
        "        while k > 0 and stack and stack[-1] > digit:",
        "            stack.pop(); k -= 1",
        "        stack.append(digit)",
        "    while k > 0: stack.pop(); k -= 1",
        "    res = ''.join(stack).lstrip('0')",
        "    return res if res else '0'",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
stack = []
for digit in num:
    while k > 0 and stack and stack[-1] > digit:
        popped = stack.pop()
        _viz_pop(popped)
        k -= 1
    stack.append(digit)
    _viz_push(digit)
while k > 0:
    popped = stack.pop()
    _viz_pop(popped)
    k -= 1
ans = "".join(stack).lstrip("0")
return ans if ans else "0"
""",
    "input_unpack": "num, k = input_data",
    "run_handlers": """
def handle_push(locs: dict, depth: int) -> dict | None:
    return {"type": "push", "val": locs.get("digit"), "locals": locs}
def handle_pop(locs: dict, depth: int) -> dict | None:
    return {"type": "pop", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_remove_k_digits_instrumented",
    _remove_k_digits_instrumented,
    num, k,
    marker_fns={"_viz_push", "_viz_pop"},
    nested_fns=set(),
    marker_handlers={
        "_viz_push": handle_push,
        "_viz_pop": handle_pop,
    }
)
"""
})


# =========================================================================
# QUEUE (10)
# =========================================================================

problems_data.append({
    "id": "implement_stack_queue",
    "title": "Implement Stack using Queues",
    "topic": "queue",
    "difficulty": "easy",
    "renderer": "queue",
    "desc": "Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (push, top, pop, and empty).",
    "default_input": '[("push", 1), ("push", 2), "pop", "top"]',
    "params": "ops",
    "code_lines": [
        "class MyStack:",
        "    def __init__(self):",
        "        self.q = []",
        "    def push(self, val):",
        "        self.q.append(val)",
        "        for _ in range(len(self.q) - 1):",
        "            self.q.append(self.q.pop(0))",
        "    def pop(self): return self.q.pop(0)",
        "    def top(self): return self.q[0]",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
queue = []
results = []
for op in ops:
    if isinstance(op, tuple):
        action, val = op
    else:
        action, val = op, None
    if action == "push":
        queue.append(val)
        _viz_enqueue(val)
        for _ in range(len(queue) - 1):
            popped = queue.pop(0)
            _viz_dequeue(popped)
            queue.append(popped)
            _viz_enqueue(popped)
    elif action == "pop":
        if queue:
            val = queue.pop(0)
            _viz_dequeue(val)
            results.append(val)
    elif action == "top":
        val = queue[0] if queue else None
        results.append(val)
return results
""",
    "input_unpack": "ops = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("val", locs.get("popped")), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("val", locs.get("popped")), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_implement_stack_queue_instrumented",
    _implement_stack_queue_instrumented,
    ops,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "implement_queue_stack",
    "title": "Implement Queue using Stacks",
    "topic": "queue",
    "difficulty": "easy",
    "renderer": "queue",
    "desc": "Implement a first-in-first-out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty).",
    "default_input": '[("push", 1), ("push", 2), "pop", "peek"]',
    "params": "ops",
    "code_lines": [
        "class MyQueue:",
        "    def __init__(self):",
        "        self.s1 = []; self.s2 = []",
        "    def push(self, val): self.s1.append(val)",
        "    def pop(self):",
        "        self.peek()",
        "        return self.s2.pop()",
        "    def peek(self):",
        "        if not self.s2:",
        "            while self.s1: self.s2.append(self.s1.pop())",
        "        return self.s2[-1]",
    ],
    "line_map": "{i: i for i in range(1, 12)}",
    "instrumented_body": """
s1 = []
s2 = []
results = []
for op in ops:
    if isinstance(op, tuple):
        action, val = op
    else:
        action, val = op, None
    if action == "push":
        s1.append(val)
        _viz_enqueue(val)
    elif action in ("pop", "peek"):
        if not s2:
            while s1:
                popped = s1.pop()
                _viz_dequeue(popped)
                s2.append(popped)
        val = s2.pop() if action == "pop" else (s2[-1] if s2 else None)
        results.append(val)
return results
""",
    "input_unpack": "ops = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("val"), "locals": {"queue": locs.get("s1")}}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("popped"), "locals": {"queue": locs.get("s1")}}

recorder = Recorder()
return recorder.record(
    "_implement_queue_stack_instrumented",
    _implement_queue_stack_instrumented,
    ops,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "recent_calls",
    "title": "Number of Recent Calls",
    "topic": "queue",
    "difficulty": "easy",
    "renderer": "queue",
    "desc": "You have a RecentCounter class which counts the number of recent requests within a certain time frame.",
    "default_input": "[1, 100, 3001, 3002]",
    "params": "t_list",
    "code_lines": [
        "class RecentCounter:",
        "    def __init__(self):",
        "        self.q = []",
        "    def ping(self, t):",
        "        self.q.append(t)",
        "        while self.q[0] < t - 3000:",
        "            self.q.pop(0)",
        "        return len(self.q)",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
queue = []
res = []
for t in t_list:
    queue.append(t)
    _viz_enqueue(t)
    while queue and queue[0] < t - 3000:
        popped = queue.pop(0)
        _viz_dequeue(popped)
    res.append(len(queue))
return res
""",
    "input_unpack": "t_list = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("t"), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_recent_calls_instrumented",
    _recent_calls_instrumented,
    t_list,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "first_unique_char",
    "title": "First Unique Char in String",
    "topic": "queue",
    "difficulty": "easy",
    "renderer": "queue",
    "desc": "Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.",
    "default_input": '"loveleetcode"',
    "params": "s",
    "code_lines": [
        "def first_uniq_char(s):",
        "    counts = {}; q = []",
        "    for i, c in enumerate(s):",
        "        counts[c] = counts.get(c, 0) + 1",
        "        q.append((c, i))",
        "        while q and counts[q[0][0]] > 1:",
        "            q.pop(0)",
        "    return q[0][1] if q else -1",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
counts = {}
queue = []
for i, char in enumerate(s):
    counts[char] = counts.get(char, 0) + 1
    queue.append((char, i))
    _viz_enqueue(char)
    while queue and counts[queue[0][0]] > 1:
        popped = queue.pop(0)
        _viz_dequeue(popped[0])
return queue[0][1] if queue else -1
""",
    "input_unpack": "s = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("char"), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("popped")[0] if locs.get("popped") else "", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_first_unique_char_instrumented",
    _first_unique_char_instrumented,
    s,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "moving_average",
    "title": "Moving Average from Stream",
    "topic": "queue",
    "difficulty": "easy",
    "renderer": "queue",
    "desc": "Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.",
    "default_input": "([1, 10, 3, 5], 3)",
    "params": "val_list, size",
    "code_lines": [
        "class MovingAverage:",
        "    def __init__(self, size):",
        "        self.q = []; self.size = size; self.sum = 0",
        "    def next(self, val):",
        "        if len(self.q) == self.size:",
        "            self.sum -= self.q.pop(0)",
        "        self.q.append(val)",
        "        self.sum += val",
        "        return self.sum / len(self.q)",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
queue = []
curr_sum = 0
res = []
for val in val_list:
    if len(queue) == size:
        popped = queue.pop(0)
        _viz_dequeue(popped)
        curr_sum -= popped
    queue.append(val)
    _viz_enqueue(val)
    curr_sum += val
    res.append(curr_sum / len(queue))
return res
""",
    "input_unpack": "val_list, size = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("val"), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_moving_average_instrumented",
    _moving_average_instrumented,
    val_list, size,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "circular_queue",
    "title": "Design Circular Queue",
    "topic": "queue",
    "difficulty": "medium",
    "renderer": "queue",
    "desc": "Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the first position to make a circle.",
    "default_input": "(3, [('enq', 1), ('enq', 2), 'deq', ('enq', 3)])",
    "params": "size, ops",
    "code_lines": [
        "class MyCircularQueue:",
        "    def __init__(self, k):",
        "        self.q = [None] * k; self.head = -1; self.tail = -1; self.size = k",
        "    def enQueue(self, val):",
        "        if (self.tail + 1) % self.size == self.head: return False",
        "        if self.head == -1: self.head = 0",
        "        self.tail = (self.tail + 1) % self.size",
        "        self.q[self.tail] = val; return True",
        "    def deQueue(self):",
        "        if self.head == -1: return False",
        "        if self.head == self.tail: self.head = -1; self.tail = -1",
        "        else: self.head = (self.head + 1) % self.size",
        "        return True",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
queue = [None] * size
head = -1; tail = -1
res = []
for op in ops:
    if isinstance(op, tuple):
        action, val = op
    else:
        action, val = op, None
    if action == "enq":
        if (tail + 1) % size == head:
            res.append(False)
        else:
            if head == -1: head = 0
            tail = (tail + 1) % size
            queue[tail] = val
            _viz_enqueue(val)
            res.append(True)
    elif action == "deq":
        if head == -1:
            res.append(False)
        else:
            val = queue[head]
            queue[head] = None
            _viz_dequeue(val)
            if head == tail:
                head = -1; tail = -1
            else:
                head = (head + 1) % size
            res.append(True)
return res
""",
    "input_unpack": "size, ops = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("val"), "locals": {"queue": [x for x in locs.get("queue", []) if x is not None]}}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("val"), "locals": {"queue": [x for x in locs.get("queue", []) if x is not None]}}

recorder = Recorder()
return recorder.record(
    "_circular_queue_instrumented",
    _circular_queue_instrumented,
    size, ops,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "task_scheduler",
    "title": "Task Scheduler",
    "topic": "queue",
    "difficulty": "medium",
    "renderer": "queue",
    "desc": "Given a characters array tasks, representing the tasks a CPU needs to do, where each character represents a unique task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.",
    "default_input": '(["A", "A", "A", "B", "B", "B"], 2)',
    "params": "tasks, n",
    "code_lines": [
        "def least_interval(tasks, n):",
        "    counts = {}",
        "    for t in tasks: counts[t] = counts.get(t, 0) + 1",
        "    max_heap = [-v for v in counts.values()]",
        "    max_heap.sort()",
        "    q = [] # (cnt, idle_until)",
        "    time = 0",
        "    while max_heap or q:",
        "        time += 1",
        "        if max_heap:",
        "            cnt = max_heap.pop(0)",
        "            if cnt + 1 < 0: q.append((cnt + 1, time + n))",
        "        if q and q[0][1] == time:",
        "            max_heap.append(q.pop(0)[0])",
        "            max_heap.sort()",
        "    return time",
    ],
    "line_map": "{i: i for i in range(1, 17)}",
    "instrumented_body": """
counts = {}
for t in tasks: counts[t] = counts.get(t, 0) + 1
max_heap = [-v for v in counts.values()]
max_heap.sort()
queue = []
time = 0
while max_heap or queue:
    time += 1
    if max_heap:
        cnt = max_heap.pop(0)
        _viz_dequeue(cnt)
        if cnt + 1 < 0:
            queue.append((cnt + 1, time + n))
            _viz_enqueue(cnt + 1)
    if queue and queue[0][1] == time:
        item = queue.pop(0)
        _viz_dequeue(item)
        max_heap.append(item[0])
        max_heap.sort()
return time
""",
    "input_unpack": "tasks, n = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("cnt") if locs.get("cnt") is not None else 0, "locals": {"queue": [x[0] for x in locs.get("queue", [])]}}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("cnt") if locs.get("cnt") is not None else 0, "locals": {"queue": [x[0] for x in locs.get("queue", [])]}}

recorder = Recorder()
return recorder.record(
    "_task_scheduler_instrumented",
    _task_scheduler_instrumented,
    tasks, n,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "max_sliding_window_queue",
    "title": "Sliding Window Max (Deque)",
    "topic": "queue",
    "difficulty": "hard",
    "renderer": "queue",
    "desc": "Given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. Return the max sliding window.",
    "default_input": "([1, 3, -1, -3, 5, 3, 6, 7], 3)",
    "params": "nums, k",
    "code_lines": [
        "def max_sliding_window(nums, k):",
        "    q = []",
        "    res = []",
        "    for i, num in enumerate(nums):",
        "        while q and nums[q[-1]] < num: q.pop()",
        "        q.append(i)",
        "        if q[0] == i - k: q.pop(0)",
        "        if i >= k - 1: res.append(nums[q[0]])",
        "    return res",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
queue = []
res = []
for i, num in enumerate(nums):
    while queue and nums[queue[-1]] < num:
        queue.pop()
    queue.append(i)
    _viz_enqueue(i)
    if queue[0] == i - k:
        popped = queue.pop(0)
        _viz_dequeue(popped)
    if i >= k - 1:
        res.append(nums[queue[0]])
return res
""",
    "input_unpack": "nums, k = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("i"), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("popped"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_max_sliding_window_queue_instrumented",
    _max_sliding_window_queue_instrumented,
    nums, k,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "walls_and_gates",
    "title": "Walls and Gates (BFS)",
    "topic": "queue",
    "difficulty": "medium",
    "renderer": "queue",
    "desc": "Fill each empty cell in a grid with the distance to its nearest gate. If it is impossible, fill it with INF.",
    "default_input": "[[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]]",
    "params": "rooms",
    "code_lines": [
        "def walls_and_gates(rooms):",
        "    q = []",
        "    for r in range(len(rooms)):",
        "        for c in range(len(rooms[0])):",
        "            if rooms[r][c] == 0: q.append((r, c))",
        "    while q:",
        "        r, c = q.pop(0)",
        "        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:",
        "            nr, nc = r + dr, c + dc",
        "            if 0<=nr<len(rooms) and 0<=nc<len(rooms[0]) and rooms[nr][nc] == 2147483647:",
        "                rooms[nr][nc] = rooms[r][c] + 1; q.append((nr, nc))",
    ],
    "line_map": "{i: i for i in range(1, 12)}",
    "instrumented_body": """
rows = len(rooms)
cols = len(rooms[0])
queue = []
for r in range(rows):
    for c in range(cols):
        if rooms[r][c] == 0:
            queue.append((r, c))
            _viz_enqueue((r, c))
while queue:
    r, c = queue.pop(0)
    _viz_dequeue((r, c))
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
            rooms[nr][nc] = rooms[r][c] + 1
            queue.append((nr, nc))
            _viz_enqueue((nr, nc))
""",
    "input_unpack": "rooms = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("nr", locs.get("r")), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("r"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_walls_and_gates_instrumented",
    _walls_and_gates_instrumented,
    rooms,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})

problems_data.append({
    "id": "rotting_oranges",
    "title": "Rotting Oranges (BFS)",
    "topic": "queue",
    "difficulty": "medium",
    "renderer": "queue",
    "desc": "You are given an m x n grid where each cell can have one of three values: 0 empty, 1 fresh, or 2 rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange.",
    "default_input": "[[2, 1, 1], [1, 1, 0], [0, 1, 1]]",
    "params": "grid",
    "code_lines": [
        "def oranges_rotting(grid):",
        "    q = []; fresh = 0",
        "    for r in range(len(grid)):",
        "        for c in range(len(grid[0])):",
        "            if grid[r][c] == 2: q.append((r, c))",
        "            elif grid[r][c] == 1: fresh += 1",
        "    minutes = 0",
        "    while q and fresh > 0:",
        "        minutes += 1",
        "        for _ in range(len(q)):",
        "            r, c = q.pop(0)",
        "            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:",
        "                nr, nc = r+dr, c+dc",
        "                if 0<=nr<len(grid) and 0<=nc<len(grid[0]) and grid[nr][nc] == 1:",
        "                    grid[nr][nc] = 2; fresh -= 1; q.append((nr, nc))",
        "    return minutes if fresh == 0 else -1",
    ],
    "line_map": "{i: i for i in range(1, 17)}",
    "instrumented_body": """
rows = len(grid)
cols = len(grid[0])
queue = []
fresh = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            queue.append((r, c))
            _viz_enqueue((r, c))
        elif grid[r][c] == 1:
            fresh += 1
minutes = 0
while queue and fresh > 0:
    minutes += 1
    for _ in range(len(queue)):
        r, c = queue.pop(0)
        _viz_dequeue((r, c))
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc))
                _viz_enqueue((nr, nc))
return minutes if fresh == 0 else -1
""",
    "input_unpack": "grid = input_data",
    "run_handlers": """
def handle_enq(locs: dict, depth: int) -> dict | None:
    return {"type": "enqueue", "val": locs.get("nr", locs.get("r")), "locals": locs}
def handle_deq(locs: dict, depth: int) -> dict | None:
    return {"type": "dequeue", "val": locs.get("r"), "locals": locs}

recorder = Recorder()
return recorder.record(
    "_rotting_oranges_instrumented",
    _rotting_oranges_instrumented,
    grid,
    marker_fns={"_viz_enqueue", "_viz_dequeue"},
    nested_fns=set(),
    marker_handlers={
        "_viz_enqueue": handle_enq,
        "_viz_dequeue": handle_deq,
    }
)
"""
})


# =========================================================================
# LINKED LIST (10)
# =========================================================================

build_chain_helpers = """
def build_list(arr):
    if not arr: return None
    from neonodes.problems.base import ListNode
    nodes = [ListNode(val) for val in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    return nodes[0]

def build_list_cycle(arr, pos):
    if not arr: return None
    from neonodes.problems.base import ListNode
    nodes = [ListNode(val) for val in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    if pos >= 0 and pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0]
"""

problems_data.append({
    "id": "reverse_linked_list",
    "title": "Reverse Linked List",
    "topic": "linked_list",
    "difficulty": "easy",
    "renderer": "linked_list",
    "desc": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
    "default_input": "[1, 2, 3, 4]",
    "params": "head",
    "code_lines": [
        "def reverse_list(head):",
        "    prev = None",
        "    curr = head",
        "    while curr is not None:",
        "        nxt = curr.next",
        "        curr.next = prev",
        "        prev = curr",
        "        curr = nxt",
        "    return prev",
    ],
    "line_map": "{i: i for i in range(1, 10)}",
    "instrumented_body": """
prev = None
curr = head
while curr is not None:
    _viz_compare(curr)
    nxt = curr.next
    curr.next = prev
    _viz_link(curr, prev)
    prev = curr
    curr = nxt
    _viz_update(prev, curr)
return prev
""",
    "input_unpack": "head = build_list(input_data)",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_reverse_linked_list_instrumented",
    _reverse_linked_list_instrumented,
    head,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "merge_two_lists",
    "title": "Merge Two Sorted Lists",
    "topic": "linked_list",
    "difficulty": "easy",
    "renderer": "linked_list",
    "desc": "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists in a one sorted list.",
    "default_input": "([1, 3, 5], [2, 4, 6])",
    "params": "list1, list2",
    "code_lines": [
        "def merge_two_lists(list1, list2):",
        "    dummy = ListNode(0)",
        "    curr = dummy",
        "    while list1 and list2:",
        "        if list1.val <= list2.val:",
        "            curr.next = list1; list1 = list1.next",
        "        else:",
        "            curr.next = list2; list2 = list2.next",
        "        curr = curr.next",
        "    curr.next = list1 or list2",
        "    return dummy.next",
    ],
    "line_map": "{i: i for i in range(1, 12)}",
    "instrumented_body": """
from neonodes.problems.base import ListNode
dummy = ListNode(0)
curr = dummy
while list1 is not None and list2 is not None:
    _viz_compare(list1, list2)
    if list1.val <= list2.val:
        curr.next = list1
        _viz_link(curr, list1)
        list1 = list1.next
    else:
        curr.next = list2
        _viz_link(curr, list2)
        list2 = list2.next
    curr = curr.next
    _viz_update(curr, list1, list2)
if list1 is not None:
    curr.next = list1
    _viz_link(curr, list1)
elif list2 is not None:
    curr.next = list2
    _viz_link(curr, list2)
return dummy.next
""",
    "input_unpack": "list1 = build_list(input_data[0]); list2 = build_list(input_data[1])",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_merge_two_lists_instrumented",
    _merge_two_lists_instrumented,
    list1, list2,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "linked_list_cycle",
    "title": "Linked List Cycle",
    "topic": "linked_list",
    "difficulty": "easy",
    "renderer": "linked_list",
    "desc": "Given head, the head of a linked list, determine if the linked list has a cycle in it.",
    "default_input": "([1, 2, 3, 4], 1)",
    "params": "head",
    "code_lines": [
        "def has_cycle(head):",
        "    slow = head",
        "    fast = head",
        "    while fast and fast.next:",
        "        slow = slow.next",
        "        fast = fast.next.next",
        "        if slow == fast: return True",
        "    return False",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
slow = head
fast = head
while fast is not None and fast.next is not None:
    _viz_compare(slow, fast)
    slow = slow.next
    fast = fast.next.next
    _viz_update(slow, fast)
    if slow == fast:
        _viz_found(slow)
        return True
return False
""",
    "input_unpack": "head = build_list_cycle(input_data[0], input_data[1])",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_linked_list_cycle_instrumented",
    _linked_list_cycle_instrumented,
    head,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "remove_nth_from_end",
    "title": "Remove Nth Node From End",
    "topic": "linked_list",
    "difficulty": "medium",
    "renderer": "linked_list",
    "desc": "Given the head of a linked list, remove the nth node from the end of the list and return its head.",
    "default_input": "([1, 2, 3, 4, 5], 2)",
    "params": "head, n",
    "code_lines": [
        "def remove_nth_from_end(head, n):",
        "    dummy = ListNode(0, head)",
        "    slow = dummy; fast = dummy",
        "    for _ in range(n + 1): fast = fast.next",
        "    while fast is not None:",
        "        slow = slow.next; fast = fast.next",
        "    slow.next = slow.next.next",
        "    return dummy.next",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
from neonodes.problems.base import ListNode
dummy = ListNode(0, head)
slow = dummy
fast = dummy
for _ in range(n + 1):
    if fast: fast = fast.next
_viz_update(slow, fast)
while fast is not None:
    _viz_compare(slow, fast)
    slow = slow.next
    fast = fast.next
    _viz_update(slow, fast)
to_delete = slow.next
if to_delete:
    slow.next = to_delete.next
    _viz_link(slow, to_delete.next)
return dummy.next
""",
    "input_unpack": "head = build_list(input_data[0]); n = input_data[1]",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_remove_nth_from_end_instrumented",
    _remove_nth_from_end_instrumented,
    head, n,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "reorder_list",
    "title": "Reorder List",
    "topic": "linked_list",
    "difficulty": "medium",
    "renderer": "linked_list",
    "desc": "You are given the head of a singly linked-list. Reorder the list to be on the form L0 -> Ln -> L1 -> Ln-1 -> ...",
    "default_input": "[1, 2, 3, 4]",
    "params": "head",
    "code_lines": [
        "def reorder_list(head):",
        "    if not head: return",
        "    slow = head; fast = head",
        "    while fast and fast.next:",
        "        slow = slow.next; fast = fast.next.next",
        "    prev = None; curr = slow.next; slow.next = None",
        "    while curr:",
        "        nxt = curr.next; curr.next = prev; prev = curr; curr = nxt",
        "    l1, l2 = head, prev",
        "    while l1 and l2:",
        "        nxt1, nxt2 = l1.next, l2.next",
        "        l1.next = l2; l2.next = nxt1",
        "        l1, l2 = nxt1, nxt2",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
if not head: return
slow = head; fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

prev = None
curr = slow.next
slow.next = None
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
    
l1 = head
l2 = prev
while l1 and l2:
    _viz_compare(l1, l2)
    nxt1 = l1.next
    nxt2 = l2.next
    
    l1.next = l2
    _viz_link(l1, l2)
    l2.next = nxt1
    _viz_link(l2, nxt1)
    
    l1 = nxt1
    l2 = nxt2
    _viz_update(l1, l2)
""",
    "input_unpack": "head = build_list(input_data)",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_reorder_list_instrumented",
    _reorder_list_instrumented,
    head,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "copy_random_list",
    "title": "Copy List with Random Pointer",
    "topic": "linked_list",
    "difficulty": "medium",
    "renderer": "linked_list",
    "desc": "A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null. Construct a deep copy of the list.",
    "default_input": "[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]",
    "params": "head",
    "code_lines": [
        "def copy_random_list(head):",
        "    if not head: return None",
        "    curr = head; mapping = {}",
        "    while curr:",
        "        mapping[curr] = ListNode(curr.val)",
        "        curr = curr.next",
        "    curr = head",
        "    while curr:",
        "        node = mapping[curr]",
        "        if curr.next: node.next = mapping[curr.next]",
        "        if curr.random: node.random = mapping[curr.random]",
        "        curr = curr.next",
        "    return mapping[head]",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
if not head: return None
from neonodes.problems.base import ListNode
curr = head
mapping = {}
while curr:
    new_node = ListNode(curr.val)
    mapping[id(curr)] = new_node
    _viz_compare(curr)
    curr = curr.next

curr = head
while curr:
    new_node = mapping[id(curr)]
    nxt = curr.next
    rnd = curr.random
    if nxt: new_node.next = mapping[id(nxt)]
    if rnd: new_node.random = mapping[id(rnd)]
    _viz_link(new_node, new_node.next)
    curr = curr.next
    _viz_update(new_node)
return mapping[id(head)]
""",
    "input_unpack": "head = build_list_random(input_data)",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_copy_random_list_instrumented",
    _copy_random_list_instrumented,
    head,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": """
def build_list_random(arr):
    if not arr: return None
    from neonodes.problems.base import ListNode
    nodes = [ListNode(val[0]) for val in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    for i, val in enumerate(arr):
        rnd_idx = val[1]
        if rnd_idx is not None and rnd_idx >= 0 and rnd_idx < len(nodes):
            nodes[i].random = nodes[rnd_idx]
    return nodes[0]
"""
})

problems_data.append({
    "id": "add_two_numbers",
    "title": "Add Two Numbers",
    "topic": "linked_list",
    "difficulty": "medium",
    "renderer": "linked_list",
    "desc": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
    "default_input": "([2, 4, 3], [5, 6, 4])",
    "params": "l1, l2",
    "code_lines": [
        "def add_two_numbers(l1, l2):",
        "    dummy = ListNode(0)",
        "    curr = dummy; carry = 0",
        "    while l1 or l2 or carry:",
        "        v1 = l1.val if l1 else 0",
        "        v2 = l2.val if l2 else 0",
        "        total = v1 + v2 + carry",
        "        carry = total // 10",
        "        curr.next = ListNode(total % 10)",
        "        curr = curr.next",
        "        if l1: l1 = l1.next",
        "        if l2: l2 = l2.next",
        "    return dummy.next",
    ],
    "line_map": "{i: i for i in range(1, 14)}",
    "instrumented_body": """
from neonodes.problems.base import ListNode
dummy = ListNode(0)
curr = dummy
carry = 0
while l1 is not None or l2 is not None or carry > 0:
    _viz_compare(l1, l2)
    v1 = l1.val if l1 else 0
    v2 = l2.val if l2 else 0
    total = v1 + v2 + carry
    carry = total // 10
    new_node = ListNode(total % 10)
    curr.next = new_node
    _viz_link(curr, new_node)
    curr = new_node
    if l1: l1 = l1.next
    if l2: l2 = l2.next
    _viz_update(curr, l1, l2)
return dummy.next
""",
    "input_unpack": "l1 = build_list(input_data[0]); l2 = build_list(input_data[1])",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_add_two_numbers_instrumented",
    _add_two_numbers_instrumented,
    l1, l2,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "intersection_two_lists",
    "title": "Intersection of Two Lists",
    "topic": "linked_list",
    "difficulty": "easy",
    "renderer": "linked_list",
    "desc": "Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.",
    "default_input": "([4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3)",
    "params": "headA, headB",
    "code_lines": [
        "def get_intersection_node(headA, headB):",
        "    pA = headA; pB = headB",
        "    while pA != pB:",
        "        pA = pA.next if pA else headB",
        "        pB = pB.next if pB else headA",
        "    return pA",
    ],
    "line_map": "{i: i for i in range(1, 7)}",
    "instrumented_body": """
pA = headA
pB = headB
while pA != pB:
    _viz_compare(pA, pB)
    pA = pA.next if pA else headB
    pB = pB.next if pB else headA
    _viz_update(pA, pB)
_viz_found(pA)
return pA
""",
    "input_unpack": "headA, headB = build_intersect_lists(input_data[0], input_data[1], input_data[2], input_data[3])",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_found(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_intersection_two_lists_instrumented",
    _intersection_two_lists_instrumented,
    headA, headB,
    marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_update": handle_update,
        "_viz_found": handle_found,
    }
)
""",
    "extra_helpers": """
def build_intersect_lists(arrA, arrB, skipA, skipB):
    if not arrA or not arrB: return None, None
    from neonodes.problems.base import ListNode
    nodesA = [ListNode(val) for val in arrA[:skipA]]
    nodesB = [ListNode(val) for val in arrB[:skipB]]
    nodesCommon = [ListNode(val) for val in arrA[skipA:]]
    
    for i in range(len(nodesA) - 1): nodesA[i].next = nodesA[i+1]
    for i in range(len(nodesB) - 1): nodesB[i].next = nodesB[i+1]
    for i in range(len(nodesCommon) - 1): nodesCommon[i].next = nodesCommon[i+1]
    
    if nodesCommon:
        if nodesA: nodesA[-1].next = nodesCommon[0]
        else: nodesA = nodesCommon
        if nodesB: nodesB[-1].next = nodesCommon[0]
        else: nodesB = nodesCommon
    return nodesA[0] if nodesA else None, nodesB[0] if nodesB else None
"""
})

problems_data.append({
    "id": "palindrome_linked_list",
    "title": "Palindrome Linked List",
    "topic": "linked_list",
    "difficulty": "easy",
    "renderer": "linked_list",
    "desc": "Given the head of a singly linked list, return true if it is a palindrome or false otherwise.",
    "default_input": "[1, 2, 2, 1]",
    "params": "head",
    "code_lines": [
        "def is_palindrome(head):",
        "    vals = []",
        "    curr = head",
        "    while curr:",
        "        vals.append(curr.val)",
        "        curr = curr.next",
        "    return vals == vals[::-1]",
    ],
    "line_map": "{i: i for i in range(1, 8)}",
    "instrumented_body": """
vals = []
curr = head
while curr:
    _viz_compare(curr)
    vals.append(curr.val)
    curr = curr.next
return vals == vals[::-1]
""",
    "input_unpack": "head = build_list(input_data)",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_palindrome_linked_list_instrumented",
    _palindrome_linked_list_instrumented,
    head,
    marker_fns={"_viz_compare"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

problems_data.append({
    "id": "odd_even_list",
    "title": "Odd Even Linked List",
    "topic": "linked_list",
    "difficulty": "medium",
    "renderer": "linked_list",
    "desc": "Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.",
    "default_input": "[1, 2, 3, 4, 5]",
    "params": "head",
    "code_lines": [
        "def odd_even_list(head):",
        "    if not head: return None",
        "    odd = head; even = head.next; even_head = even",
        "    while even and even.next:",
        "        odd.next = even.next; odd = odd.next",
        "        even.next = odd.next; even = even.next",
        "    odd.next = even_head",
        "    return head",
    ],
    "line_map": "{i: i for i in range(1, 9)}",
    "instrumented_body": """
if not head: return None
odd = head
even = head.next
even_head = even
while even and even.next:
    _viz_compare(odd, even)
    odd.next = even.next
    _viz_link(odd, even.next)
    odd = odd.next
    
    even.next = odd.next
    _viz_link(even, odd.next)
    even = even.next
    _viz_update(odd, even)
odd.next = even_head
_viz_link(odd, even_head)
return head
""",
    "input_unpack": "head = build_list(input_data)",
    "run_handlers": """
def handle_compare(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}
def handle_link(locs: dict, depth: int) -> dict | None:
    return {"type": "link_update", "locals": locs}
def handle_update(locs: dict, depth: int) -> dict | None:
    return {"type": "pointer_update", "locals": locs}

recorder = Recorder()
return recorder.record(
    "_odd_even_list_instrumented",
    _odd_even_list_instrumented,
    head,
    marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
    nested_fns=set(),
    marker_handlers={
        "_viz_compare": handle_compare,
        "_viz_link": handle_link,
        "_viz_update": handle_update,
    }
)
""",
    "extra_helpers": build_chain_helpers
})

# Write the python modules
for p in problems_data:
    filename = f"{p['id']}.py"
    filepath = os.path.join(problems_dir, filename)
    
    extra_h = p.get("extra_helpers", "")
    
    # Dedent the bodies to strip common indentation first, then add 4 spaces
    clean_body = textwrap.dedent(p['instrumented_body'].strip("\n"))
    indented_body = "\n".join("    " + line if line else "" for line in clean_body.split("\n"))
    
    clean_run = textwrap.dedent(p['run_handlers'].strip("\n"))
    indented_run = "\n".join("    " + line if line else "" for line in clean_run.split("\n"))
    
    content = f"""\"\"\"{p['title']} — Neonodes visualizer problem module.\"\"\"
from __future__ import annotations
from neonodes.recorder import Recorder

TITLE = {repr(p['title'])}
CATEGORY = {repr(p['topic'])}
DIFFICULTY = {repr(p['difficulty'])}
RENDERER = {repr(p['renderer'])}
DESCRIPTION = {repr(p['desc'])}
DEFAULT_INPUT = {p['default_input']}

CODE_LINES = {repr(p['code_lines'])}
_LINE_MAP = {p['line_map']}

# Dummy visualization markers
def _viz_compare(*args, **kwargs): pass
def _viz_update(*args, **kwargs): pass
def _viz_found(*args, **kwargs): pass
def _viz_push(*args, **kwargs): pass
def _viz_pop(*args, **kwargs): pass
def _viz_peek(*args, **kwargs): pass
def _viz_enqueue(*args, **kwargs): pass
def _viz_dequeue(*args, **kwargs): pass
def _viz_link(*args, **kwargs): pass

{extra_h}

def _{p['id']}_instrumented({p['params']}):
{indented_body}

def run(input_data):
    {p['input_unpack'].strip()}
{indented_run}
"""
    
    with open(filepath, "w") as f:
        f.write(content)

print(f"Generated {len(problems_data)} problem modules in {problems_dir}.")
