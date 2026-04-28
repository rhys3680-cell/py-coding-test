"""D2 sorted(key=lambda) 드릴 솔루션."""


# D2-1: 튜플 두 번째 원소 오름차순
arr = [(1, 30), (2, 10), (3, 20)]
print(sorted(arr, key=lambda x: x[1]))
# [(2, 10), (3, 20), (1, 30)]


# D2-2: 문자열 길이순
words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words, key=len))
# ['fig', 'kiwi', 'apple', 'banana']
# (key=len 처럼 key는 함수면 무엇이든 OK. lambda 안 써도 됨)


# D2-3: 절댓값 기준
arr = [-5, 3, -1, 4, -2]
print(sorted(arr, key=abs))
# [-1, -2, 3, 4, -5]
# (abs 자체가 함수)


# D2-4: dict items, value 내림차순
d = {"a": 3, "b": 1, "c": 2}
print(sorted(d.items(), key=lambda kv: kv[1], reverse=True))
# [('a', 3), ('c', 2), ('b', 1)]


# D2-5: 첫째 오름 + 같으면 둘째 내림
arr = [(1, 2), (1, 5), (2, 3), (1, 1)]
print(sorted(arr, key=lambda x: (x[0], -x[1])))
# [(1, 5), (1, 2), (1, 1), (2, 3)]
# 핵심: 둘째 키 내림 = 음수 부호 -x[1]
# (모든 원소가 내림이면 reverse=True가 더 깔끔, 일부만 내림이면 -부호)


# D2-6: 길이 우선 + 같은 길이는 알파벳
words = ["bb", "a", "ccc", "ab", "ba"]
print(sorted(words, key=lambda w: (len(w), w)))
# ['a', 'ab', 'ba', 'bb', 'ccc']
# 튜플 비교: 첫째 같으면 둘째로


# D2-7: dict value 정렬해서 key만
d = {"a": 3, "b": 1, "c": 2}
print([k for k, v in sorted(d.items(), key=lambda kv: kv[1])])
# ['b', 'c', 'a']
# 정렬 후 컴프리헨션으로 key 추출


# D2-8: 마지막 글자 기준
words = ["apple", "banana", "kiwi"]
print(sorted(words, key=lambda w: w[-1]))
# ['banana', 'apple', 'kiwi']
# 음수 인덱싱으로 마지막 글자


# D2-9: 점수 내림 + 같으면 이름 오름
scores = [("Tom", 90), ("Anna", 90), ("Bob", 85)]
print(sorted(scores, key=lambda x: (-x[1], x[0])))
# [('Anna', 90), ('Tom', 90), ('Bob', 85)]
# 점수만 내림이라 -x[1], 이름은 그대로 x[0]


# D2-10: 42889 핵심 패턴
rates = [(1, 0.5), (2, 0.8), (3, 0.5), (4, 0.0)]
print(sorted(rates, key=lambda x: (-x[1], x[0])))
# [(2, 0.8), (1, 0.5), (3, 0.5), (4, 0.0)]
# fail_rate 내림 + stage_id 오름 = (-x[1], x[0])