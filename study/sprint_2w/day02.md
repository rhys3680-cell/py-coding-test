# Day 2 — 문자열 처리 (2026-08-01)

**변경**: 라이브러리 제약 **없음**. `sorted`, `set`, `Counter`, 슬라이싱 전부 써도 된다.
실전과 같은 조건으로 빠르게 푸는 게 목표다.

**구성**: 짧은 문제 5개. 하나에 5~7분. 막히면 바로 다음 문제로 넘어가고 표시만 해둘 것.
**한 문제에 오래 붙들지 않는다** — 오늘 목적은 유형 감각을 넓게 잡는 것.

---

## B1. 문자열 뒤집기

```python
s = "hello"
# expected: "olleh"
```

```python
def b1(s):
    pass
```

---

## B2. 회문(팰린드롬) 판정

앞뒤가 같으면 `True`. **대소문자 무시, 공백 무시.**

```python
b2("Never odd or even")   # True
b2("hello")               # False
```

```python
def b2(s):
    pass
```

---

## B3. 가장 많이 나온 문자

문자열에서 가장 많이 등장한 문자를 반환. 공백은 제외.
동점이면 아무거나 (또는 먼저 나온 것).

```python
b3("hello world")   # 'l'
```

> `Counter` 자산 있음 → [D1_counter.md](../mini_drills/D1_counter.md)

```python
def b3(s):
    pass
```

---

## B4. 단어 단위 뒤집기

단어 순서만 뒤집는다. 단어 내부는 그대로.

```python
b4("the sky is blue")   # "blue is sky the"
```

```python
def b4(s):
    pass
```

---

## B5. 문자열 압축

연속된 같은 문자를 `문자+개수`로 압축. 압축 결과가 원본보다 길면 원본 반환.

```python
b5("aabcccccaaa")   # "a2b1c5a3"
b5("abc")           # "abc"  (압축하면 a1b1c1 로 더 길어짐)
```

> Day 1 s1r "가장 긴 연속 같은 값"과 같은 골격이다. 연속 구간 추적.

```python
def b5(s):
    pass
```

---

## 워밍업 재풀이 (Day 1 이월)

시간 남으면. 안 되면 Day 3으로 넘겨도 된다.

**A. 두 번째로 작은 수** — 이번엔 **제약 없음**. `sorted`/`set` 써서 3줄로.

```python
def solution_a(arr):
    pass
```

> Day 1 교훈: `&`는 `and`가 아니다 / 가드는 함수 맨 위 / `second` 초기화에 "비어 있음" 상태 필요

---

## 오늘 끝나고

```json
{"date":"2026-08-01","day":2,"type":"문자열","solved":?,"stuck":[],"min":?,"note":""}
```

[solutions/day02.py](solutions/day02.py)와 비교.