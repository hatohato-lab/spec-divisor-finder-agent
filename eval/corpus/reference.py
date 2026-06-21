# 正例: 試し割りで最小の非自明な約数を返す。約数が無ければ（素数なら）None。
def find_divisor(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return i
        i += 1
    return None
