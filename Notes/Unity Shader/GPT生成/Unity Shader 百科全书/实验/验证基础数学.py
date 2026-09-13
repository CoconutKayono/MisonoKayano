"""A01-A04 的数值校验；仅使用 Python 标准库，不启动 Unity 或修改项目。

在本文件目录运行：python 验证基础数学.py
这些测试验证卡片公式与数值例子，不证明 Shader 已在 GPU 上正确运行。
"""
import math
import random
import unittest


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def unit(v):
    length = math.sqrt(dot(v, v))
    if length < 1e-12:
        raise ValueError("零向量没有可归一化的方向")
    return tuple(x / length for x in v)


def transpose(m):
    return list(zip(*m))


def mv(m, v):
    return tuple(dot(row, v) for row in m)


def mm(a, b):
    return [tuple(dot(row, col) for col in transpose(b)) for row in a]


def inverse(m):
    size = len(m)
    a = [list(map(float, row)) + [float(i == j) for j in range(size)]
         for i, row in enumerate(m)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError("矩阵不可逆")
        a[col], a[pivot] = a[pivot], a[col]
        factor = a[col][col]
        a[col] = [x / factor for x in a[col]]
        for row in range(size):
            if row != col:
                factor = a[row][col]
                a[row] = [x-factor*y for x, y in zip(a[row], a[col])]
    return [row[size:] for row in a]


def teaching_projection(n=1.0, f=9.0):
    return [(1,0,0,0), (0,1,0,0),
            (0,0,f/(n-f), f*n/(n-f)), (0,0,-1,0)]


def ndc(clip):
    if abs(clip[3]) < 1e-12:
        raise ValueError("w 为零，不能透视除法")
    return tuple(x / clip[3] for x in clip[:3])


class Foundations(unittest.TestCase):
    def vector_equal(self, actual, expected, places=9):
        self.assertEqual(len(actual), len(expected))
        for a, b in zip(actual, expected):
            self.assertAlmostEqual(a, b, places=places)

    def test_A01_length_dot_and_zero(self):
        v = (0,3,4)
        self.assertEqual(dot(v,v), 25)
        self.vector_equal(unit(v), (0,.6,.8))
        self.assertEqual(dot(v,(0,0,1)), 4)
        self.assertAlmostEqual(dot(unit(v),(0,0,1)), .8)
        with self.assertRaises(ValueError):
            unit((0,0,0))

    def test_A01_band_boundary_moves_with_length(self):
        self.assertAlmostEqual(math.degrees(math.acos(.5)), 60)
        self.assertAlmostEqual(math.degrees(math.acos(.25)), 75.522487814)
        n, light = (.8,0,.6), (0,0,1)
        self.assertAlmostEqual(dot(n,light), .6)
        self.assertAlmostEqual(dot(tuple(2*x for x in n),light), 1.2)

    def test_A01_cross_order_and_perpendicularity(self):
        self.vector_equal(cross((1,0,0),(0,1,0)), (0,0,1))
        a, b = (2,-1,3), (4,2,-1)
        c = cross(a,b)
        self.assertEqual(dot(c,a), 0)
        self.assertEqual(dot(c,b), 0)
        self.vector_equal(cross(b,a), tuple(-x for x in c))

    def test_A02_transform_order_point_vector_and_inverse(self):
        t = [(1,0,0,10), (0,1,0,0), (0,0,1,0), (0,0,0,1)]
        r = [(0,-1,0,0), (1,0,0,0), (0,0,1,0), (0,0,0,1)]
        s = [(2,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)]
        m = mm(mm(t,r),s)
        p, v = (1,1,0,1), (1,1,0,0)
        self.vector_equal(mv(m,p), (9,2,0,1))
        self.vector_equal(mv(m,v), (-1,2,0,0))
        self.vector_equal(mv(mm(mm(t,s),r),p), (8,1,0,1))
        self.vector_equal(mv(inverse(m),mv(m,p)), p)

    def test_A02_normalizing_linear_transform_is_not_rotation_only(self):
        rotated = unit((-1,1,0))
        scaled_rotated = unit((-1,2,0))
        self.assertLess(dot(rotated,scaled_rotated), .999)

    def test_A03_depth_endpoints_and_perspective(self):
        p = teaching_projection()
        self.vector_equal(ndc(mv(p,(0,0,-1,1))), (0,0,0))
        self.vector_equal(ndc(mv(p,(0,0,-9,1))), (0,0,1))
        self.vector_equal(mv(p,(1,0,-2,1)), (1,0,1.125,2))
        self.vector_equal(ndc(mv(p,(1,0,-2,1))), (.5,0,.5625))
        self.vector_equal(ndc(mv(p,(1,0,-4,1))), (.25,0,.84375))

    def test_A03_orthographic_x_independent_of_depth(self):
        # 半宽/半高为 2，近远为 1/9，观察空间朝 -Z。
        p = [(.5,0,0,0), (0,.5,0,0), (0,0,-1/8,-1/8), (0,0,0,1)]
        self.assertAlmostEqual(ndc(mv(p,(1,0,-2,1)))[0], .5)
        self.assertAlmostEqual(ndc(mv(p,(1,0,-4,1)))[0], .5)

    def test_A03_pixel_offset_requires_w(self):
        width, pixels = 800, 4
        delta = 2*pixels/width
        self.assertAlmostEqual(delta,.01)
        for w in (2,4,10):
            screen_change = ((delta*w)/w)*width/2
            self.assertAlmostEqual(screen_change,pixels)
        self.assertAlmostEqual((.02/4)*width/2, 2)

    def test_A04_nonuniform_scale_counterexample(self):
        a = [(2,0,0),(0,1,0),(0,0,1)]
        n, t = (1,1,0), (1,-1,0)
        t_prime = mv(a,t)
        wrong = mv(a,n)
        correct = mv(transpose(inverse(a)),n)
        self.vector_equal(correct,(.5,1,0))
        self.assertEqual(dot(wrong,t_prime),3)
        self.assertAlmostEqual(dot(unit(wrong),unit(t_prime)),.6)
        self.assertAlmostEqual(dot(correct,t_prime),0)
        self.assertAlmostEqual(dot(unit(wrong),(0,1,0)),1/math.sqrt(5))
        self.assertAlmostEqual(dot(unit(correct),(0,1,0)),2/math.sqrt(5))

    def test_A04_normal_constraint_for_shear_and_reflection(self):
        a = [(-2,.3,.1),(.2,1.5,.4),(0,.1,.8)]
        normal_matrix = transpose(inverse(a))
        rng = random.Random(20260906)
        for _ in range(50):
            u = tuple(rng.uniform(-2,2) for _ in range(3))
            v = tuple(rng.uniform(-2,2) for _ in range(3))
            n = cross(u,v)
            n_prime = mv(normal_matrix,n)
            self.assertAlmostEqual(dot(n_prime,mv(a,u)),0,places=8)
            self.assertAlmostEqual(dot(n_prime,mv(a,v)),0,places=8)

    def test_A04_tbn_mapping_and_flat_normal(self):
        t, b, n = (0,0,1),(0,1,0),(-1,0,0)
        tbn_columns = transpose([t,b,n])
        self.vector_equal(mv(tbn_columns,(0,0,1)),n)
        self.vector_equal(mv(tbn_columns,(.6,0,.8)),(-.8,0,.6))
        self.vector_equal(cross(n,t),b)

    def test_A04_handedness_and_determinant_identity(self):
        n, t = (0,0,1),(1,0,0)
        b = cross(n,t)
        self.vector_equal(b,(0,1,0))
        self.vector_equal(tuple(-x for x in b),(0,-1,0))
        a = [(-2,0,0),(0,3,0),(0,0,1)]
        u, v = (1,2,0),(0,1,1)
        lhs = cross(mv(a,u),mv(a,v))
        rhs = tuple(-6*x for x in mv(transpose(inverse(a)),cross(u,v)))
        self.vector_equal(lhs,rhs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
