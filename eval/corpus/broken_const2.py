# 陰性対照: 常に 2 を返すバグ。奇数の素数・合成数では 2 で割り切れず、n=2 では 1<d<n も破る。
def find_divisor(n):
    return 2
