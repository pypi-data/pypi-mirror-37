import random
class fraction(object):
    numer = 0
    denom = 0
    def __init__(self, numer, denom):
        self.numer = numer
        self.denom = denom

    def total_count(self):
        return self.numer * 50

x = 3 / 2
y = 3. / 2
foo = list(range(100))
assert x == 1 and isinstance(x, int)
assert y == 1.5 and isinstance(y, float)
a = 1 + foo[len(foo) / 2]
b = 1 + foo[len(foo) * 3 / 4]
assert a == 51
assert b == 76
r = random.randint(0, 1000) * 1.0 / 1000
output = { "SUCCESS": 5, "TOTAL": 10 }
output["SUCCESS"] * 100 / output["TOTAL"]
obj = fraction(1, 50)
val = float(obj.numer) / obj.denom * 1e-9
obj.numer * obj.denom / val
obj.total_count() * val / 100
original_numer = 1
original_denom = 50
100 * abs(obj.numer - original_numer) / float(max(obj.denom, original_denom))
100 * abs(obj.numer - original_numer) / max(obj.denom, original_denom)
float(original_numer) * float(original_denom) / float(obj.numer)
