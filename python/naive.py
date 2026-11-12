def naive_search(T: str, P: str) -> tuple[int, int]:
    """Retorna (count, checksum): nº de ocorrências e soma das posições mod 2^32."""
    n, m = len(T), len(P)
    count = checksum = 0
    if m == 0 or m > n:
        return 0, 0
    for i in range(n - m + 1):
        j = 0
        while j < m and T[i + j] == P[j]:
            j += 1
        if j == m:
            count += 1
            checksum += i
    return count, checksum & 0xFFFFFFFF
