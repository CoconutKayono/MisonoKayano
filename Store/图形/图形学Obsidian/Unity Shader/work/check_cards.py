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
             *cards.glob('*.md'), *b_cards.glob('*.md'), *experiments.glob('*.md')]
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
actual = sorted(path.name[:3] for directory in (cards,b_cards)
                for path in directory.glob('[A-F][0-9][0-9]-*.md'))
assert sorted(generated) == actual, (generated, actual)
assert len(actual) == len(set(actual))
next_card = next((code for code in planned if code not in actual), 'none')
print(f'Markdown files: {len(documents)}; local links: {checked_links}; example copies: {len(exports)}')
print(f'Mainline plan: {len(planned)}; generated: {len(generated)}; next: {next_card}')
print('PASS: links, fences, copy equality, brace counts, and progress. Unity compilation NOT tested.')
