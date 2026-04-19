---
name: pdf-book-translate
description: 将英文 PDF 书籍全自动翻译为中文 Markdown。按章节提取 PDF 文本和图片，生成结构化中文 Markdown 文件。触发条件：用户要求翻译整本 PDF 书籍、将 PDF 翻译为 Markdown、批量翻译 PDF 章节。
---

# PDF 整书翻译技能

## 功能概述

| 功能 | 说明 |
|------|------|
| 文本提取 | 从 PDF 按章节提取英文原文（pdfplumber） |
| 图片提取 | 提取 PDF 中所有嵌入图片（PyMuPDF） |
| 表格提取 | 提取 PDF 中的表格并转为 Markdown |
| 批量处理 | 自动识别目录结构，按章分组输出 |
| 翻译工作流 | 英文 Markdown → 中文 Markdown，保留格式 |

## 依赖安装

```bash
pip install pdfplumber pymupdf --break-system-packages
```

## 执行流程

### 步骤 1：分析 PDF 结构

先检查 PDF 基本信息（页数、是否有可提取图片）：
```python
import fitz

doc = fitz.open("book.pdf")
print(f"总页数: {len(doc)}")

# 统计有图片的页
img_pages = set()
for i, page in enumerate(doc):
    if page.get_images():
        img_pages.add(i)
print(f"有图片的页: {sorted(img_pages)[:10]}...")
```

### 步骤 2：提取文本和图片

使用配套脚本一次性完成文本 + 图片提取：

```bash
python3 .claude/skills/pdf-book-translate/pdf_book_translate.py \
    <pdf_path> \
    <output_dir> \
    [start_page] [end_page]
```

**输出结构：**
```
output_dir/
├── c1_ChapterName.md    # 各章节英文原文
├── c2_ChapterName.md
├── ...
└── images/              # 提取的图片
    ├── p022_001_xxx.jpg  # 页码_序号_hash.扩展名
    └── ...
```

### 步骤 3：建立图片引用映射

脚本会在每个章节 Markdown 末尾追加图片引用块：
```markdown
## 图片

![图 1 (PDF第22页)](images/p022_001_xxx.png)
![图 2 (PDF第22页)](images/p022_002_xxx.png)
```

### 步骤 4：翻译 Markdown

使用 translate-markdown-zh 技能将英文 Markdown 译为中文：
- 读取英文 Markdown 文件
- 保留标题层级、粗体、斜体、列表、表格、代码块格式
- 链接标题翻译，正文转中文
- 保留图片路径不变
- 输出 `原文件名-zh.md`

## 翻译提示词

将以下英文 Markdown 内容重写为流畅的简体中文：

```
请将以下英文内容重写成通俗流畅、引人入胜的简体中文。

核心要求：
- 读者与风格：面向技术读者，清晰易懂，像讲故事而非写论文
- 准确第一：核心事实、数据和逻辑必须与原文完全一致
- 行文流畅：优先使用地道的中文语序，英文长句拆解为中文短句
- 术语标准：专业术语使用行业公认的标准翻译，第一次出现时括号加注英文原文
- 保留格式：原文的标题层级、粗体、斜体、列表、表格等 Markdown 格式原样保留
- 适当解读：对于专业术语或文化差异导致的难懂内容做注释，用（**...**）包裹
- 代码块：代码内容默认不翻译，仅翻译注释或说明文字
- 不编造：不添加原文不存在的数据、引用或结论
```

## 表格处理

PDF 中的表格用 pdfplumber 提取后转 Markdown：

```python
import pdfplumber

with pdfplumber.open("book.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if not table:
                continue
            header = table[0]
            rows = table[1:]
            md = "| " + " | ".join(str(h).strip() if h else "" for h in header) + " |\n"
            md += "| " + " | ".join(["---"] * len(header)) + " |\n"
            for row in rows:
                md += "| " + " | ".join(str(c).strip() if c else "" for c in row) + " |\n"
            print(md)
```

## 常见问题

### 1. PDF 是扫描件（无文本层）
- 现象：`page.extract_text()` 返回空
- 解决：需要 OCR 处理（pytesseract + pdf2image），不在本技能范围内

### 2. 图片提取失败（FlateDecode 压缩）
- 原因：pypdf 对某些压缩格式支持不完整
- 解决：使用 PyMuPDF（fitz），本技能已内置

### 3. PDF 目录不完整或页码不准
- 解决：手动指定页码范围 `--start-page 10 --end-page 50`

### 4. 翻译后图片不显示
- 检查：确认图片保存在 `images/` 子目录，Markdown 中引用路径正确
- 注意：翻译时图片路径不变，只移动文件到中文版本目录

## 工作流程示例

```
1. 提取 PDF 原文 + 图片
   python3 pdf_book_translate.py book.pdf output/

2. 查看生成的章节文件和图片
   ls output/
   ls output/images/ | wc -l  # 查看图片数量

3. 对每个英文 Markdown 翻译
   读取 output/c1_Introduction.md
   翻译为中文
   保存为 output/c1_Introduction-zh.md

4. 整理最终目录结构
   output/
   ├── c1_Introduction-zh.md   # 中文译文
   ├── c2_SecondChapter-zh.md
   ├── images/                 # 图片（引用路径不变）
   │   └── ...
   └── book_zh.md             # 可选：合并为单文件
```
