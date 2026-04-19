---
name: pdf-book-translate
description: 将整本英文 PDF 书籍翻译为中文 Markdown。按章节提取 PDF 文本，生成结构化的中文 Markdown 文件。触发条件：用户要求翻译整本 PDF 书籍、将 PDF 翻译为 Markdown、批量翻译 PDF 章节。
---

# PDF 整书翻译技能

## 核心目标

将英文 PDF 书籍全自动翻译为中文 Markdown，保留章节结构、标题层级、列表、表格等格式，按章节目录组织输出文件。

## 执行流程

### 1. 解析 PDF 结构

```python
import pdfplumber

def extract_toc_and_chapters(pdf_path):
    """从 PDF 中提取目录结构和每个章节的页码范围"""
    with pdfplumber.open(pdf_path) as pdf:
        # 提取目录页（通常是前几页）
        toc_pages = []
        for i, page in enumerate(pdf.pages[:5]):
            text = page.extract_text()
            if text and ('Chapter' in text or 'CHAPTER' in text or '目录' in text):
                toc_pages.append((i, text))

        # 提取全文用于分段
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += f"\n--- PAGE {page.page_number} ---\n" + text

    return toc_pages, full_text
```

### 2. 识别章节边界

- 搜索 `CHAPTER X` 或 `Chapter X: Title` 模式的标题
- 通过目录页获取章节标题和页码对应关系
- 每个章节从其标题所在页开始，到下一章标题出现为止

### 3. 分段提取文本

```python
def split_into_chapters(full_text, toc_entries):
    """根据 TOC 将全文拆分为各章节"""
    chapters = []
    for i, (title, page_num) in enumerate(toc_entries):
        start_marker = f"CHAPTER {i+1}" if str(i+1).isdigit() else title
        end_marker = toc_entries[i+1][0] if i+1 < len(toc_entries) else None

        # 提取章节内容
        start_idx = full_text.find(start_marker)
        end_idx = full_text.find(end_marker, start_idx) if end_marker else len(full_text)
        chapter_text = full_text[start_idx:end_idx]
        chapters.append((title, chapter_text))
    return chapters
```

### 4. 翻译（调用翻译提示词）

对每个章节应用以下翻译规则：

```
请将以下英文内容重写成通俗流畅、引人入胜的简体中文。

核心要求：
- 读者与风格：面向技术读者的风格，清晰易懂
- 准确第一：核心事实、数据和逻辑必须与原文完全一致
- 行文流畅：优先使用地道的中文语序，英文长句拆解为中文短句
- 术语标准：专业术语使用行业公认的标准翻译，第一次出现时括号加注英文原文
- 保留格式：保持原文的标题层级、粗体、斜体、列表、表格等 Markdown 格式
- 适当解读：对于技术术语或文化差异导致的难懂内容做注释，用（**...**）包裹
- 代码块：代码内容默认不翻译，仅翻译注释或说明文字
```

### 5. 输出文件结构

```
output/
├── c1_chapter_name.md      # Chapter 1
├── c2_chapter_name.md      # Chapter 2
├── ...
├── toc.md                  # 目录索引
└── metadata.md            # 书籍元信息（标题、作者、翻译日期等）
```

### 6. 表格提取

PDF 中的表格需要特殊处理：

```python
def extract_tables_from_page(page):
    """从 PDF 页面提取表格"""
    tables = page.extract_tables()
    # 返回列表形式的表格数据 [[row1], [row2], ...]
    return tables

def tables_to_markdown(tables):
    """将表格转换为 Markdown 格式"""
    md_tables = []
    for table in tables:
        if not table:
            continue
        # 生成 Markdown 表格
        header = table[0]
        rows = table[1:]
        md = "| " + " | ".join(str(h) for h in header) + " |\n"
        md += "| " + " | ".join(["---"] * len(header)) + " |\n"
        for row in rows:
            md += "| " + " | ".join(str(c) if c else "" for c in row) + " |\n"
        md_tables.append(md)
    return md_tables
```

## 注意事项

- PDF 扫描件（图片）无法提取文本，需要 OCR 处理
- 代码块、图表标题、页眉页脚等需要人工校验
- 翻译过程中跳过版权页、空白页等非内容页
- 如果 PDF 目录不完整或页码不准，需要手动调整章节分段

## 翻译质量自检

完成后对每个章节检查：
1. 标题是否正确对应原文章节
2. 段落大意是否与原文一致
3. 术语翻译是否统一
4. 格式（列表、表格、代码块）是否保留
