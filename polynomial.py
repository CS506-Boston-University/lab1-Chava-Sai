class X:
    def __init__(self):
        pass

    def __repr__(self):
        return "X"

    def evaluate(self, x_value):
        return Int(x_value)

    def simplify(self):
        return self


class Int:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return str(self.i)

    def evaluate(self, x_value):
        return Int(self.i)

    def simplify(self):
        return self


class Add:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return repr(self.p1) + " + " + repr(self.p2)

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value).i
        v2 = self.p2.evaluate(x_value).i
        return Int(v1 + v2)

    def simplify(self):
        p1 = self.p1.simplify()
        p2 = self.p2.simplify()
        # 0 + x -> x
        if isinstance(p1, Int) and p1.i == 0:
            return p2
        if isinstance(p2, Int) and p2.i == 0:
            return p1
        # Int + Int -> Int
        if isinstance(p1, Int) and isinstance(p2, Int):
            return Int(p1.i + p2.i)
        return Add(p1, p2)


class Mul:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        if isinstance(self.p1, Add):
            if isinstance(self.p2, Add):
                return "( " + repr(self.p1) + " ) * ( " + repr(self.p2) + " )"
            return "( " + repr(self.p1) + " ) * " + repr(self.p2)
        if isinstance(self.p2, Add):
            return repr(self.p1) + " * ( " + repr(self.p2) + " )"
        return repr(self.p1) + " * " + repr(self.p2)

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value).i
        v2 = self.p2.evaluate(x_value).i
        return Int(v1 * v2)

    def simplify(self):
        p1 = self.p1.simplify()
        p2 = self.p2.simplify()
        # 0 * x -> 0
        if (isinstance(p1, Int) and p1.i == 0) or (isinstance(p2, Int) and p2.i == 0):
            return Int(0)
        # 1 * x -> x
        if isinstance(p1, Int) and p1.i == 1:
            return p2
        if isinstance(p2, Int) and p2.i == 1:
            return p1
        # Int * Int -> Int
        if isinstance(p1, Int) and isinstance(p2, Int):
            return Int(p1.i * p2.i)
        return Mul(p1, p2)


class Sub:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        left = f"( {repr(self.p1)} )" if isinstance(self.p1, Add) else repr(self.p1)
        right = f"( {repr(self.p2)} )" if isinstance(self.p2, (Add, Sub)) else repr(self.p2)
        return f"{left} - {right}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value).i
        v2 = self.p2.evaluate(x_value).i
        return Int(v1 - v2)

    def simplify(self):
        p1 = self.p1.simplify()
        p2 = self.p2.simplify()
        # x - 0 -> x
        if isinstance(p2, Int) and p2.i == 0:
            return p1
        # Int - Int -> Int
        if isinstance(p1, Int) and isinstance(p2, Int):
            return Int(p1.i - p2.i)
        return Sub(p1, p2)


class Div:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        wrap_left = isinstance(self.p1, (Add, Sub))
        wrap_right = isinstance(self.p2, (Add, Sub))
        left = f"( {repr(self.p1)} )" if wrap_left else repr(self.p1)
        right = f"( {repr(self.p2)} )" if wrap_right else repr(self.p2)
        return f"{left} / {right}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value).i
        v2 = self.p2.evaluate(x_value).i
        if v2 == 0:
            raise ZeroDivisionError("Division by zero in polynomial evaluation")
        return Int(v1 // v2)

    def simplify(self):
        p1 = self.p1.simplify()
        p2 = self.p2.simplify()
        # x / 1 -> x
        if isinstance(p2, Int) and p2.i == 1:
            return p1
        # Int / Int -> Int (integer division)
        if isinstance(p1, Int) and isinstance(p2, Int) and p2.i != 0:
            return Int(p1.i // p2.i)
        return Div(p1, p2)


# Original polynomial example
poly = Add(Add(Int(4), Int(3)), Add(X(), Mul(Int(1), Add(Mul(X(), X()), Int(1)))))
print("Original polynomial:", poly)

# Test new Sub and Div classes
print("\n--- Testing Sub and Div classes ---")
try:
    sub_poly = Sub(Int(10), Int(3))
    print("Subtraction:", sub_poly)
except Exception as e:
    print("❌ Subtraction test failed - Sub class not implemented yet")

try:
    div_poly = Div(Int(15), Int(3))
    print("Division:", div_poly)
except Exception as e:
    print("❌ Division test failed - Div class not implemented yet")

# Test evaluation
print("\n--- Testing evaluation ---")
try:
    simple_poly = Add(Sub(Mul(Int(2), X()), Int(1)), Div(Int(6), Int(2)))
    print("Test polynomial:", simple_poly)
    result = simple_poly.evaluate(4)
    print(f"Evaluation for X=4: {result}")
    print(f"Simplified: {simple_poly.simplify()}")
except Exception as e:
    print("❌ Evaluation test failed - evaluate methods not implemented yet")

try:
    original_result = poly.evaluate(2)
    print(f"Original polynomial evaluation for X=2: {original_result}")
    print(f"Simplified: {poly.simplify()}")
except Exception as e:
    print(
        "❌ Original polynomial evaluation failed - evaluate methods not implemented yet"
    )

# Option to run comprehensive tests
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("\n" + "=" * 60)
        print("Running comprehensive test suite...")
        print("=" * 60)
        from test_polynomial import run_all_tests

        run_all_tests()
    else:
        print("\n💡 To run comprehensive tests, use: python polynomial.py --test")
        print("💡 Or run directly: python test_polynomial.py")
