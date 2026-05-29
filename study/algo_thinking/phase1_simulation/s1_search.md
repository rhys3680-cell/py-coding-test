# Phase 1 - Session 1: 단순 탐색

**목표**: 사고 전환 5단계 양식 처음 적용. 알고리즘은 매우 단순한 거.

## 양식 (모든 문제 공통)

```
[1] 문제 (제시됨)

[2] 사람으로 풀이 (작은 예시로 손풀이):
   한국말로 3~5줄.
   "왼쪽부터 본다... 비교한다... 갱신한다..." 식.

[3] 상태 변수:
   - 변수명: 의미
   - 초기값
   - 언제 갱신

[4] 의사 코드:
   3~5줄. 파이썬 비슷하지만 한국말 섞여도 OK.

[5] 파이썬 코드:
   동작하는 코드.
```

**시간 측정 권장**: [2]~[5] 각 단계 따로 (선택).

---

## 문제 1: 배열 최댓값

배열 `arr`가 주어질 때 가장 큰 원소를 반환.
**제약**: `max()` 함수 쓰지 말기. 직접 탐색.

```python
arr = [3, 1, 4, 1, 5, 9, 2, 6]
# expected: 9
```

### 풀이

```
[2] 사람으로 풀이:
1. 기준이 되는 max_number 선언 / 여기서 max_number는 문제에서 주어진 가장 작은 수, 나는 0으로 초기화
2. arr를 전부 탐색
3. max_number보다 크면 max_number에 할당
4. max_number를 반환

[3] 상태 변수:
변수명 max_number / el
max_number는 기준이 되는 수
el은 arr 안의 요소 하나하나 
 
max_number의 초깃값은 0
el은 arr안의 변수

max_number보다 el이 클 경우 max_number에 el 값을 할당


[4] 의사 코드:
이정도는 파이썬으로 바로 작성 가능해서 작성했음


[5] 파이썬 코드:
def solution(arr: list):
    max_number = 0
    for el in arr:
        if max_number < el:
            max_number = el

    return max_number


# 6m 9s
# expected: 9
```

---

## 문제 2: 특정 값의 등장 횟수

배열에서 특정 값 `target`이 몇 번 나오는지 반환.
**제약**: `count()`, `Counter` 쓰지 말기.

```python
arr = [1, 2, 3, 2, 4, 2, 5]
target = 2
# expected: 3
```

### 풀이

```
[2] 사람으로 풀이:
0. cnt를 선언하고 0으로 초기화
1. arr를 for문으로 순회
2. 안의 요소를 el에 저장
3. el과 target을 비교
4. 일치할 경우 cnt += 1


[3] 상태 변수:
cnt = 0
el과 target이 일치할 경우 갱신


[4] 의사 코드:
의사코드는 필요 없음


[5] 파이썬 코드:
def solution(arr, target):
    cnt = 0
    for el in arr:
        if el == target:
            cnt += 1

    return cnt


print(solution(arr, target))
# 1m 30s
```

---

## 문제 3: 두 배열의 교집합 개수

두 배열 `a`, `b`에서 **양쪽 모두에 있는** 원소의 개수.
중복은 한 번만 카운트.

```python
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
# expected: 2  (3과 4만 양쪽에 있음)
```

**제약**: `set` 연산자(`&`) 쓰지 말기. 직접 비교.

### 풀이

```
[2] 사람으로 풀이: 
1. set을 만들어서 사용
2. 두 개의 set을 순서대로 조회
3. 개수만 반환하면 되니까 cnt로 일치할 경우 cnt += 1


[3] 상태 변수:
cnt / 0 / 두 개의 set의 원소가 일치할 경우 +1


[4] 의사 코드:


[5] 파이썬 코드:
def solution(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)

    cnt = 0

    for el1 in set1:
        for el2 in set2:
            if el1 == el2:
                cnt += 1

    return cnt

<!-- 특정한 상황에서 발생하는 경우에 대한 최적화 -->
def solution(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)

    cnt = 0

    start1 = [i for i in set1].index(max(min(set1), min(set2)))
    end1 = [i for i in set1].index(min(max(set1), max(set2)))

    start2 = [i for i in set2].index(max(min(set1), min(set2)))
    end2 = [i for i in set2].index(min(max(set1), max(set2)))

    set1 = [i for i in set1][start1 : end1 + 1]

    set2 = [i for i in set2][start2 : end2 + 1]

    for el1 in set1:
        for el2 in set2:
            if el1 == el2:
                cnt += 1

    return cnt

<!-- 21m 43s -->
```

---

## 문제 4: 가장 긴 연속 같은 값의 길이

배열에서 같은 값이 연속으로 나오는 가장 긴 구간의 길이.

```python
arr = [1, 1, 2, 2, 2, 3, 1, 1, 1, 1]
# expected: 4  (마지막 1이 4번 연속)
```

**제약**: `itertools.groupby` 쓰지 말기. 직접 추적.

### 풀이

```
[2] 사람으로 풀이:
0. cnt = 0으로 초기화
0-1. 요소 값을 임시로 저장하는 변수인 temp = -1으로 초기화(문제에서 주어지지 않는 변수값)
0-2. for문으로 순회 
1. 0번째 인덱스부터 추적
2. temp에 0번째 인덱스 변수 저장
3. temp와 1번째 인덱스 변수와 일치하는지 확인
4. 일치하지 않으면 갱신(temp에 1번째 인덱스 변수 저장, cnt = 0으로 저장)
5. 일치하면 cnt += 1

[3] 상태 변수:
cnt 0으로 초기화 반환값 값이 몇개가 있는지 추적하는 변수
temp -1로 초기화한 다음 인덱스로 초기화

[4] 의사 코드:
구현하던 중에 temp를 선언하는 방식이 더 까다로울 거 같아서 arr[i+1] 포인터 방식으로 변경, 중첩 for문을 사용하는 방법도 가능할 거 같아서 시도해봄 → 단일 for문으로 가능할듯 


[5] 파이썬 코드:
def solution(arr: list):
    cnt = 1

    for i, el in enumerate(arr):
        if i + 1 == len(arr):
            break

        if el == arr[i + 1]:
            cnt += 1
        else:
            cnt = 1

    return cnt

print(solution(arr))

def solution(arr: list):
    cnt = 1

    for i in range(len(arr)):
        if i + 1 == len(arr):
            break
        if arr[i] == arr[i + 1]:
            cnt += 1
        else:
            cnt = 1

    return cnt
15m 51s
```

---

## 마치고

- 각 문제 5단계 다 채웠는지 점검
- [solutions/s1_search.py](solutions/s1_search.py)와 비교
- 가장 시간 들인 단계 = 본인 약점
- 막힌 단계는 [log.jsonl](../log.jsonl)에 기록

## 자가 점검

각 문제 끝나고 자문:
- [2] 사람으로 풀이가 [5] 파이썬 코드보다 **먼저** 떠올랐나?
- [3] 상태 변수가 **명확히 이름 붙여진** 변수인가?
- [4] 의사 코드 없이 바로 [5]로 갔다면 → 약점 신호