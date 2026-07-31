"""Day 2 — 문자열 처리 솔루션.

각 문제마다 "실전용 한 줄"과 "직접 구현"을 같이 둔다.
코테에서는 위쪽(라이브러리)을 쓰면 된다. 아래쪽은 원리 확인용.
"""

from collections import Counter


# ---------------------------------------------------------------
# B1. 문자열 뒤집기
# ---------------------------------------------------------------
def b1(s):
    return s[::-1]


# 슬라이싱 [start:stop:step] 에서 step=-1 이면 뒤에서부터.
# 코테 필수 스니펫. 리스트에도 똑같이 통한다.


# ---------------------------------------------------------------
# B2. 회문 판정
# ---------------------------------------------------------------
def b2(s):
    t = s.replace(" ", "").lower()
    return t == t[::-1]


# 핵심은 "정규화 먼저, 비교 나중". 대소문자/공백 조건을 먼저 없애고 나면
# 판정 자체는 B1 한 줄이다.
# 문장부호까지 무시해야 하면: t = "".join(c for c in s.lower() if c.isalnum())


# ---------------------------------------------------------------
# B3. 가장 많이 나온 문자
# ---------------------------------------------------------------
def b3(s):
    return Counter(s.replace(" ", "")).most_common(1)[0][0]


# most_common(1) 은 [('l', 3)] 형태의 리스트를 준다.
# → [0] 으로 튜플, [0][0] 으로 문자. 이 반환형이 D1 에서 헷갈렸던 지점.
def b3_manual(s):
    cnt = {}
    for c in s:
        if c == " ":
            continue
        cnt[c] = cnt.get(c, 0) + 1
    return max(cnt, key=cnt.get)


# max(dict, key=dict.get) — 값이 가장 큰 키를 반환. 자주 쓰는 관용구.


# ---------------------------------------------------------------
# B4. 단어 단위 뒤집기
# ---------------------------------------------------------------
def b4(s):
    return " ".join(s.split()[::-1])


# split() 은 인자 없이 쓰면 연속 공백도 알아서 처리하고 양끝 공백도 버린다.
# split(" ") 로 쓰면 빈 문자열이 끼므로 인자 없이 쓰는 쪽이 안전하다.


# ---------------------------------------------------------------
# B5. 문자열 압축
# ---------------------------------------------------------------
# invariant: i번째 문자까지 본 시점에,
#   parts  = 이미 확정된 (문자,개수) 조각들
#   prev   = 지금 세고 있는 연속 구간의 문자
#   run    = 그 구간의 길이
#
# s1r "가장 긴 연속 같은 값"과 골격이 같다. 거기선 max_len 을 추적했고
# 여기선 조각을 모을 뿐이다.
def b5(s):
    if not s:
        return s

    parts = []
    prev, run = s[0], 1

    for c in s[1:]:
        if c == prev:
            run += 1
        else:
            parts.append(f"{prev}{run}")
            prev, run = c, 1
    parts.append(f"{prev}{run}")  # 마지막 구간은 루프가 안 닫아준다

    out = "".join(parts)
    return out if len(out) < len(s) else s


# 흔한 실수: 루프가 끝난 뒤 마지막 구간을 append 하는 걸 빠뜨린다.
# "연속 구간" 유형은 전부 이 함정을 공유한다. 루프 밖 마무리 한 줄을 기억할 것.


# ---------------------------------------------------------------
# 워밍업 A. 두 번째로 작은 수 (제약 없음 버전)
# ---------------------------------------------------------------
def solution_a(arr):
    uniq = sorted(set(arr))
    return uniq[1] if len(uniq) > 1 else None


# Day 1 에서 30분 걸린 문제가 제약을 풀면 2줄이다.
# set 이 "중복 한 번만" 을, sorted 가 "두 번째로 작은" 을 각각 담당한다.


if __name__ == "__main__":
    assert b1("hello") == "olleh"
    assert b1("") == ""

    assert b2("Never odd or even") is True
    assert b2("hello") is False
    assert b2("") is True

    assert b3("hello world") == "l"
    assert b3_manual("hello world") == "l"

    assert b4("the sky is blue") == "blue is sky the"
    assert b4("  hello   world  ") == "world hello"

    assert b5("aabcccccaaa") == "a2b1c5a3"
    assert b5("abc") == "abc"
    assert b5("") == ""
    assert b5("aabb") == "aabb"  # a2b2 는 4글자로 동일 → 원본 반환

    assert solution_a([3, 1, 4, 1, 5, 9, 2, 6]) == 2
    assert solution_a([1, 1, 3]) == 3
    assert solution_a([1, 1]) is None
    assert solution_a([5]) is None
    assert solution_a([]) is None

    print("all ok")