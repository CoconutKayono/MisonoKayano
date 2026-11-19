"""SDF beginner demo. Python 3, standard library only.

Run: python sdf_demo.py
Writes sdf-render.png beside this script.
"""
import math
import struct
import zlib
from pathlib import Path


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, s):
    return tuple(x * s for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def length(v):
    return math.sqrt(dot(v, v))


def normalize(v):
    return mul(v, 1.0 / length(v))


def scene(p):
    # Sphere: center = (0, 0, 0), radius = 1.
    return length(p) - 1.0


def trace(ro, rd, eps=0.001, max_distance=20.0, max_steps=128):
    # Assumes a normalized ray direction and a starting point outside.
    t = 0.0
    for _ in range(max_steps):
        p = add(ro, mul(rd, t))
        d = scene(p)
        if abs(d) < eps:
            return "hit", t
        if d < 0:
            return "invalid", t
        t += d
        if t > max_distance:
            return "out_of_range", t
    return "step_limit", t


def normal(p, e=0.0001):
    dx = (e, 0.0, 0.0)
    dy = (0.0, e, 0.0)
    dz = (0.0, 0.0, e)
    g = tuple(scene(add(p, a)) - scene(add(p, mul(a, -1.0)))
              for a in (dx, dy, dz))
    return normalize(g)


def write_png(path, width, height, rgb):
    # Minimal RGB PNG encoder. This part is file I/O, not SDF math.
    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))
    stride = width * 3
    raw = b"".join(b"\x00" + bytes(rgb[y * stride:(y + 1) * stride])
                   for y in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def render(width=480, height=320):
    ro = (0.0, 0.0, 3.0)
    light = normalize((-0.6, 0.8, 1.0))  # From surface toward the light.
    rgb, mask, normals = bytearray(), bytearray(), bytearray()
    counts = {}
    for y in range(height):
        for x in range(width):
            # Dividing both axes by height preserves the aspect ratio.
            u = (2.0 * (x + 0.5) - width) / height
            v = (height - 2.0 * (y + 0.5)) / height
            rd = normalize((u, v, -1.8))
            status, t = trace(ro, rd)
            counts[status] = counts.get(status, 0) + 1
            if status == "hit":
                p = add(ro, mul(rd, t))
                n = normal(p)
                intensity = 0.15 + 0.85 * max(dot(n, light), 0.0)
                color = tuple(round(255 * c * intensity)
                              for c in (0.20, 0.68, 0.65))
                mask.extend((25, 51, 64))
                normals.extend(round(255 * (c * 0.5 + 0.5)) for c in n)
            else:
                # A step-limit result is unresolved; shown as background here.
                color = (245, 242, 235)
                mask.extend(color)
                normals.extend(color)
            rgb.extend(color)
    return rgb, mask, normals, counts


if __name__ == "__main__":
    width, height = 480, 320
    rgb, _, _, counts = render(width, height)
    output = Path(__file__).resolve().with_name("sdf-render.png")
    write_png(output, width, height, rgb)
    print(f"Saved: {output}")
    print(f"Ray results: {counts}")
