class a:
    def __init__(self, b):
        self.b = b
        self.b.x = 100

class b:
    def __init__(self):
        self.x = 10

o = b()
o2 = a(o)
print(o)
print(o.x)