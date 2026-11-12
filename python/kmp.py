def kmp_search(T: str, P: str) -> tuple[int, int]:
    """Retorna (count, checksum): nº de ocorrências e soma das posições mod 2^32."""
    n, m = len(T), len(P)
    if m == 0 or m > n:
        return 0, 0

    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and P[i] != P[k]:
            k = fail[k - 1]
        if P[i] == P[k]:
            k += 1
        fail[i] = k

    count = checksum = 0
    k = 0
    for i in range(n):
        while k > 0 and T[i] != P[k]:
            k = fail[k - 1]
        if T[i] == P[k]:
            k += 1
        if k == m:
            count += 1
            checksum += i + 1 - m
            k = fail[k - 1]
    return count, checksum & 0xFFFFFFFF
