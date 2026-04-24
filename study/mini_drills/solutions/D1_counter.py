"""D1 Counter 드릴 솔루션.

각 솔루션은 '가장 파이써닉한 한 줄' 기준.
다른 풀이 가능하지만, 체화 목표는 이 버전.
"""

from collections import Counter


# D1-1: 가장 많이 나온 글자
s = "mississippi"
print(Counter(s).most_common(1)[0][0])
# 'i'


# D1-2: 각 숫자 등장 횟수
arr = [1, 2, 2, 3, 3, 3]
print(Counter(arr))
# Counter({3: 3, 2: 2, 1: 1})


# D1-3: A에만 있는 원소 (중복 포함)
A = ["a", "a", "b", "c"]
B = ["a", "b"]
print(Counter(A) - Counter(B))
# Counter({'a': 1, 'c': 1})


# D1-4: 가장 많이 나온 글자 Top 3
s = "abracadabra"
print(Counter(s).most_common(3))
# [('a', 5), ('b', 2), ('r', 2)]


# D1-5: 가장 많이 나온 원소 자체
arr = [1, 2, 2, 3, 3, 3]
print(Counter(arr).most_common(1)[0][0])
# 3


# D1-6: 애너그램 판정
a = "listen"
b = "silent"
print(Counter(a) == Counter(b))
# True
# (sorted(a) == sorted(b) 도 가능. Counter가 더 빠름 O(n) vs O(n log n))


# D1-7: 중복 제거, 순서 보존
arr = ["a", "b", "a", "c", "b"]
print(list(Counter(arr)))
# ['a', 'b', 'c']
# (Counter는 dict라 3.7+ 삽입 순서 보존. list()하면 키만 순서대로)
# 대안: list(dict.fromkeys(arr))  — dict.fromkeys가 더 표준적


# D1-8: 가장 많이 나온 원소의 등장 횟수
arr = [1, 1, 2, 2, 2, 3]
print(Counter(arr).most_common(1)[0][1])
# 3
# 대안: max(Counter(arr).values())


# D1-9: 한 번만 나온 원소들
arr = [1, 2, 2, 3, 4, 4, 5]
print([k for k, v in Counter(arr).items() if v == 1])
# [1, 3, 5]


# D1-10: 참가자 중 완주 못 한 사람 (42576)
participant = ["mislav", "stanko", "mislav", "ana"]
completion = ["stanko", "ana", "mislav"]
print((Counter(participant) - Counter(completion)).most_common(1)[0][0])
# 'mislav'
# 대안: list(Counter(participant) - Counter(completion))[0]