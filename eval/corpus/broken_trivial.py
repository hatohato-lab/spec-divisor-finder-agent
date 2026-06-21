# 陰性対照: 約数を見つけても n 自身を返すバグ。1<d<n を満たさない（自明な約数）。
def find_divisor(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return n  # バグ: 見つけた約数 i ではなく n を返す
        i += 1
    return None
