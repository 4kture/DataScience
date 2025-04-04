class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 1)

    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res

    def range_query(self, l, r):
        return self.query(r) - self.query(l - 1)

quantities = [5, 8, 3, 7, 2, 6, 4, 9, 1, 10]
n = len(quantities)

ft = FenwickTree(n)
for idx, val in enumerate(quantities, start=1):
    ft.update(idx, val)

print("Сумма с 3 по 7:", ft.range_query(3, 7))

ft.update(5, 4)
print("Сумма с 3 по 7 после обновления:", ft.range_query(3, 7))
