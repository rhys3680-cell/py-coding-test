# 패턴 치트시트 (풀이 전 30초 훑기용)

> 4번 이상 노출됐지만 미전이된 패턴, 또는 자주 쓸 파이써닉 관용구 모음.
> **목적**: 세션 시작 전 훑어서 작업 메모리에 올려두기 (retrieval practice 힌트).

---

## 1. `sum(... for ...)` — 변환 후 집계

**상황**: 각 원소를 변환해서 합치고 싶을 때

```python
# 자릿수 합 (12931, 12947)
sum(int(c) for c in str(n))

# 제곱합
sum(x**2 for x in arr)

# 조건부 합 (짝수만)
sum(x for x in arr if x % 2 == 0)

# 개수 세기 (bool → int)
sum(x > 0 for x in arr)
```

**JS로 치면**: `arr.reduce((a, x) => a + f(x), 0)`
**핵심**: `sum()`은 이터러블 받음 → 제너레이터 표현식 바로 넣기

---

## 2. 리스트 컴프리헨션 — 변환/필터

```python
# 변환만
[x * 2 for x in arr]

# 필터만
[x for x in arr if x > 0]

# 변환 + 필터
[x * 2 for x in arr if x > 0]

# 조건부 변환
[x if x > 0 else 0 for x in arr]
```

**JS로 치면**: `arr.map(x => x*2)` / `arr.filter(...)` / `arr.filter(...).map(...)`
**주의**: `if cond else` 순서
- 뒤에 `if`만 → **필터**
- 앞에 `A if c else B` → **조건부 변환**

---

## 3. `str(n)` + 자릿수 다루기

```python
# 자릿수 리스트
[int(c) for c in str(n)]

# 자릿수 합
sum(int(c) for c in str(n))

# 자릿수 뒤집어 배열
[int(c) for c in str(n)][::-1]

# 내림차순 배치
int("".join(sorted(str(n), reverse=True)))
```

---

## 4. 정렬 — `sorted` vs `list.sort`

```python
# sorted: 새 리스트 반환, chaining 가능, 모든 이터러블
sorted(arr)
sorted(arr, reverse=True)
sorted(arr, key=lambda x: x[1])
sorted("cba")  # ['a', 'b', 'c']  ← 문자열도 바로 받음

# list.sort: in-place, None 반환, 리스트만
arr.sort()
```

**규칙**: 파이프라인에 쓸 거면 `sorted`, 원본 바꿔도 되면 `.sort`

---

## 5. 뒤집기

```python
arr[::-1]           # 슬라이싱 (새 리스트/문자열)
"".join(reversed(s))  # 제너레이터 → 문자열
arr.reverse()       # in-place
```

---

## 6. f-string 자주 쓰는 형태

```python
f"{a} is {a + b}"           # 표현식
f"{x:05d}"                  # 5자리 0패딩
f"{pi:.2f}"                 # 소수점 2자리
f"{'Yes' if ok else 'No'}"  # 안에 삼항
```

---

## 7. print 활용

```python
print(*arr)                  # "1 2 3"
print(*arr, sep="\n")        # 한 줄에 하나씩
print(a, b, sep="")          # "ab" (붙여 출력)
print(x, end="")             # 개행 없이
```

---

## 8. bool ↔ int

```python
# True==1, False==0
sum(x > 0 for x in arr)      # 양수 개수
int(cond)                    # 1 또는 0
```

```python
# 불필요한 삼항 주의
return True if cond else False   # ❌
return cond                      # ✅
```

---

## 9. 정수 제곱근

```python
import math
math.isqrt(n)                 # 정수 제곱근, float 오차 없음
n == math.isqrt(n) ** 2       # 완전제곱수 판정
```

---

## 10. 정수 나눗셈

```python
a // b                        # 몫 (JS의 Math.floor(a/b))
a % b                         # 나머지
divmod(a, b)                  # (몫, 나머지) 튜플
```

---

## 사용법

1. 세션 시작 전 30초~1분간 **눈으로 훑기**
2. 실제 문제 풀 때 **"이 패턴 쓸 자리인가?"** 자문
3. 사용한 패턴은 data.jsonl `patterns_used`에 기록
4. 놓친 패턴은 `patterns_missed`에 기록

### 업데이트 규칙
- 3회 이상 안정적 전이된 패턴은 이 파일에서 제거 (이미 체화됨)
- 새로운 미전이 패턴은 추가
- 월 1회 점검