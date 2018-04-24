import itertools

import dimod

from dwavecsp.core.constraint import Constraint

__all__ = ['sat2in4']


@dimod.vartype_argument('vartype')
def sat2in4(*args, vartype=dimod.BINARY, name='2-in-4', pos=tuple(), neg=tuple()):
    """2in4sat"""

    pos = args + tuple(pos)
    neg = tuple(neg)

    variables = pos + neg

    if len(variables) != 4:
        raise ValueError("")

    if neg and (len(neg) < 4):
        # because 2-in-4 sat is symmetric, all negated is the same as none negated

        const = sat2in4(pos=variables, vartype=vartype)  # make one that has no negations
        for v in neg:
            const.flip_variable(v)
            const.name = name  # overwrite the name directly

        return const

    # we can just construct them directly for speed
    if vartype is dimod.BINARY:
        configurations = frozenset([(0, 0, 1, 1),
                                    (0, 1, 0, 1),
                                    (1, 0, 0, 1),
                                    (0, 1, 1, 0),
                                    (1, 0, 1, 0),
                                    (1, 1, 0, 0)])
    else:
        # SPIN, vartype is checked by the decorator
        configurations = frozenset([(-1, -1, +1, +1),
                                    (-1, +1, -1, +1),
                                    (+1, -1, -1, +1),
                                    (-1, +1, +1, -1),
                                    (+1, -1, +1, -1),
                                    (+1, +1, -1, -1)])

    def func(a, b, c, d):
        if a == b:
            return (b != c) and (c == d)
        elif a == c:
            # a != b
            return b == d
        else:
            # a != b, a != c -> b == c
            return a == d

    return Constraint(func=func, configurations=configurations, variables=variables,
                      vartype=vartype, name=name)
