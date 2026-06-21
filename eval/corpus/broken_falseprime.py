# 陰性対照: ループ条件が i*i < n（<= でない）バグ。平方数 p*p を見落とし素数扱いして None を返す。
def find_divisor(n):
    i = 2
    while i * i < n:  # バグ: <= であるべき
        if n % i == 0:
            return i
        i += 1
    return None
