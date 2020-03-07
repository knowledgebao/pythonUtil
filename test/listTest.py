class A:
    def eat(self):
        print("A")

class B(A):
    def eat(self):
        super().eat()
        print("B")

class C(A):
    def eat(self):
        super().eat()
        print("C")

class D(B,C):
    def eat(self):
        super().eat()
        print("D")

test = D()
test.eat()

