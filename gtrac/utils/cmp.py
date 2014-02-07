
def do_eq(left, right):
    return left == right

def do_lt(left, right):
    return left < right

def do_le(left, right):
    return left <= right

def do_gt(left, right):
    return left > right

def do_ge(left, right):
    return left >= right

def do_contains(left, right):
    return right in left

def do_icontains(left, right):
    return right.lower() in left.lower()

def do_in(left, right):
    return left in right

def do_iin(left, right):
    return left.lower() in right.lower()

def do_startswith(left, right):
    return left.startswith(right)

def do_istartswith(left, right):
    return left.lower().startswith(right.lower())

def do_endswith(left, right):
    return left.endswith(right)

def do_iendswith(left, right):
    return left.lower().endswith(right.lower())
