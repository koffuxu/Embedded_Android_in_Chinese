#!/usr/bin/env python3
"""
PDF 整书翻译脚本
用法: python3 pdf_book_translate.py <pdf_path> <output_dir> [start_page] [end_page]

依赖: pip install pdfplumber
"""

import sys
import re
import os
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("错误: 需要安装 pdfplumber，请运行: pip install pdfplumber --break-system-packages")
    sys.exit(1)


def extract_toc(pdf_path):
    """从 PDF 前10页提取目录"""
    toc_entries = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages[:10]):
            text = page.extract_text()
            if not text:
                continue
            # 匹配目录条目: "1.2 Title ............................ 5"
            pattern = r'(\d+(?:\.\d+)*)\.?\s+([A-Za-z][^\n]+?)\s+\.+\s+(\d+)'
            matches = re.findall(pattern, text)
            for m in matches:
                chapter_num = m[0].strip()
                title = m[1].strip().rstrip('.')
                page = m[2].strip()
                if title and page.isdigit():
                    toc_entries.append((chapter_num, title, int(page)))
    return toc_entries


def extract_page_text(pdf_path, page_num):
    """提取指定页码的文本（1-indexed）"""
    with pdfplumber.open(pdf_path) as pdf:
        if page_num <= len(pdf.pages):
            return pdf.pages[page_num - 1].extract_text() or ""
    return ""


def extract_chapter_text(pdf_path, start_page, end_page):
    """提取指定页码范围的文本"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start_page - 1, min(end_page, len(pdf.pages))):
            page_text = pdf.pages[i].extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def extract_tables_from_pages(pdf_path, start_page, end_page):
    """从页面范围提取所有表格"""
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start_page - 1, min(end_page, len(pdf.pages))):
            page = pdf.pages[i]
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:
                    all_tables.append(table)
    return all_tables


def tables_to_markdown(tables):
    """将表格列表转换为 Markdown 字符串"""
    md_parts = []
    for table in tables:
        if not table:
            continue
        header = table[0]
        rows = table[1:]

        # 构建 Markdown 表格
        md = "| " + " | ".join(str(h).strip() if h else "" for h in header) + " |\n"
        md += "| " + " | ".join(["---"] * len(header)) + " |\n"
        for row in rows:
            md += "| " + " | ".join(str(c).strip() if c else "" for c in row) + " |\n"
        md_parts.append(md)
    return "\n\n".join(md_parts)


def clean_text(text):
    """清理 PDF 提取文本中的噪声"""
    # 移除页眉页脚（常见模式）
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # 跳过孤立的页码行
        if re.match(r'^\s*\d+\s*$', line):
            continue
        # 移除常见页眉
        if re.match(r'^[A-Za-z\s]+\s+\d+$', line.strip()):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)


def split_into_sections(text, min_paragraph_len=50):
    """将文本拆分为段落，移除短行/噪声"""
    lines = text.split('\n')
    paragraphs = []
    current = []
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                para = ' '.join(current)
                if len(para) > min_paragraph_len:
                    paragraphs.append(para)
                current = []
        else:
            current.append(line)
    if current:
        para = ' '.join(current)
        if len(para) > min_paragraph_len:
            paragraphs.append(para)
    return paragraphs


def translate_text_to_chinese(text):
    """
    调用翻译接口将英文文本翻译为中文。
    目前为占位实现，实际使用时替换为具体翻译服务调用。
    """
    # TODO: 接入翻译服务（如 Claude API、DeepL、Google Translate 等）
    print(f"  [翻译] 文本长度: {len(text)} 字符")
    return f"[待翻译原文]\n\n{text}"


def main():
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <pdf_path> <output_dir> [start_page] [end_page]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    start_page = int(sys.argv[3]) if len(sys.argv) > 3 else None
    end_page = int(sys.argv[4]) if len(sys.argv) > 4 else None

    if not os.path.exists(pdf_path):
        print(f"错误: PDF 文件不存在: {pdf_path}")
        sys.exit(1)

    print(f"正在解析 PDF: {pdf_path}")
    toc = extract_toc(pdf_path)
    print(f"找到 {len(toc)} 个目录条目")
    for entry in toc[:10]:
        print(f"  {entry}")

    if len(toc) > 10:
        print(f"  ... 还有 {len(toc) - 10} 个条目")

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF 总页数: {total_pages}")

    # 如果指定了页码范围，只处理指定范围
    if start_page and end_page:
        print(f"\n提取页码范围: {start_page} - {end_page}")
        text = extract_chapter_text(pdf_path, start_page, end_page)
        cleaned = clean_text(text)
        output_file = output_dir / f"pages_{start_page}_{end_page}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Pages {start_page}-{end_page}\n\n")
            f.write(cleaned)
        print(f"输出: {output_file}")
    else:
        # 生成每章的 Markdown
        print("\n开始提取各章节...")
        for i, (chapter_num, title, page) in enumerate(toc):
            if i + 1 < len(toc):
                next_page = toc[i + 1][2]
            else:
                next_page = total_pages

            print(f"\n[{i+1}/{len(toc)}] {title} (页 {page}-{next_page})")
            text = extract_chapter_text(pdf_path, page, next_page)
            if not text.strip():
                print(f"  [跳过] 无内容")
                continue

            cleaned = clean_text(text)
            safe_name = re.sub(r'[^\w\s\-]', '', title)[:50].strip()
            safe_name = re.sub(r'\s+', '_', safe_name)
            output_file = output_dir / f"c{chapter_num}_{safe_name}.md"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(cleaned)

            print(f"  -> {output_file} ({len(cleaned)} 字符)")

    print(f"\n完成！文件保存在: {output_dir}")


if __name__ == "__main__":
    main()
