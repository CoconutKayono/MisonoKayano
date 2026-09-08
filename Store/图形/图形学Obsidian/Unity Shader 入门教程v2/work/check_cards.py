"""Check Markdown links, progress and example copies. --export writes copies only.

Does not update the learning plan/progress and does not compile Unity code.
"""
from pathlib import Path
import argparse
import re

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--export', action='store_true')
args = parser.parse_args()
cards = root / '01-数学与数据'
b_cards = root / '02-Shader执行与几何'
c_cards = root / '03-可见性与输出'
experiments = root / '实验'
exports = [
    (next(cards.glob('A01-*.md')), 'hlsl', 'A01VectorLab.shader'),
    (next(cards.glob('A02-*.md')), 'csharp', 'A02SpaceLab.cs'),
    (next(cards.glob('A03-*.md')), 'csharp', 'A03ProjectionLab.cs'),
    (next(cards.glob('A04-*.md')), 'csharp', 'A04NormalLab.cs'),
    (next(cards.glob('A05-*.md')), 'csharp', 'A05ColorLab.cs'),
    (next(cards.glob('A06-*.md')), 'csharp', 'A06MeshAudit.cs'),
    (next(cards.glob('A07-*.md')), 'csharp', 'A07BufferLab.cs'),
    (next(cards.glob('A08-*.md')), 'csharp', 'A08TextureAudit.cs'),
    (experiments / 'A阶段检查点.md', 'shaderlab', 'AStageDataLab.shader'),
    (next(b_cards.glob('B01-*.md')), 'shaderlab', 'B01VariantLab.shader'),
    (next(b_cards.glob('B02-*.md')), 'shaderlab', 'B02BranchLab.shader'),
    (next(b_cards.glob('B03-*.md')), 'csharp', 'B03CommandLab.cs'),
    (next(b_cards.glob('B03-*.md')), 'shaderlab', 'B03ClipTriangle.shader'),
    (next(b_cards.glob('B04-*.md')), 'csharp', 'B04TriangleLab.cs'),
    (next(b_cards.glob('B04-*.md')), 'shaderlab', 'B04FacingLab.shader'),
    (next(b_cards.glob('B05-*.md')), 'shaderlab', 'B05InterpolationLab.shader'),
    (next(b_cards.glob('B06-*.md')), 'csharp', 'B06TextureLab.cs'),
    (next(b_cards.glob('B06-*.md')), 'shaderlab', 'B06SamplingLab.shader'),
    (next(b_cards.glob('B07-*.md')), 'shaderlab', 'B07DepthLab.shader'),
    (next(b_cards.glob('B08-*.md')), 'csharp', 'B08StencilLab.cs'),
    (next(b_cards.glob('B08-*.md')), 'shaderlab', 'B08StencilLab.shader'),
    (next(c_cards.glob('C01-*.md')), 'shaderlab', 'C01EarlyDepthLab.shader'),
    (next(c_cards.glob('C02-*.md')), 'shaderlab', 'C02BlendLab.shader'),
    (next(c_cards.glob('C03-*.md')), 'shaderlab', 'C03MRTLab.shader'),
    (next(c_cards.glob('C03-*.md')), 'csharp', 'C03MRTLab.cs'),
    (next(c_cards.glob('C04-*.md')), 'shaderlab', 'C04CoverageLab.shader'),
    (next(c_cards.glob('C04-*.md')), 'csharp', 'C04MSAALab.cs'),
    (next(c_cards.glob('C05-*.md')), 'shaderlab', 'C05LoadStoreLab.shader'),
    (next(c_cards.glob('C05-*.md')), 'csharp', 'C05LoadStoreLab.cs'),
    (next(c_cards.glob('C06-*.md')), 'hlsl', 'C06DependencyLab.compute'),
    (next(c_cards.glob('C06-*.md')), 'csharp', 'C06DependencyLab.cs'),
    (next(c_cards.glob('C07-*.md')), 'shaderlab', 'C07DeformationLab.shader'),
    (next(c_cards.glob('C07-*.md')), 'csharp', 'C07SkinningLab.cs'),
    (next(c_cards.glob('C08-*.md')), 'shaderlab', 'C08WorkloadLab.shader'),
    (next(c_cards.glob('C08-*.md')), 'csharp', 'C08WorkloadLab.cs'),
]
for source, language, output in exports:
    content = source.read_text(encoding='utf-8')
    blocks = re.findall(r'^```' + language + r'\n(.*?)\n```', content, re.M | re.S)
    assert blocks, source
    expected = blocks[0] + '\n'
    target = experiments / output
    if args.export:
        target.write_text(expected, encoding='utf-8')
    assert target.read_text(encoding='utf-8') == expected, f'Copy mismatch: {target}'
    assert expected.count('{') == expected.count('}'), f'Brace count: {target}'

documents = [root / 'README.md', *(root / '00-学习导航').glob('*.md'),
             *cards.glob('*.md'), *b_cards.glob('*.md'), *c_cards.glob('*.md'),
             *experiments.glob('*.md')]
checked_links = 0
for source in documents:
    content = source.read_text(encoding='utf-8')
    assert len(re.findall(r'^```', content, re.M)) % 2 == 0, source
    for link in re.findall(r'\]\(([^)]+)\)', content):
        if '://' in link or link.startswith('#'):
            continue
        target = link.split('#')[0].strip('<>')
        assert (source.parent / target).exists(), f'Missing link: {source}: {link}'
        checked_links += 1

plan = (root / '00-学习导航/学习计划.md').read_text(encoding='utf-8')
planned = re.findall(r'^\| ([A-F]\d{2}) \|', plan, re.M)
assert len(planned) == len(set(planned)) == 48
progress = (root / '00-学习导航/学习进度.md').read_text(encoding='utf-8')
generated = re.findall(r'^\| \[([A-F]\d{2})\].*\| 已生成 \|', progress, re.M)
actual = sorted(path.name[:3] for directory in (cards,b_cards,c_cards)
                for path in directory.glob('[A-F][0-9][0-9]-*.md'))
assert sorted(generated) == actual, (generated, actual)
assert len(actual) == len(set(actual))
next_card = next((code for code in planned if code not in actual), 'none')
print(f'Markdown files: {len(documents)}; local links: {checked_links}; example copies: {len(exports)}')
print(f'Mainline plan: {len(planned)}; generated: {len(generated)}; next: {next_card}')
print('PASS: links, fences, copy equality, brace counts, and progress. Unity compilation NOT tested.')
