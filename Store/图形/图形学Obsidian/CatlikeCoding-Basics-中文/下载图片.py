#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载 Catlike Coding Basics 中文翻译系列引用的全部图片。

用法：
    python 下载图片.py

说明：
    - 扫描当前目录下所有 01~07 的 .md 文件（跳过 README.md）。
    - 提取形如 ![描述](https://...) 的图片链接。
    - 下载到 images/<教程名>/ 子目录，保留原文件名。
    - 已存在的图片会跳过（支持断点续传式地重复运行）。
    - 图片版权归 Catlike Coding / Jasper Flick 所有，仅供个人学习使用。
"""

import os
import re
import sys
import time
import urllib.request
from pathlib import Path

# 图片链接的 markdown 语法：![alt](url)
IMG_PATTERN = re.compile(r"!\[[^\]]*\]\((https?://[^\s)]+)\)")

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "images"

# 请求头：部分站点会拒绝默认的 Python UA
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def collect_images(md_path: Path) -> list[str]:
    """返回该 markdown 文件中所有图片 URL（去重、保持顺序）。"""
    text = md_path.read_text(encoding="utf-8")
    urls = IMG_PATTERN.findall(text)
    # 去重且保持顺序
    seen, unique = set(), []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def download(url: str, dest: Path, retries: int = 3) -> bool:
    """下载单个文件，失败时简单重试。已存在则跳过。"""
    if dest.exists():
        print(f"  跳过（已存在） {dest.name}")
        return True

    dest.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            dest.write_bytes(data)
            print(f"  已下载 {dest.name} ({len(data)} bytes)")
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"  失败（第 {attempt}/{retries} 次） {url} -> {exc}")
            if attempt < retries:
                time.sleep(1.0 * attempt)
    return False


def main() -> int:
    md_files = sorted(BASE_DIR.glob("[0-9][0-9]_*.md"))
    if not md_files:
        print("未在当前目录找到 01~07 的教程 markdown 文件。")
        return 1

    total_ok = total_fail = 0
    for md in md_files:
        urls = collect_images(md)
        if not urls:
            continue

        article_dir = OUT_DIR / md.stem
        print(f"\n[{md.name}] 共 {len(urls)} 张图片 -> {article_dir}/")

        for url in urls:
            # 取 URL 路径的最后一段作为文件名
            filename = url.split("?")[0].rstrip("/").split("/")[-1]
            if not filename or "." not in filename:
                filename = f"image_{urls.index(url)}.jpg"
            dest = article_dir / filename
            if download(url, dest):
                total_ok += 1
            else:
                total_fail += 1

    print(f"\n完成：成功/跳过 {total_ok} 张，失败 {total_fail} 张。")
    print(f"图片保存位置：{OUT_DIR}")
    return 0 if total_fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
