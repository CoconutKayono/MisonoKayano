"""A05-A08: deterministic numerical examples, NOT Unity/GPU execution tests."""
import math
import random
import struct
import unittest


def decode_srgb(e):
    return e / 12.92 if e <= 0.04045 else ((e + 0.055) / 1.055) ** 2.4


def encode_srgb(v):
    return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def block_bytes(width, height, block_width, block_height, size):
    return math.ceil(width / block_width) * math.ceil(height / block_height) * size


def mip_sizes(width, height):
    while True:
        yield width, height
        if width == height == 1:
            break
        width, height = max(1, width // 2), max(1, height // 2)


class ColorMeshTextureTests(unittest.TestCase):
    def test_srgb_reference_values(self):
        self.assertAlmostEqual(decode_srgb(0.5), 0.21404114048223255, places=12)
        self.assertAlmostEqual(encode_srgb(0.5), 0.7353569830524495, places=12)
        self.assertAlmostEqual(decode_srgb(decode_srgb(0.5)), 0.0376494785571514, places=12)

    def test_srgb_roundtrip_and_low_branch(self):
        for value in [0, 0.001, 0.02, 0.1, 0.25, 0.5, 0.8, 1]:
            self.assertAlmostEqual(decode_srgb(encode_srgb(value)), value, places=12)
        self.assertAlmostEqual(decode_srgb(0.04), 0.04 / 12.92, places=12)

    def test_linear_mix_and_byte_encoding(self):
        self.assertGreater(encode_srgb((0 + 1) / 2), 0.5)
        self.assertEqual(round(encode_srgb(0.5) * 255), 188)
        self.assertAlmostEqual(decode_srgb(128 / 255), 0.21586050011389926, places=12)

    def test_mask_threshold_counterexample(self):
        self.assertGreaterEqual(0.6, 0.5)
        self.assertLess(decode_srgb(0.6), 0.5)
        self.assertAlmostEqual(decode_srgb(0.6), 0.31854677812509186, places=12)

    def test_hdr_teaching_mapping(self):
        hdr = 4.0
        mapped = hdr / (1 + hdr)
        self.assertAlmostEqual(mapped, 0.8)
        self.assertAlmostEqual(encode_srgb(mapped), 0.9063317533440594, places=12)

    def test_mesh_counts_and_payload(self):
        faces, vertices_per_face, triangles_per_face = 6, 4, 2
        vertices = faces * vertices_per_face
        indices = faces * triangles_per_face * 3
        stride = (3 + 3 + 2) * 4
        self.assertEqual((vertices, indices, indices // 3, stride), (24, 36, 12, 32))
        self.assertEqual(vertices * stride + indices * 2, 840)
        self.assertEqual(vertices * stride + indices * 4, 912)

    def test_vertex_address_and_submesh_base(self):
        # baseAddress + (storedIndex + baseVertex) * stride + attributeOffset
        address = 1000 + (3 + 10) * 32 + 24
        self.assertEqual(address, 1440)
        self.assertEqual(struct.calcsize('<3f3f2f'), 32)

    def test_upload_payload(self):
        self.assertEqual(4 * 16, 64)
        self.assertEqual(1000 * 16 * 60, 960000)
        self.assertEqual(1024 * 1024 * 4 * 60 // (1024 * 1024), 240)

    def test_block_rounding(self):
        self.assertEqual(block_bytes(9, 7, 4, 4, 8), 48)
        self.assertEqual(block_bytes(1, 1, 4, 4, 8), 8)
        self.assertEqual(block_bytes(1024, 1024, 6, 6, 16), 467856)

    def test_format_table(self):
        mib = 1024 * 1024
        self.assertEqual(block_bytes(1024, 1024, 4, 4, 8), mib // 2)
        self.assertEqual(block_bytes(1024, 1024, 4, 4, 16), mib)
        self.assertEqual(1024 * 1024 * 8, 8 * mib)

    def test_mip_sum_and_small_block_tail(self):
        sizes = list(mip_sizes(1024, 1024))
        self.assertEqual(len(sizes), 11)
        self.assertEqual(sum(w * h * 4 for w, h in sizes), 5592404)
        self.assertLess(sum(w * h for w, h in sizes), 1024 ** 2 * 4 / 3)
        self.assertEqual(sum(block_bytes(w, h, 4, 4, 8)
                             for w, h in mip_sizes(4, 4)), 24)

    def test_unorm_quantization_and_boundary_error(self):
        rng = random.Random(20260906)
        bound = 0.5 / 255
        for value in [0, 0.5, 1] + [rng.random() for _ in range(1000)]:
            restored = round(value * 255) / 255
            self.assertLessEqual(abs(restored - value), bound + 1e-15)
        self.assertAlmostEqual(bound / 0.01, 0.19607843137254902)
        self.assertAlmostEqual(bound / 0.001, 1.9607843137254901)

    def test_half_float_spacing(self):
        one = struct.unpack('<e', struct.pack('<H', 0x3C00))[0]
        next_value = struct.unpack('<e', struct.pack('<H', 0x3C01))[0]
        self.assertEqual(one, 1.0)
        self.assertEqual(next_value - one, 2 ** -10)
        self.assertGreater(next_value - one, 1 / 65535)


if __name__ == '__main__':
    unittest.main(verbosity=2)
