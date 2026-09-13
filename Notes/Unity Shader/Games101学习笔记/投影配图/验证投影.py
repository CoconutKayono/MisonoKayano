"""Validate the lecture-4 projection examples. Python standard library only."""

from itertools import product
from math import isclose
from pathlib import Path
import re


def mv(matrix, vector):
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4))
                       for j in range(4)) for i in range(4))


def divide(p):
    assert p[3] != 0
    return tuple(v / p[3] for v in p[:3])


def check(actual, expected):
    assert len(actual) == len(expected)
    assert all(isclose(a, e, rel_tol=1e-10, abs_tol=1e-10)
               for a, e in zip(actual, expected)), (actual, expected)


def ortho(l, r, b, t, n, f):
    return (
        (2 / (r-l), 0, 0, -(r+l) / (r-l)),
        (0, 2 / (t-b), 0, -(t+b) / (t-b)),
        (0, 0, 2 / (n-f), -(n+f) / (n-f)),
        (0, 0, 0, 1),
    )


def squish(n, f):
    return ((n, 0, 0, 0), (0, n, 0, 0),
            (0, 0, n+f, -n*f), (0, 0, 1, 0))


def main():
    cases = 0
    for l, r, b, t, n, f in [(-1, 1, -1, 1, -1, -5),
                             (2, 6, -1, 3, -2, -12)]:
        o, q = ortho(l, r, b, t, n, f), squish(n, f)
        p = mm(o, q)
        # Orthographic corners and center.
        for x, y, z in product((l, r), (b, t), (f, n)):
            check(divide(mv(o, (x, y, z, 1))),
                  (-1 if x == l else 1, -1 if y == b else 1,
                   -1 if z == f else 1))
            cases += 1
        check(divide(mv(o, ((l+r)/2, (b+t)/2, (n+f)/2, 1))), (0, 0, 0))
        previous_depth = float('inf')
        # Cross-section boundaries map to the same rectangle at every depth.
        for i in range(21):
            z = n + (f-n) * i / 20
            mapped_depth = divide(mv(p, (0, 0, z, 1)))[2]
            assert mapped_depth < previous_depth
            previous_depth = mapped_depth
            assert -1-1e-10 <= mapped_depth <= 1+1e-10
            for xs, ys in product((l, (l+r)/2, r), (b, (b+t)/2, t)):
                point = (xs*z/n, ys*z/n, z, 1)
                intermediate = divide(mv(q, point))
                check(intermediate, (xs, ys, n+f-n*f/z))
                direct = divide(mv(p, point))
                check(direct, divide(mv(o, (*intermediate, 1))))
                check(direct[:2], ((2*xs-r-l)/(r-l), (2*ys-t-b)/(t-b)))
                cases += 1
        check(divide(mv(q, (l, b, n, 1))), (l, b, n))
        check((divide(mv(q, (l*f/n, b*f/n, f, 1)))[2],), (f,))
    # Full numerical example used in the generated arithmetic diagram.
    o, q = ortho(-1, 1, -1, 1, -1, -5), squish(-1, -5)
    a = mv(q, (1, 1, -2, 1))
    check(a, (-1, -1, 7, -2))
    clip = mv(o, a)
    check(clip, (-1, -1, 0.5, -2))
    ndc = divide(clip)
    check(ndc, (0.5, 0.5, -0.25))
    check(((ndc[0]+1)*800/2, (1-ndc[1])*600/2), (600, 150))
    check(((2-4)/2, (4-4)/2, (6-4)/2), (-1, 0, 1))
    check((2/2, 2/4), (1, 0.5))
    print(f'PASS: {cases} boundary/interior cases; full example; viewport; interval; triangle ratios')

    # Local Markdown assets and formulas delimiters.
    note = Path(__file__).resolve().parent.parent / '第04讲投影详解.md'
    text = note.read_text(encoding='utf-8')
    missing = []
    for ref in re.findall(r'\]\(([^)]+)\)', text):
        if '://' in ref or ref.startswith('#'):
            continue
        if not (note.parent / ref.split('#')[0]).exists():
            missing.append(ref)
    assert not missing, f'Missing local references: {missing}'
    assert text.count('$$') % 2 == 0
    print('PASS: all local Markdown links/images exist; display-math delimiters paired')


if __name__ == '__main__':
    main()
