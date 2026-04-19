#!/usr/bin/env python3
"""
PDF 整书翻译脚本（支持图片提取）
用法: python3 pdf_book_translate.py <pdf_path> <output_dir> [start_page] [end_page]

依赖: pip install pdfplumber pypdf --break-system-packages
"""

import sys
import re
import os
import hashlib
import zlib
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("错误: 需要安装 pdfplumber，请运行: pip install pdfplumber --break-system-packages")
    sys.exit(1)

try:
    import fitz
except ImportError:
    print("错误: 需要安装 fitz (PyMuPDF)，请运行: pip install pymupdf --break-system-packages")
    sys.exit(1)


def extract_toc(pdf_path):
    """从 PDF 前10页提取目录"""
    toc_entries = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages[:10]):
            text = page.extract_text()
            if not text:
                continue
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
        md = "| " + " | ".join(str(h).strip() if h else "" for h in header) + " |\n"
        md += "| " + " | ".join(["---"] * len(header)) + " |\n"
        for row in rows:
            md += "| " + " | ".join(str(c).strip() if c else "" for c in row) + " |\n"
        md_parts.append(md)
    return "\n\n".join(md_parts)


def extract_images_from_pdf(pdf_path, output_dir, start_page=None, end_page=None):
    """
    使用 PyMuPDF 从 PDF 中提取所有图片，保存到 output_dir/images/ 目录。
    返回图片引用列表，每项为 (image_index, image_path, page_num, xref_id)
    """
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    image_refs = []
    image_counter = 0

    doc = fitz.open(pdf_path)
    total = len(doc)

    if start_page is None:
        start_page = 1
    if end_page is None:
        end_page = total

    # PyMuPDF 页码从 0 开始
    for page_idx in range(start_page - 1, min(end_page, total)):
        page = doc[page_idx]
        page_num = page_idx + 1

        try:
            images = page.get_images()
        except Exception:
            continue

        for img in images:
            image_counter += 1
            xref = img[0]

            try:
                base_image = doc.extract_image(xref)
                ext = base_image["ext"]
                img_data = base_image["image"]
                width = base_image["width"]
                height = base_image["height"]

                hash_str = hashlib.md5(f"{page_num}_{xref}".encode()).hexdigest()[:8]
                img_path = images_dir / f"p{page_num:03d}_{image_counter:03d}_{hash_str}.{ext}"

                with open(img_path, 'wb') as f:
                    f.write(img_data)

                image_refs.append((image_counter, str(img_path.relative_to(output_dir)), page_num, str(xref)))
                print(f"    [图片] 页 {page_num}: {img_path.name} ({len(img_data)} bytes, {width}x{height})")

            except Exception as e:
                print(f"    [跳过] 页 {page_num} 图片 {image_counter} (xref={xref}): {e}")
                image_counter -= 1

    return image_refs


def embed_images_ref_in_text(image_refs):
    """在 Markdown 正文中插入图片引用"""
    lines = []
    for img_idx, img_path, page_num, xref in image_refs:
        lines.append(f"![图 {img_idx} (PDF第{page_num}页)]({img_path})")
    return lines


def clean_text(text):
    """清理 PDF 提取文本中的噪声"""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        if re.match(r'^\s*\d+\s*$', line):
            continue
        if re.match(r'^[A-Za-z\s]+\s+\d+$', line.strip()):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)


def split_into_sections(text, min_paragraph_len=50):
    """将文本拆分为段落"""
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
    """占位翻译函数"""
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

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF 总页数: {total_pages}")

    print(f"\n开始提取图片...")
    image_refs = extract_images_from_pdf(pdf_path, output_dir, start_page, end_page)
    print(f"共提取 {len(image_refs)} 张图片\n")

    if start_page and end_page:
        print(f"提取页码范围: {start_page} - {end_page}")
        text = extract_chapter_text(pdf_path, start_page, end_page)
        cleaned = clean_text(text)
        output_file = output_dir / f"pages_{start_page}_{end_page}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Pages {start_page}-{end_page}\n\n")
            f.write(cleaned)
            if image_refs:
                f.write("\n\n## 图片\n\n")
                for line in embed_images_ref_in_text(image_refs):
                    f.write(line + "\n")
        print(f"输出: {output_file}")
    else:
        print("开始提取各章节...")
        for i, (chapter_num, title, page) in enumerate(toc):
            if i + 1 < len(toc):
                next_page = toc[i + 1][2]
            else:
                next_page = total_pages

            print(f"\n[{i+1}/{len(toc)}] {title} (页 {page}-{next_page})")

            # 提取该章节的图片
            chap_images = extract_images_from_pdf(pdf_path, output_dir, page, next_page)
            print(f"  本章图片: {len(chap_images)} 张")

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
                if chap_images:
                    f.write("\n\n## 图片\n\n")
                    for line in embed_images_ref_in_text(chap_images):
                        f.write(line + "\n")

            print(f"  -> {output_file} ({len(cleaned)} 字符)")

    print(f"\n完成！文件保存在: {output_dir}")
    print(f"图片保存在: {output_dir}/images/")


if __name__ == "__main__":
    main()
