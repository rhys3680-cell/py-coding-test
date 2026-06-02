# Phase 1 - Session 1 Revisit (양식 v2): 문제 3, 4 재풀이

**목적**: s1에서 알고리즘 결함이 발견된 문제 3, 4를 양식 v2 (Invariant 중심)로 다시 풀이.

**선행 학습**: [loop_invariants.md](../loop_invariants.md) 먼저 읽기.

---

## 양식 v2 (Invariant 중심)

```
[1] 문제

[2] 손풀이 (작은 입력 1개로 표 그리기):
    | i | 본 값 | 변수1 | 변수2 | ... |
    종료 → 답: ?

[3] Invariant (한 문장):
    "i번째 원소까지 본 시점에, [변수들]은 [관계]를 만족한다"

    체크리스트:
    - [ ] 문제의 "최대", "중복", "처음" 같은 키워드가 명제에 들어갔나?
    - [ ] 변수가 아니라 변수 사이 "관계"를 적었나?

[4] 3-부분 점검:
    (a) 초기화: 시작 시 명제 참?
    (b) 유지: 한 번 돌고도 명제 참?
    (c) 종료: 끝났을 때 명제가 답을 알려주는가?

[5] 파이썬 코드:
    (a) → 변수 초기화
    (b) → 루프 본문
    (c) → return
```

**경고**: [5]를 먼저 머릿속에 그리지 말기. [3]에 시간 들이기. [3]이 잘 잡히면 [4](b)와 [5]는 거의 자동.

---

## 문제 3: 두 배열의 교집합 개수

두 배열 `a`, `b`에서 **양쪽 모두에 있는** 원소의 개수.
중복은 한 번만 카운트.

```python
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
# expected: 2  (3과 4만 양쪽에 있음)
```

**제약**: `set` 연산자(`&`) 쓰지 말기. 직접 탐색.

### 본인의 s1 풀이 약점 (참고)

- [3]에 "중복 한 번만" 누락 → `seen` 변수 없음
- 이중 for 루프로 우회 (O(n\*m))
- 둘째 코드가 수식 사고 재발 (over-engineering)

### 풀이 (양식 v2)

```
[2] 손풀이 (a=[1,2,3,4], b=[3,4,5,6]):
    | i | a[i] | a[i] in b? | seen 전 | seen에 새로? | cnt |
    | 0 | 1    | 아니         | {}        | 아니           | 0   |
    | 1 | 2    | 아니         | {}        | 아니           | 0   |
    | 2 | 3    | 예          | {}        | 예 (추가)     | 1   |
    | 3 | 4    | 예          | {3}       | 예 (추가)     | 2   |
    종료 → 답: 2

[3] Invariant:
i번째 원소까지 본 시점에
    seen = a[0..i] 중 b에 있는 원소들의 집합이고
    cnt = seen의 크기이다

[4] 3-부분 점검:
    (a) 초기화:
        i == 0일 때 [3]이 참이려면?
        만약 a[0] in b 라면
            seen = a[0]
            cnt += 1 할 수도 있고 아니면 마지막에 len(seen)으로 구할 수도 있음
        아니라면
            pass

    (b) 유지:
        uv
    (c) 종료:

[5] 파이썬 코드:
def solution(a, b):
    pass
```

---

## 문제 4: 가장 긴 연속 같은 값의 길이

배열에서 같은 값이 연속으로 나오는 가장 긴 구간의 길이.

```python
arr = [1, 1, 2, 2, 2, 3, 1, 1, 1, 1]
# expected: 4  (마지막 1이 4번 연속)
```

**반례 확인용 입력**: `[1, 1, 1, 1, 2]` → expected: 4

**제약**: `itertools.groupby` 쓰지 말기. 직접 추적.

### 본인의 s1 풀이 약점 (참고)

- [3]에 "가장 긴" 누락 → `max_len` 변수 없음
- 결과 코드가 마지막 그룹 길이만 반환 (틀린 알고리즘)
- `[1,1,1,1,2]` 입력에서 1 반환 (정답 4)

### 풀이 (양식 v2)

```
[2] 손풀이 (arr = [1, 1, 2, 2, 2, 3]):
    | i | 본 값 | current_val | current_len | max_len |
    | 0 | 1     | 1           | 1           | 1       |
    | 1 | 1     | 1           | 2           | 2       |
    | 2 | 2     | 2           | 1           | 2       |
    | 3 | 2     | 2           | 2           | 2       |
    | 4 | 2     | 2           | 3           | 3       |
    | 5 | 3     | 3           | 1           | 3       |
    종료 → 답: ?

[3] Invariant:
    "i번째 원소까지 본 시점에, current_val은 arr[i]이고 current_len는 arr[i]로 끝나는 연속으로 같은 값의 길이이고 max_len = arr[0..i] 중 가장 긴 연속으로 같은 값의 길이이다."


[4] 3-부분 점검:
    (a) 초기화:
        i = 0 시점에 [3]이 참이려면?
            current_val = arr[0]
            current_len = 1
            max_len = current_len
    (b) 유지:
        arr[i+1] == current_val일 때 →
            current_val 그대로
            current_len += 1
        arr[i+1] != current_val일 때 →
            current_val = arr[i+1]
            current_len = 1
        양쪽 모두:
            max_len = max(max_len, current_len)
    (c) 종료:
        루프 끝나면 max_len을 return

[5] 파이썬 코드:
def solution(arr: list):
    # 값(value)은 arr[0]로 대체
    current_val = arr[0]
    # 길이(length)는 단순 숫자를 의미
    # 단순 1로 초기화
    current_len = 1
    # max_len도 초기화 단계에는 단순 1로 초기화
    # current_len으로 초기화하는 게 더 가독성 ↑
    # 메모리 주소를 공유하지 않나?
    max_len = current_len

    # 다음 인덱스를 알아야하기 때문에 enumerate로
    for i, _ in enumerate(arr):
        # 표와 일치하기 위해서 print로 확인
        # print(i, el, current_val, current_len, max_len)
        if i == len(arr) - 1:
            return max_len

        if arr[i + 1] == current_val:
            current_len += 1
        else:
            current_val = arr[i + 1]
            current_len = 1

        max_len = max(current_len, max_len)

    return
```

---

## 마치고

- 5단계 다 채웠는지 점검
- 특히 [3] Invariant 한 문장에 시간 들였는지
- [solutions/s1r_search_v2.py](solutions/s1r_search_v2.py) 와 비교
- 가장 시간 들인 단계 = 본인 약점 신호

## 자가 점검

각 문제 끝나고 자문:

- [3] Invariant에 문제 조건의 모든 키워드가 들어갔나?
  - 문제 3: "중복은 한 번만"이 명제에 있나?
  - 문제 4: "가장 긴"이 명제에 있나?
- [4] (a)(b)(c) 점검 후 [5] 코드가 자동으로 따라왔나?
  - 아니면 [3]이 부족했다는 신호.
- 막힘 신호 있었을 때 멈춰서 [3]을 재정의했나?
  - 다른 접근으로 옮겨갔다면 다음에는 멈춤 훈련.
