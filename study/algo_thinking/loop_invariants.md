# Loop Invariants — 상태 사고의 핵심

본인 진단 (2026-05-27): "간단한 건 외워서 즉답, 깊어지면 혼란."

원인: **변환 사고**(map/filter/reduce)는 자동화됐지만 **상태 사고**(loop + 상태 변수 관계)는 새 근육.

이 문서는 상태 사고의 핵심 도구 **Loop Invariant**를 본인 맥락에 맞춰 정리.

---

## 1. 변환 사고 vs 상태 사고

### 변환 사고 (본인 디폴트)
**"무엇이 어떻게 바뀌는가"** 추적.
- map: x → f(x)
- filter: x → 통과/탈락
- reduce: 누적 합산
- 함수 외우면 끝 (D1 Counter, D2 sorted key 자동화 효과)

### 상태 사고
**"무엇이 변하지 않는가"** 추적.
- 루프 돌면서도 **항상 참인 명제** = Loop Invariant
- 예: "max는 지금까지 본 원소 중 가장 큰 값"
- i가 변해도 이 **관계는 불변**

### 왜 깊은 문제에서 혼란?
- 변환 사고: 한 함수로 끝남 → 단순
- 상태 사고: 루프 + 여러 변수 + 변수들 사이 관계 → 복잡
- **단순 문제**: 변환 1번이면 됨 → 외운 패턴 적용
- **복잡 문제**: 상태 관계 추적 필수 → 변환 사고로 우회 불가

---

## 2. Loop Invariant란

**"루프의 모든 시점에서 항상 참인 명제."**

- 루프 시작 전 참
- 매 이터레이션 끝나도 참
- 루프 끝났을 때도 참

→ 이 명제 하나가 **루프 코드를 거의 자동 도출**.

### 비유

변환 사고 = "물건을 어떻게 옮길까"
상태 사고 = "옮기는 동안 무엇이 깨지면 안 되는가"

알고리즘은 후자의 사고가 코드 정확성을 보장.

---

## 3. 세 부분 프로토콜

Invariant 찾으면 자동으로 따라오는 세 부분:

### (a) Initialization (초기화)
**루프 시작 전 invariant가 참인가?**
- 변수 초기값 결정
- 빈 상태에서 명제가 trivially 참이게

### (b) Maintenance (유지)
**한 번 루프 돌고 나서도 invariant가 참인가?**
- 루프 본문 작성 가이드
- "i번째에서 참이면 i+1번째에서도 참"

### (c) Termination (종료)
**루프 끝났을 때 invariant가 답을 주는가?**
- 종료 조건 결정
- return 문 자동 도출

---

## 4. 실전 예시 — 4문제 풀어보기

### 예시 1: 최댓값 찾기

#### Invariant
> "i번째 원소까지 본 시점에, `current_max` = arr[0..i] 중 가장 큰 값"

#### 점검
- **(a) 초기화**: i=0 시점 → `current_max = arr[0]` → `arr[0..0] = {arr[0]}`의 최댓값 = arr[0] ✓
- **(b) 유지**: i번째에서 i+1번째로 넘어갈 때, arr[i+1]이 current_max보다 크면 갱신, 작거나 같으면 그대로 → 새 시점에서도 명제 참 ✓
- **(c) 종료**: i = n-1 시점에 종료 → current_max = arr[0..n-1] 최댓값 = 답 ✓

#### 코드
```python
def solution(arr):
    current_max = arr[0]                # (a)
    for x in arr[1:]:                   # (b)
        if x > current_max:
            current_max = x
    return current_max                  # (c)
```

#### 본인의 실수 분석
본인은 `max_number = 0`으로 초기화 → **(a) 초기화 실패**. 명제 "0이 [0..i] 최댓값"이 음수 배열에선 거짓. invariant 명시했으면 못 했을 실수.

---

### 예시 2: 특정 값의 등장 횟수

#### Invariant
> "i번째 원소까지 본 시점에, `cnt` = arr[0..i] 중 target과 같은 원소 개수"

#### 점검
- (a) i=−1 (보기 전), `cnt = 0`, 빈 집합의 일치 개수 = 0 ✓
- (b) arr[i+1] == target이면 cnt++, 아니면 그대로 ✓
- (c) i = n-1, cnt = 전체 일치 개수 ✓

#### 코드
```python
def solution(arr, target):
    cnt = 0
    for x in arr:
        if x == target:
            cnt += 1
    return cnt
```

본인이 이 문제는 1분 30초 만에 풂. **단순 일치 카운트는 변환 사고로도 가능** (filter + count).

---

### 예시 3: 두 배열 교집합 개수 (중복 한 번)

#### Invariant
> "i번째 원소까지 본 시점에:
>   - `cnt` = arr1[0..i] 중 arr2에 있고 처음 만난 원소 개수
>   - `seen` = arr1[0..i] 중 arr2에 있는 원소들의 집합"

핵심: **"중복 한 번"**이 invariant에 명시됨. `seen` 변수가 자동 등장.

#### 점검
- (a) 시작 시 cnt = 0, seen = set() ✓
- (b) arr1[i+1]가 arr2에 있고 seen에 없으면 cnt++ + seen에 추가 ✓
- (c) 끝나면 cnt = 답 ✓

