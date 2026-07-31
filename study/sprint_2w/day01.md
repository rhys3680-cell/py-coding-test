# Day 1 — 구현 / 시뮬레이션 (2026-07-31)

**오늘 목표**: 6주 공백 후 감각 복구. 이미 강한 유형이니 **속도**만 본다.

**규칙**: 문제당 시간 적기. 20분 막히면 [solutions/day01.py](solutions/day01.py) 열기.
5단계 양식 **안 쓴다**. 막혔을 때만 [loop_invariants.md](../algo_thinking/loop_invariants.md).

---

## 워밍업 (10분) — 문제 A: 두 번째로 작은 수

`s_memory_check_2`에서 미완으로 남은 문제. 그대로 가져왔다.

배열 `arr`에서 **두 번째로 작은 수**를 반환. 없으면 `None`.

```python
arr = [3, 1, 4, 1, 5, 9, 2, 6]
# expected: 2
```

**중복 처리**: 같은 값은 한 번만.

- `[1, 1, 3]` → 3
- `[1, 1]` → None
- `[5]` → None

**제약**: `sorted`, `set` 금지. 한 번 순회.

> 주의: 지난번 손풀이에서 **"작은"을 "큰"으로 읽고** big/second를 큰 쪽으로
> 추적했다. 문제 문장을 한 번 더 읽고 시작할 것.

### 풀이 A

```python
def solution_a(arr):
    big = min(arr[0], arr[1])
    second = max(arr[0], arr[1])

    for el in arr:
        if el <= big:
            big = el
        elif el <= second:
            second = el
        else:
            pass

    return second

# 시간:
```

---

## 신규 (30분) — 문제 B: 달팽이 배열

`n`이 주어지면 1부터 `n*n`까지를 **시계 방향 나선**으로 채운 2차원 배열을 반환.

```python
n = 3
# expected:
# [[1, 2, 3],
#  [8, 9, 4],
#  [7, 6, 5]]

n = 4
# expected:
# [[ 1,  2,  3,  4],
#  [12, 13, 14,  5],
#  [11, 16, 15,  6],
#  [10,  9,  8,  7]]
```

**왜 이 문제**: 구현 유형의 대표. "방향 전환"을 코드로 옮기는 게 핵심이고,
이건 코테 구현 문제의 절반이 요구하는 감각이다.

**힌트가 필요하면 여기까지만 보기**:

> 방향을 `dr, dc` 리스트로 두고 "벽에 닿거나 이미 채워졌으면 방향 전환"

### 풀이 B

```python
def solution_b(n):
    pass


# 시간:
# 막힌 지점:
```

---

## 오늘 끝나고

[log.jsonl](log.jsonl)에 한 줄:

```json
{"date":"2026-07-31","day":1,"type":"구현","solved":?,"stuck":null,"min":?,"note":""}
```

풀고 나서 [solutions/day01.py](solutions/day01.py)와 비교.
