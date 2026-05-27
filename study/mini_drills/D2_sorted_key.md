# D2 — sorted(key=lambda) 드릴

`sorted(..., key=lambda)` 자동화용 10문제.

42889 실패율에서 막힌 핵심 도구. **lambda + 정렬 기준 지정**이 본 드릴 목표.

## 사전 지식 (30초 훑기)

```python
# 기본 정렬 (오름차순)
sorted([3, 1, 2])                    # [1, 2, 3]
sorted([3, 1, 2], reverse=True)      # [3, 2, 1]

# key= 함수로 정렬 기준 지정
sorted(["abc", "ab", "abcd"], key=len)        # ['ab', 'abc', 'abcd']
sorted([(1, 2), (3, 1), (2, 3)], key=lambda x: x[1])
# [(3, 1), (1, 2), (2, 3)]   ← 두 번째 원소 기준

# 다중 기준 (튜플로)
sorted(arr, key=lambda x: (x[0], -x[1]))
# 첫째 키 오름, 둘째 키 내림 (음수 부호로)

# dict 정렬
sorted(d.items(), key=lambda kv: kv[1])
# (key, value) 튜플의 value 기준

# 문자열 길이순, 같으면 사전순
sorted(words, key=lambda w: (len(w), w))
```

**lambda 형식**: `lambda 매개변수: 반환값` — 한 줄 익명 함수.

---

## 드릴

각 문제 **한 줄**로 풀이. 시간 측정.

---

### D2-1
**튜플 리스트를 두 번째 원소 기준 오름차순**.

```python
arr = [(1, 30), (2, 10), (3, 20)]
# expected: [(2, 10), (3, 20), (1, 30)]

answer = sorted(arr, key=lambda x: x[1])

# 20s
```

---

### D2-2
**문자열 리스트를 길이순**으로 정렬.

```python
words = ["banana", "kiwi", "apple", "fig"]
# expected: ['fig', 'kiwi', 'apple', 'banana']

answer = sorted(words, key=len)
# 20s 
# 2 try
```

---

### D2-3
**리스트를 절댓값 기준** 오름차순.

```python
arr = [-5, 3, -1, 4, -2]
# expected: [-1, -2, 3, 4, -5]

answer = sorted(arr, key=lambda x: abs(x))
# 20s
```

---

### D2-4
**dict의 (key, value) 쌍을 value 기준 내림차순**으로.

```python
d = {"a": 3, "b": 1, "c": 2}


answer = sorted(d.items(), key=lambda kv: kv[1])
```

```python
d = {"a": 3, "b": 1, "c": 2}
# expected: [('a', 3), ('c', 2), ('b', 1)]

answer = sorted(d, key=lambda kv: kv[1])
# 딕셔너리 인덱싱을 어떻게 해야할지 모르겠어
# 2m 54s
# 3 try
```

---

### D2-5
**튜플 리스트, 첫 번째 원소 오름차순 + 같으면 두 번째 원소 내림차순**.

```python
arr = [(1, 2), (1, 5), (2, 3), (1, 1)]
# expected: [(1, 5), (1, 2), (1, 1), (2, 3)]

answer = sorted(arr, key=lambda x:( x[0], -x[1]))

# 3 try
# 2m 42s
```

---

### D2-6
**문자열 리스트를 사전순 + 같은 길이끼리는 알파벳순**.
(즉 길이 우선, 같으면 알파벳)

```python
words = ["bb", "a", "ccc", "ab", "ba"]
# expected: ['a', 'ab', 'ba', 'bb', 'ccc']

answer = sorted(words, key=lambda x: (len(x), x))

# 3 try
# 2m 43s
```

---

### D2-7
**dict를 value 기준 정렬해서 key 리스트만** 반환.

```python
d = {"a": 3, "b": 1, "c": 2}
# expected: ['b', 'c', 'a']

answer = answer = [el[0] for el in sorted(d.items(), key=lambda kv: kv[1])]

# 3m 32s
# 1 try
```

---

### D2-8
**리스트를 마지막 글자 기준** 정렬.

```python
words = ["apple", "banana", "kiwi"]
# 끝글자: e, a, i → 정렬: a < e < i
# expected: ['banana', 'apple', 'kiwi']

answer = sorted(words, key=lambda x: x[-1])

# 30s
# 1 try
```

---

### D2-9
**튜플 리스트 (이름, 점수)를 점수 내림차순 + 같으면 이름 오름차순**.

```python
scores = [("Tom", 90), ("Anna", 90), ("Bob", 85)]
# expected: [('Anna', 90), ('Tom', 90), ('Bob', 85)]

answer = sorted(scores, key=lambda x: (-x[1], x[0]))
# 이제 적응되서 시간 측정 X
```

---

### D2-10
**42889 핵심 패턴**: `[(stage_id, fail_rate), ...]`을 **fail_rate 내림차순 + 같으면 stage_id 오름차순**.

```python
rates = [(1, 0.5), (2, 0.8), (3, 0.5), (4, 0.0)]
# expected: [(2, 0.8), (1, 0.5), (3, 0.5), (4, 0.0)]

answer = sorted(rates, key=lambda x: (-x[1], x[0]))
```

---

## 마치고

- 각 문제 소요 시간 측정
- 다 풀면 [solutions/D2_sorted_key.py](solutions/D2_sorted_key.py) 와 비교
- 헷갈렸던 문제 번호 `log.jsonl`에 기록

## 채점 기준
- **전부 90초 이내**: 자동화 도달 🎉
- **2~3개 막힘**: 3일 뒤 재풀이
- **5개 이상 막힘**: 사전 지식 다시 + 내일 재풀이

## 핵심 패턴 정리
- 단일 키: `key=lambda x: x[i]`
- 다중 키: `key=lambda x: (x[0], x[1])`
- 내림차순: `reverse=True` 또는 **음수 부호 `-x[i]`** (다중 키 일부만 내림 시)
- dict 정렬: `sorted(d.items(), key=lambda kv: kv[1])`