#### 코드
```python
def solution(arr1, arr2):
    cnt = 0
    seen = set()
    for x in arr1:
        if x in arr2 and x not in seen:
            cnt += 1
            seen.add(x)
    return cnt
```

#### 본인의 실수 분석
본인 [3] 상태 변수: "`cnt = 0, 일치할 경우 +1`"
- **"중복 한 번"이 어디에도 명시 안 됨**.
- → `seen` 변수 누락
- → 이중 for 루프로 우회 (틀린 알고리즘은 아니지만 비효율)

Invariant를 한 문장으로 적었으면 "중복은?" 자문에서 막혀서 명제 보강했을 것.

---

### 예시 4: 가장 긴 연속 같은 값

#### Invariant
> "i번째 원소까지 본 시점에:
>   - `current_val` = arr[i] (현재 보고 있는 값)
>   - `current_len` = arr[i]가 i 위치에서 시작해 거꾸로 같은 값이 몇 개 연속
>   - `max_len` = arr[0..i] 중 가장 긴 연속 길이"

핵심: **"가장 긴"**이 invariant에 명시 → `max_len` 변수 자동 등장.

#### 점검
- (a) i=0: current_val=arr[0], current_len=1, max_len=1 ✓
- (b) arr[i+1]:
  - == current_val: current_len++
  - != current_val: current_val=arr[i+1], current_len=1
  - 어느 경우든: max_len = max(max_len, current_len) ✓
- (c) 끝: max_len = 답 ✓

#### 코드
```python
def solution(arr):
    current_val = arr[0]
    current_len = 1
    max_len = 1
    for x in arr[1:]:
        if x == current_val:
            current_len += 1
        else:
            current_val = x
            current_len = 1
        max_len = max(max_len, current_len)
    return max_len
```

#### 본인의 실수 분석
본인 [3]: "cnt 0 초기화 / temp -1 초기화"
- **"가장 긴"이 명시 안 됨** → `max_len` 누락
- 결과: 마지막 그룹 길이만 반환하는 **틀린 알고리즘**

Invariant에 "가장 긴"을 적었으면 → "그럼 그걸 추적할 변수는?" → max_len 자동 등장.

---

## 5. 5단계 양식 v2 (Invariant 중심)

```
[1] 문제

[2] 손풀이 (작은 입력 1개로 표 그리기):
    | i | 본 값 | 변수1 | 변수2 | ... |
    종료 → 답: ?

[3] Invariant (한 문장):
    "i번째 원소까지 본 시점에, [변수들]은 [관계]를 만족한다"
    
    체크: 문제의 모든 요구사항이 명제에 들어갔나?
    (예: "최대", "중복 한 번", "처음 만난" 같은 키워드 명시 필수)

[4] 3-부분 점검:
    (a) 초기화: 시작 시 명제 참?
    (b) 유지: 한 번 돌고도 명제 참?
    (c) 종료: 끝났을 때 명제가 답을 알려주는가?

[5] 파이썬 코드:
    (a) → 변수 초기화
    (b) → 루프 본문
    (c) → return
```

---

## 6. 핵심 차이 (구 양식 vs 새 양식)

| 구 양식 [3] | 새 양식 [3] |
|---|---|
| "변수 이름 + 초기값 + 갱신 시점" | **"한 문장 명제 (관계)"** |
| 변수 나열 | **변수 간 관계 추적** |
| 문제 조건 누락 가능 | **문제 조건이 명제에 들어감** |

핵심 통찰:
> **"무엇이 변하지 않는가"**를 한 문장으로 적으면 **나머지 코드가 따라옴**.

---

## 7. 막힘 신호 매뉴얼

### 신호 감지
- 같은 줄 5분 이상
- "더 효율적으로?" 생각
- 두 번째 접근 떠올림

### 멈춤 + 자문
1. **[3] invariant가 문제 모든 조건을 커버하나?**
   - "최대", "중복", "처음" 같은 키워드 빠졌나?
2. **[2] 손풀이 표를 작은 입력 1개로 끝까지 완성했나?**
3. **다른 접근 시도 전에 위 둘을 확인했나?**

세 가지 모두 NO면 → **새 접근 X, invariant 재정의**.

---

## 8. 다음 단계

이 문서 다 읽었으면:
1. README.md에 양식 v2 반영
2. s1 문제 3, 4 새 양식으로 다시 풀기
3. s2 누적 드릴 생성 시 양식 v2 적용

## 참고자료

- [Loop invariants can give you coding superpowers · YourBasic](https://yourbasic.org/algorithms/loop-invariants-explained/)
- [12. Invariant - CS1010 Programming Methodology](https://nus-cs1010.github.io/2122-s1/12-invariant.html)
- [Loop Invariant Condition with Examples - GeeksforGeeks](https://www.geeksforgeeks.org/dsa/loop-invariant-condition-examples-sorting-algorithms/)
- [Loop Invariant Condition | Interview Kickstart](https://www.interviewkickstart.com/learn/loop-invariant-condition-examples-sorting-algorithms)
- [Python Loop Invariants - Learning Actors](https://learningactors.com/python-loop-invariants/)