# D1 — Counter 드릴

`collections.Counter` 자동화용 10문제.

## 사전 지식 (30초 훑기)

```python
from collections import Counter

c = Counter("mississippi")
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

c.most_common(2)          # [('i', 4), ('s', 4)]  상위 n개
c.most_common()[-1]       # 최하위
c["x"]                    # 없는 키 → 0 (자동 기본값)
c1 + c2                   # 합산
c1 - c2                   # 뺄셈 (음수는 제거)
c1 & c2                   # 교집합 (min)
c1 | c2                   # 합집합 (max)
c.subtract(other)         # in-place 뺄셈
len(c)                    # 유일 원소 수
sum(c.values())           # 전체 원소 수
```

## 드릴

각 문제 **한 줄**로 풀이. 시간 측정.

---

### D1-1
**문자열 `"mississippi"`에서 가장 많이 나온 글자**를 반환.

```python
s = "mississippi"
# expected: 'i' (또는 's' — 둘 다 4회, 출현 순서상 'i')

answer = 
# 30s
from collections import Counter

s = "mississippi"

def solution(s):
    return Counter(s).most_common(1)
```

---

### D1-2
**리스트 `[1, 2, 2, 3, 3, 3]`의 각 숫자 등장 횟수**를 dict처럼 반환.

```python
arr = [1, 2, 2, 3, 3, 3]
# expected: Counter({3: 3, 2: 2, 1: 1})

answer =

# 1m 16s
from collections import Counter

arr = [1, 2, 2, 3, 3, 3]


def solution(arr):
    return Counter(arr)

```

---

### D1-3
**리스트 A에만 있는 원소 (중복 포함)** — Counter 뺄셈 활용.

```python
A = ["a", "a", "b", "c"]
B = ["a", "b"]
# expected: Counter({'a': 1, 'c': 1})   → 즉 ['a', 'c'] 1개씩 남음

answer =
# 1m 47s
from collections import Counter

A = ["a", "a", "b", "c"]
B = ["a", "b"]


def solution(a, b):
    return Counter(a) - Counter(b)

```


---

### D1-4
**문자열에서 가장 많이 나온 글자 Top 3**을 `[(글자, 개수), ...]` 형태로.

```python
s = "abracadabra"
# expected: [('a', 5), ('b', 2), ('r', 2)]

answer =
# 1m 14s

from collections import Counter

s = "abracadabra"


def solution(s):
    return Counter(s).most_common(3)


```

---

### D1-5
**리스트에서 가장 많이 나온 원소 자체만** 반환 (Top 1의 값).

```python
arr = [1, 2, 2, 3, 3, 3]
# expected: 3

answer =
# 3m 34s
from collections import Counter

arr = [1, 2, 2, 3, 3, 3]


def solution(arr):
    return Counter(arr).most_common(1)[0][0]

```

---

### D1-6
**두 단어가 애너그램**인지 판정 (같은 글자 구성).

```python
a = "listen"
b = "silent"
# expected: True

answer =
# 2m 36s
from collections import Counter

a = "listen"
b = "silent"


a = Counter(a) - Counter(b)


def solution(a, b):
    return len(Counter(a) - Counter(b)) == 0


```

---

### D1-7
**중복 제거하되 순서 보존** — Counter보다 dict가 쉽지만, Counter로도 가능한지 연습.

```python
arr = ["a", "b", "a", "c", "b"]
# expected: ['a', 'b', 'c']

# Hint: dict.fromkeys 또는 Counter 순서 보존(3.7+) 활용
answer =
# 모르겠음
from collections import Counter

arr = ["a", "b", "a", "c", "b"]


a = list(Counter(arr))

a1 = dict.fromkeys(arr)

b = list(dict.fromkeys(arr))

print(a1)

```

---

### D1-8
**가장 많이 나온 원소의 등장 횟수** (값만).

```python
arr = [1, 1, 2, 2, 2, 3]
# expected: 3  (원소 2가 3번)

answer =
# 1m
from collections import Counter

arr = [1, 1, 2, 2, 2, 3]

a = Counter(arr).most_common(1)[0][1]

print(a)


def solution(arr):
    return Counter(arr).most_common(1)[0][1]



```

---

### D1-9
**딱 한 번만 나온 원소들** 리스트.

```python
arr = [1, 2, 2, 3, 4, 4, 5]
# expected: [1, 3, 5]

answer =
# 모르겠음

from collections import Counter

arr = [1, 2, 2, 3, 4, 4, 5]


a = Counter(arr).items()


def solution(arr):
    return [k for k, v in Counter(arr).items() if v == 1]


print(solution(arr))

```

---

### D1-10
**두 Counter 뺄셈으로 참가자 중 완주 못 한 사람 찾기** (42576 재현).

```python
participant = ["mislav", "stanko", "mislav", "ana"]
completion = ["stanko", "ana", "mislav"]
# expected: "mislav"

answer =
# 4m 37s

from collections import Counter

participant = ["mislav", "stanko", "mislav", "ana"]
completion = ["stanko", "ana", "mislav"]

p = Counter(participant)
c = Counter(completion)

result = p - c

print(result.most_common(1)[0][0])


def solution(p, c):
    return (Counter(p) - Counter(c)).most_common(1)[0][0]


print(solution(participant, completion))

```

---

## 마치고

- 각 문제 소요 시간 측정
- 다 풀면 [solutions/D1_counter.py](solutions/D1_counter.py) 와 비교
- 헷갈렸던 문제 번호 `log.jsonl`에 기록

## 채점 기준
- **전부 90초 이내**: 해당 도구 자동화 도달 🎉
- **2~3개 이상 막힘**: 3일 뒤 같은 드릴 재풀이
- **5개 이상 막힘**: 사전 지식 섹션 다시 읽고 내일 재풀이