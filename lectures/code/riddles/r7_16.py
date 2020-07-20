# Allowed ops: &, |, ~
# Num ops: 4
def xor1(a, b):
    return (a | b) & ~(a & b)


# Allowed ops: &, ~
# Num ops: 7
def xor2(a, b):
    return ~(~a & ~b) & ~(a & b)


# Allowed ops: &, |, ^, ~, <<, >>
# Num ops: 1
def bang(a):
    return 1 >> a


for a in range(0, 16):
    for b in range(0, 16):
        assert xor1(a, b) == a ^ b
        assert xor2(a, b) == a ^ b

for a in range(0, 16):
    assert int(not a) == bang(a)
assert bang(123456789) == 0

print("Success!")
