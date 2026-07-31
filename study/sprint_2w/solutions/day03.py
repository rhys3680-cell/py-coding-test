"""Day 3 — 해시 (dict / Counter) 솔루션.

해시 유형의 공통 발상:
  "무언가를 세거나 / 짝을 찾거나 / 본 적 있는지 확인" → dict 또는 set
  리스트를 매번 훑으면 O(n²), 해시에 담아두면 조회가 O(1)이라 O(n)이 된다.
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------
# C1. 완주하지 못한 선수
# ---------------------------------------------------------------
def c1(participant, completion):
    return (Counter(participant) - Counter(completion)).most_common(1)[0][0]


# Counter 끼리 빼기가 된다. 이게 핵심 스니펫.
# set 차집합이 틀리는 이유: set 은 중복을 버린다.
#   ["mislav","stanko","mislav","ana"] → {"mislav","stanko","ana"}
#   완주자에도 mislav 가 있으니 차집합은 비어버린다.
#   "mislav 가 2명인데 1명만 완주"라는 개수 정보가 사라진 것.
# → "중복이 의미를 갖는다" 는 신호가 보이면 set 이 아니라 Counter.


def c1_manual(participant, completion):
    cnt = {}
    for p in participant:
        cnt[p] = cnt.get(p, 0) + 1
    for c in completion:
        cnt[c] -= 1
    for name, n in cnt.items():
        if n > 0:
            return name


# ---------------------------------------------------------------
# C2. 두 수의 합
# ---------------------------------------------------------------
def c2(nums, target):
    seen = {}  # 값 -> 인덱스
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


# invariant: i번째까지 본 시점에, seen 은 nums[0..i-1] 의 (값 -> 인덱스) 이다.
#
# 발상 전환이 핵심이다.
#   이중 루프  = "x 와 y 를 둘 다 고른다"        → O(n²)
#   해시       = "x 를 보는 순간 짝은 target-x 로 정해진다. 이미 봤나?" → O(n)
# 짝이 정해져 있으면 탐색이 아니라 조회다. 이 전환이 해시 유형 전체를 관통한다.
#
# seen[x] = i 를 조회 뒤에 두는 이유: 앞에 두면 [3,3] target=6 에서
# 자기 자신과 짝지어 [0,0] 이 나온다.


# ---------------------------------------------------------------
# C3. 전화번호 목록
# ---------------------------------------------------------------
def c3(phone_book):
    s = set(phone_book)
    for number in phone_book:
        for i in range(1, len(number)):
            if number[:i] in s:
                return False
    return True


# (b) 방식: 각 번호의 모든 접두어를 만들어 set 에 있는지 조회.
# 번호 길이가 최대 20 이므로 접두어 개수도 20 이하 → 사실상 O(n).


def c3_sorted(phone_book):
    phone_book.sort()
    for a, b in zip(phone_book, phone_book[1:]):
        if b.startswith(a):
            return False
    return True


# (a) 방식: 문자열 정렬하면 접두어 관계인 것끼리 반드시 이웃이 된다.
#   ["119", "1195524421", "97674223"]  ← 119 와 1195524421 이 붙는다
# 사전순 정렬에서 "짧은 쪽이 긴 쪽의 접두어" 면 그 사이에 다른 게 낄 수 없기 때문.
# zip(lst, lst[1:]) 는 이웃 쌍 만드는 관용구. 기억해둘 것.


# ---------------------------------------------------------------
# C4. 위장
# ---------------------------------------------------------------
def c4(clothes):
    cnt = Counter(kind for _, kind in clothes)

    total = 1
    for n in cnt.values():
        total *= n + 1  # +1 = "이 종류는 안 입는다"
    return total - 1  # 전부 안 입는 경우 제외


# 이름은 안 쓰고 종류별 개수만 쓴다 → Counter 에 kind 만 넣는다.
# 곱셈 원리: 종류별 선택이 독립이므로 (선택지 수)를 전부 곱한다.
# "최소 1개" 조건이 마지막 -1 로 정확히 대응된다.


# ---------------------------------------------------------------
# C5. 베스트앨범
# ---------------------------------------------------------------
def c5(genres, plays):
    total = defaultdict(int)  # 장르 -> 재생수 합
    songs = defaultdict(list)  # 장르 -> [(재생수, 인덱스), ...]

    for i, (g, p) in enumerate(zip(genres, plays)):
        total[g] += p
        songs[g].append((p, i))

    answer = []
    for g in sorted(total, key=total.get, reverse=True):
        # 재생수 내림차순, 같으면 인덱스 오름차순
        best = sorted(songs[g], key=lambda x: (-x[0], x[1]))
        answer += [i for _, i in best[:2]]
    return answer


# 3단 정렬을 분리해서 생각하면 쉬워진다:
#   1) 장르 순서   sorted(total, key=total.get, reverse=True)
#   2) 곡 순서     key=lambda x: (-x[0], x[1])   ← 튜플 정렬
#   3) 상위 2개    [:2]
#
# 튜플 key 가 핵심 스니펫이다. (-재생수, 인덱스) 로 두면
# "재생수 내림차순, 동점이면 인덱스 오름차순" 이 한 줄에 표현된다.
# 숫자에 마이너스를 붙이는 게 reverse 를 부분적으로 적용하는 관용구.
# D2 에서 자동화한 sorted(key=lambda) 가 여기서 쓰인다.


if __name__ == "__main__":
    assert c1(["leo", "kiki", "eden"], ["eden", "kiki"]) == "leo"
    assert c1(["marina", "josipa", "nikola", "vinko", "filipa"],
              ["josipa", "filipa", "marina", "nikola"]) == "vinko"
    assert c1(["mislav", "stanko", "mislav", "ana"],
              ["stanko", "ana", "mislav"]) == "mislav"
    assert c1_manual(["mislav", "stanko", "mislav", "ana"],
                     ["stanko", "ana", "mislav"]) == "mislav"

    assert c2([2, 7, 11, 15], 9) == [0, 1]
    assert c2([3, 2, 4], 6) == [1, 2]
    assert c2([3, 3], 6) == [0, 1]
    assert c2([1, 2], 99) == []

    assert c3(["119", "97674223", "1195524421"]) is False
    assert c3(["123", "456", "789"]) is True
    assert c3(["12", "123", "1235", "567", "88"]) is False
    assert c3_sorted(["119", "97674223", "1195524421"]) is False
    assert c3_sorted(["123", "456", "789"]) is True

    assert c4([["yellow_hat", "headgear"], ["blue_sunglasses", "eyewear"],
               ["green_turban", "headgear"]]) == 5
    assert c4([["crow_mask", "face"], ["blue_sunglasses", "face"],
               ["smoky_makeup", "face"]]) == 3

    assert c5(["classic", "pop", "classic", "classic", "pop"],
              [500, 600, 150, 800, 2500]) == [4, 1, 3, 0]
    assert c5(["a"], [10]) == [0]

    print("all ok")