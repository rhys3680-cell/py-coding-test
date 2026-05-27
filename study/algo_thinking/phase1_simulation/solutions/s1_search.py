"""Phase 1 Session 1: 단순 탐색 솔루션.

각 문제의 5단계 풀이.
"""


# ============================================================
# 문제 1: 배열 최댓값
# ============================================================
"""
[2] 사람으로 풀이:
   "첫 원소를 임시 최댓값으로 둔다.
    두 번째 원소부터 본다.
    더 크면 임시 최댓값 갱신, 작거나 같으면 패스.
    끝까지 가서 임시 최댓값 반환."

[3] 상태 변수:
   - current_max: 지금까지 본 원소 중 가장 큰 값
   - 초기값: arr[0]
   - 갱신 시점: 새 원소가 더 클 때

[4] 의사 코드:
   current_max = arr[0]
   for x in arr[1:]:
       if x > current_max:
           current_max = x
   return current_max
"""


def solution_1(arr):
    current_max = arr[0]
    for x in arr[1:]:
        if x > current_max:
            current_max = x
    return current_max


print(solution_1([3, 1, 4, 1, 5, 9, 2, 6]))  # 9


# ============================================================
# 문제 2: 특정 값의 등장 횟수
# ============================================================
"""
[2] 사람으로 풀이:
   "카운트 0으로 시작.
    원소 하나씩 본다.
    target과 같으면 카운트++, 다르면 패스.
    끝까지 가서 카운트 반환."

[3] 상태 변수:
   - count: target과 일치한 횟수
   - 초기값: 0
   - 갱신: 일치 시 +1

[4] 의사 코드:
   count = 0
   for x in arr:
       if x == target:
           count += 1
   return count
"""


def solution_2(arr, target):
    count = 0
    for x in arr:
        if x == target:
            count += 1
    return count


print(solution_2([1, 2, 3, 2, 4, 2, 5], 2))  # 3


# ============================================================
# 문제 3: 두 배열의 교집합 개수
# ============================================================
"""
[2] 사람으로 풀이:
   "a의 원소 하나씩 본다.
    그게 b에도 있는지 확인.
    있으면 카운트++.
    근데 중복은 한 번만 → 이미 카운트한 거 기록해두기.
    끝까지 가서 카운트 반환."

[3] 상태 변수:
   - count: 양쪽에 있는 원소 수
   - seen: 이미 카운트한 원소 모음
   - 갱신: a 원소가 b에 있고 seen에 없으면 count++ + seen에 추가

[4] 의사 코드:
   count = 0
   seen = set()
   for x in a:
       if x in b and x not in seen:
           count += 1
           seen.add(x)
   return count
"""


def solution_3(a, b):
    count = 0
    seen = set()
    for x in a:
        if x in b and x not in seen:
            count += 1
            seen.add(x)
    return count


print(solution_3([1, 2, 3, 4], [3, 4, 5, 6]))  # 2


# ============================================================
# 문제 4: 가장 긴 연속 같은 값의 길이
# ============================================================
"""
[2] 사람으로 풀이:
   "첫 원소를 현재 값으로, 현재 길이 1로 둔다.
    두 번째 원소부터 본다.
    현재 값과 같으면 길이++, 다르면 현재 값 바꾸고 길이 1로 리셋.
    매번 최댓값 갱신.
    끝까지 가서 최댓값 반환."

[3] 상태 변수:
   - current_val: 지금 보고 있는 값
   - current_len: 그 값의 연속 길이
   - max_len: 지금까지 본 최대 연속 길이

[4] 의사 코드:
   current_val = arr[0]
   current_len = 1
   max_len = 1
   for x in arr[1:]:
       if x == current_val:
           current_len += 1
       else:
           current_val = x
           current_len = 1
       if current_len > max_len:
           max_len = current_len
   return max_len
"""


def solution_4(arr):
    current_val = arr[0]
    current_len = 1
    max_len = 1
    for x in arr[1:]:
        if x == current_val:
            current_len += 1
        else:
            current_val = x
            current_len = 1
        if current_len > max_len:
            max_len = current_len
    return max_len


print(solution_4([1, 1, 2, 2, 2, 3, 1, 1, 1, 1]))  # 4


# ============================================================
# 메타 노트
# ============================================================
"""
4문제 공통 패턴:
- 모두 "왼쪽부터 한 번 순회"
- "상태 변수 1~3개 추적"
- "조건에 따라 갱신"

이게 알고리즘 사고의 가장 기본 형태:
   초기화 → 순회 → 조건부 갱신 → 결과 반환

수식 사고와의 차이:
   수식: "n과 k의 관계로 답 계산"
   알고리즘: "한 단계씩 진행하며 상태 변화 추적"
"""