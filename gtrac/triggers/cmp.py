from gtrac.ganglia.models import Metric

def metric_only(func):
    def wrapped(*args, **kwargs):
        if len(args) == 0 or not isinstance(args[0], Metric):
            message = "gtrac.ganglia.models.Metric expected"
            raise NotImplementedError(message)
        return func(*args, **kwargs)
    return wrapped

def do_eq(left, right):
    return left == right

@metric_only
def do_eq_ratio(left, right, reference):
    vmax = left.host[reference].value
    return (left.value / vmax * 100) == right

def do_lt(left, right):
    return left < right

@metric_only
def do_lt_ratio(left, right, reference):
    vmax = left.host[reference].value
    return (left.value / vmax * 100) < right

def do_le(left, right):
    return left <= right

@metric_only
def do_le_ratio(left, right, reference):
    vmax = left.host[reference].value
    return (left.value / vmax * 100) <= right

def do_gt(left, right):
    return left > right

@metric_only
def do_gt_ratio(left, right, reference):
    vmax = left.host[reference].value
    return (left.value / vmax * 100) > right

def do_ge(left, right):
    return left >= right

@metric_only
def do_ge_ratio(left, right, reference):
    vmax = left.host[reference].value
    return (left.value / vmax * 100) >= right

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
