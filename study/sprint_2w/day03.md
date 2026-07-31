# Day 3 — 해시 (dict / Counter)

**왜 이 유형**: 국내 코테 빈출 1위급. 프로그래머스 "해시" 카테고리가 통째로 이것.
**"뭔가를 세거나, 짝을 찾거나, 본 적 있는지 확인"**하면 거의 다 해시다.

**난이도 조정**: Day 2가 분 단위로 끝나서 실전 체감에 맞춰 올렸다.
C1~C2는 워밍업, **C3~C5가 오늘의 본체**다.

---

## 반복 지적 (2일 연속 나온 것)

> **인덱스 접근 전에 길이를 먼저 본다.**
> `sorted(set(arr))[1]` — 원소가 1개면 터진다. Day 1, Day 2 모두 같은 패턴.
> 오늘 문제에서도 빈 입력이 들어온다. 함수 첫 줄에 가드를 쓰는 습관을 만들 것.

---

## C1. 완주하지 못한 선수 (프로그래머스 42576)

`participant`에 있는데 `completion`에 없는 사람 1명을 반환. **동명이인 있음.**

```python
c1(["leo", "kiki", "eden"], ["eden", "kiki"])              # "leo"
c1(["marina","josipa","nikola","vinko","filipa"],
   ["josipa","filipa","marina","nikola"])                  # "vinko"
c1(["mislav", "stanko", "mislav", "ana"],
   ["stanko", "ana", "mislav"])                            # "mislav"
```

> 세 번째가 함정이다. `set` 차집합으로 풀면 틀린다 — 왜인지 생각해볼 것.
> [D1_counter.md](../mini_drills/D1_counter.md) 자산 활용.

```python
def c1(participant, completion):
    pass
```

---

## C2. 두 수의 합 (Two Sum)

배열에서 더해서 `target`이 되는 **두 원소의 인덱스**를 반환.

```python
c2([2, 7, 11, 15], 9)    # [0, 1]   (2+7)
c2([3, 2, 4], 6)         # [1, 2]   (2+4)
c2([3, 3], 6)            # [0, 1]
```

> 이중 for문으로도 풀리지만 O(n²)다. **한 번 순회 O(n)**으로 푸는 게 목표.
> 힌트: "지금 값이 x면, 내가 찾던 짝은 `target - x`다. 그걸 **이미 봤나?**"

```python
def c2(nums, target):
    pass
```

---

## C3. 전화번호 목록 (프로그래머스 42577)

한 번호가 다른 번호의 **접두어**이면 `False`, 아니면 `True`.

```python
c3(["119", "97674223", "1195524421"])    # False  ("119"가 "1195524421"의 접두어)
c3(["123", "456", "789"])                # True
c3(["12", "123", "1235", "567", "88"])   # False
```

> 접근 두 가지: (a) 정렬 후 이웃만 비교 (b) set에 넣고 각 번호의 모든 접두어를 조회.
> 둘 중 하나 골라서. 왜 그게 되는지 설명할 수 있어야 한다.

```python
def c3(phone_book):
    pass
```

---

## C4. 위장 (프로그래머스 42578)

옷 종류별로 하나씩 고르거나 안 고를 수 있다. **최소 1개는 입어야 함.** 조합 수는?

```python
c4([["yellow_hat","headgear"], ["blue_sunglasses","eyewear"], ["green_turban","headgear"]])
# 5

c4([["crow_mask","face"], ["blue_sunglasses","face"], ["smoky_makeup","face"]])
# 3
```

풀어쓰면: headgear 2개(yellow_hat, green_turban), eyewear 1개.
- headgear 선택지 = 2개 + **안 입기** = 3
- eyewear 선택지 = 1개 + **안 입기** = 2
- 3 × 2 = 6 → 여기서 **전부 안 입는 경우 1개**를 빼면 5

> 이건 세는 문제다. 종류별 개수만 있으면 되고 옷 이름은 필요 없다.

```python
def c4(clothes):
    pass
```

---

## C5. 베스트앨범 (프로그래머스 42579) — 오늘의 최고난도

장르별 재생수 합이 많은 장르부터, 각 장르 안에서는 재생수 많은 곡부터 **최대 2곡**.
재생수가 같으면 **고유번호(인덱스)가 낮은 것** 먼저.

```python
c5(["classic","pop","classic","classic","pop"], [500, 600, 150, 800, 2500])
# [4, 1, 3, 0]
```

풀어쓰면:
- classic 합 = 500+150+800 = 1450 / pop 합 = 600+2500 = 3100
- pop이 먼저 → pop 중 상위 2곡: 4번(2500), 1번(600)
- classic 중 상위 2곡: 3번(800), 0번(500)

> 이건 **해시 + 정렬 조합**이다. D2 sorted(key=) 자산이 여기서 쓰인다.
> 20분 룰 적용 대상. 막히면 미련 없이 해설.

```python
def c5(genres, plays):
    pass
```

---

## 오늘 끝나고

```json
{"date":"2026-08-02","day":3,"type":"해시","solved":?,"stuck":[],"min":?,"note":""}
```

[solutions/day03.py](solutions/day03.py)와 비교.