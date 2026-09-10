const fs = require('fs');
const path = require('path');

const root = path.resolve('Notes/Unity/渲染管线');
const files = [];
for (const name of [
  '02-可编程渲染管线基础知识.md',
  '04-Unity 中的渲染路径.md',
  '06-使用高清渲染管线资源.md',
]) files.push(path.join(root, name));
const urp = path.join(root, '05-使用通用渲染管线');
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(file);
    else if (entry.isFile() && entry.name.endsWith('.md') && path.dirname(file) !== urp) files.push(file);
  }
}
walk(urp);

const replacements = [
  [
    'https://docs.unity3d.com/cn/current/Manual/urp/rendering/forward-plus-rendering-path-landing.html',
    '[[06-URP 中的 Forward+ 渲染路径的故障排除]]',
  ],
];
let changed = 0;
for (const file of files) {
  let text = fs.readFileSync(file, 'utf8');
  const before = text;
  for (const [from, to] of replacements) text = text.split(from).join(to);
  text = text.replaceAll('https://docs.unity3d.com/cn/current/Manual/', 'https://docs.unity3d.com/6000.7/Documentation/Manual/');
  if (text !== before) {
    fs.writeFileSync(file, text, 'utf8');
    changed++;
  }
}
console.log(JSON.stringify({ files: files.length, changed }));
