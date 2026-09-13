"""B01-B04 numerical teaching models. No GPU simulation or performance claim."""
import itertools
import math
import struct
import unittest


def fp16(value):
    return struct.unpack('<e', struct.pack('<e', value))[0]


def masked_wave(paths, costs):
    """Serial masked-path toy model; every lane starts active."""
    steps = sum(costs[p] for p in set(paths))
    useful = sum(costs[p] for p in paths)
    return steps, useful / (len(paths) * steps)


def resident_bound(registers, width, per_lane, max_waves):
    return min(max_waves, registers // (width * per_lane))


def pipeline(cpu_ms, gpu_ms, frames):
    """Two serial stages with unlimited buffering and overlap; no Present."""
    previous_gpu_end = 0
    ends = []
    for frame in range(frames):
        cpu_end = (frame + 1) * cpu_ms
        previous_gpu_end = max(cpu_end, previous_gpu_end) + gpu_ms
        ends.append(previous_gpu_end)
    return ends


def area2(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def clip_x_nonnegative(vertices):
    """Sutherland-Hodgman for one 2D half-plane. Not hardware rasterization."""
    output = []
    previous = vertices[-1]
    for current in vertices:
        prev_in, curr_in = previous[0] >= 0, current[0] >= 0
        if prev_in != curr_in:
            t = -previous[0] / (current[0] - previous[0])
            output.append((0.0, previous[1] + t*(current[1]-previous[1])))
        if curr_in:
            output.append(current)
        previous = current
    return output


class ShaderGeometryModels(unittest.TestCase):
    def test_variant_product_matches_enumeration(self):
        options = [(False, True), (False, True), ('A', 'B', 'C')]
        self.assertEqual(len(list(itertools.product(*options))), 12)
        self.assertEqual(math.prod(map(len, options)), 12)
        self.assertEqual(2**10, 1024)

    def test_exclusive_set_is_not_independent_booleans(self):
        self.assertEqual(len(list(itertools.product(('A', 'B', 'C'),))), 3)
        self.assertEqual(len(list(itertools.product((False, True), repeat=3))), 8)

    def test_fp16_cancellation_counterexample(self):
        a, b = 1024.5, 1024.25
        self.assertEqual(a-b, 0.25)
        self.assertEqual(fp16(a), 1024)
        self.assertEqual(fp16(b), 1024)
        self.assertEqual(fp16(a)-fp16(b), 0)
        self.assertEqual(fp16(a-b), 0.25)

    def test_uniform_wave(self):
        self.assertEqual(masked_wave(['A']*8, {'A':10, 'B':6}), (10,1))

    def test_balanced_divergence(self):
        self.assertEqual(masked_wave(['A']*4+['B']*4, {'A':10, 'B':6}), (16,0.5))

    def test_unbalanced_divergence(self):
        self.assertEqual(masked_wave(['A']+['B']*7, {'A':10, 'B':6}), (16,0.40625))

    def test_register_only_occupancy_bound(self):
        self.assertEqual(resident_bound(65536,32,32,64),64)
        self.assertEqual(resident_bound(65536,32,64,64),32)
        self.assertEqual(resident_bound(65536,32,65,64),31)

    def test_gpu_limited_pipeline(self):
        ends = pipeline(4,7,4)
        self.assertEqual(ends,[11,18,25,32])
        self.assertEqual(ends[1]-ends[0],7)
        self.assertNotEqual(ends[1]-ends[0],4+7)

    def test_cpu_limited_pipeline(self):
        self.assertEqual(pipeline(7,4,4),[11,18,25,32])

    def test_index_address_and_triangle_list(self):
        self.assertEqual(1000+(3+10)*32+24,1440)
        indices = [0,1,2,2,1,3]
        triangles = [tuple(indices[i:i+3]) for i in range(0,len(indices),3)]
        self.assertEqual(triangles,[(0,1,2),(2,1,3)])
        self.assertEqual(len(set(indices)),4)

    def test_winding_and_double_flip(self):
        p = [(0,0),(1,0),(0,1)]
        mirror = [(-x,y) for x,y in p]
        self.assertEqual(area2(*p),1)
        self.assertEqual(area2(p[0],p[2],p[1]),-1)
        self.assertEqual(area2(*mirror),-1)
        self.assertEqual(area2(mirror[0],mirror[2],mirror[1]),1)

    def test_y_axis_convention_and_degenerate(self):
        self.assertEqual(area2((0,0),(1,0),(0,-1)),-1)
        self.assertEqual(area2((0,0),(1,1),(2,2)),0)

    def test_one_outside_vertex_retains_quad(self):
        original = [(-1,0),(1,-1),(1,1)]
        clipped = clip_x_nonnegative(original)
        self.assertEqual(len(clipped),4)
        self.assertEqual(set(clipped),{(0,-0.5),(1,-1),(1,1),(0,0.5)})
        self.assertTrue(all(x>=0 for x,y in clipped))
        polygon_area = abs(sum(clipped[i][0]*clipped[(i+1)%4][1]
                               - clipped[(i+1)%4][0]*clipped[i][1]
                               for i in range(4))) / 2
        self.assertEqual(polygon_area,1.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
