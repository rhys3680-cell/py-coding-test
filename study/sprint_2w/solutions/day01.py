"""Day 1 — 구현/시뮬레이션 솔루션.

풀고 나서 열 것. 막히면 20분 룰.
"""


# ---------------------------------------------------------------
# 문제 A: 두 번째로 작은 수
# ---------------------------------------------------------------
# invariant: i번째 원소까지 본 시점에,
#   small  = arr[0..i] 중 가장 작은 값
#   second = arr[0..i] 중 small과 다른 값들 중 가장 작은 값 (없으면 None)
#
# "중복은 한 번만" → second는 small과 "다른 값"이어야 한다는 조건으로 명제에 들어감.
# 이게 빠지면 [1, 1] 에서 1을 반환하는 버그가 난다.
def solution_a(arr):
    small = second = None

    for x in arr:
        if small is None or x < small:
            # x가 새 최솟값 → 기존 small이 second로 밀려남
            if small is not None and small != x:
                second = small
            small = x
        elif x != small and (second is None or x < second):
            # small과 다른 값 중 더 작은 후보
            second = x

    return second


# 실전에서 제약이 없다면 (sorted/set 허용) 이렇게 쓴다:
def solution_a_pythonic(arr):
    uniq = sorted(set(arr))
    return uniq[1] if len(uniq) > 1 else None


# ---------------------------------------------------------------
# 문제 B: 달팽이 배열
# ---------------------------------------------------------------
# 핵심: "방향 전환 조건"을 하나로 통일한다.
#   다음 칸이 (1) 격자 밖이거나 (2) 이미 채워졌으면 → 방향을 시계방향으로 90도 돌린다.
#
# 이 한 줄이 네 방향 각각의 경계 조건을 전부 대체한다.
# 구현 문제에서 조건을 유형별로 나열하기 시작하면 대개 설계가 틀린 것이다.
def solution_b(n):
    board = [[0] * n for _ in range(n)]

    # 우 → 하 → 좌 → 상 (시계 방향 순서)
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]

    r = c = d = 0
    for num in range(1, n * n + 1):
        board[r][c] = num

        nr, nc = r + dr[d], c + dc[d]
        # 밖으로 나가거나 이미 채워졌으면 방향 전환
        if not (0 <= nr < n and 0 <= nc < n) or board[nr][nc]:
            d = (d + 1) % 4
            nr, nc = r + dr[d], c + dc[d]

        r, c = nr, nc

    return board


# 마지막 칸(num == n*n)에서는 갈 곳이 없어 nr, nc가 범위 밖이 되지만
# 그 값을 쓰기 전에 루프가 끝나므로 문제없다.


if __name__ == "__main__":
    assert solution_a([3, 1, 4, 1, 5, 9, 2, 6]) == 2
    assert solution_a([1, 1, 3]) == 3
    assert solution_a([1, 1]) is None
    assert solution_a([5]) is None
    assert solution_a([]) is None
    assert solution_a([2, 1]) == 2
    assert solution_a([-1, -5, -5, 0]) == -1

    assert solution_b(1) == [[1]]
    assert solution_b(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    assert solution_b(4) == [
        [1, 2, 3, 4],
        [12, 13, 14, 5],
        [11, 16, 15, 6],
        [10, 9, 8, 7],
    ]

    print("all ok")