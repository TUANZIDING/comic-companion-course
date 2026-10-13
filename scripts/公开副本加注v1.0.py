#!/usr/bin/env python3
"""发布准备工具，Codex新写，非原始制作记录。依赖reportlab与pypdf。
仅读取v1.0副本，在新v1.1 PDF每页下方追加声明，不改原页内容。
"""
from io import BytesIO
from pathlib import Path
import hashlib
import json
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
NOTICE_HEIGHT = 46


def publish_copy(source, destination, original_credit):
    reader = PdfReader(source)
    writer = PdfWriter()
    for old in reader.pages:
        width, height = float(old.mediabox.width), float(old.mediabox.height)
        new = PageObject.create_blank_page(width=width, height=height + NOTICE_HEIGHT)
        new.merge_transformed_page(old, Transformation().translate(0, NOTICE_HEIGHT))
        stream = BytesIO()
        notice = canvas.Canvas(stream, pagesize=(width, height + NOTICE_HEIGHT))
        notice.setFillColorRGB(.08, .2, .15)
        notice.setStrokeColorRGB(.08, .2, .15)
        notice.line(12, NOTICE_HEIGHT - 2, width - 12, NOTICE_HEIGHT - 2)
        lines = [
            "AI-assisted adaptation with Hark | Organised by Haixiang Ding, MD | Free non-commercial edition",
            original_credit,
            "PDF/artwork excluded from course CC license. Non-US and reference-material rights pending review.",
            "Contact: github.com/TUANZIDING | Commercial use requires separate rights review and authorisation.",
        ]
        notice.setFont("Helvetica", 6.5)
        for text, y in zip(lines, [34, 24, 14, 4]):
            notice.drawString(12, y, text)
        notice.save()
        new.merge_page(PdfReader(BytesIO(stream.getvalue())).pages[0])
        writer.add_page(new)
        writer.pages[-1].compress_content_streams()
    writer.add_metadata({
        "/Title": destination.stem,
        "/Author": "Haixiang Ding, MD (adaptation organiser)",
        "/Subject": "AI-assisted with Hark. Free non-commercial case study; source and regional rights pending review.",
        "/Creator": "Comic Companion Course publication notice utility",
    })
    with destination.open("wb") as file:
        writer.write(file)
    result = PdfReader(destination)
    assert len(result.pages) == len(reader.pages)
    for old, new in zip(reader.pages, result.pages):
        assert (old.extract_text() or "").strip() in (new.extract_text() or ""), "原内容文字未完整保留"
    return {"source": source.relative_to(ROOT).as_posix(), "copy": destination.relative_to(ROOT).as_posix(),
            "pages": len(result.pages), "bytes": destination.stat().st_size,
            "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "textPreserved": True, "noticeHeightPoints": NOTICE_HEIGHT}


def main():
    records = []
    for name, credit in [
        ("维尼漫画伴读", "Original: A. A. Milne text / E. H. Shepard illustrations, 1926 | Project Gutenberg #67098. No Disney references."),
        ("彼得兔漫画伴读", "Original: Beatrix Potter text and illustrations | The Tale of Peter Rabbit | Project Gutenberg #14838."),
    ]:
        for preview in ["", "预览"]:
            source = ROOT / "books" / (name + preview + "v1.0.pdf")
            destination = ROOT / "books" / (name + preview + "v1.1.pdf")
            records.append(publish_copy(source, destination, credit))
    evidence = ROOT / "docs/证据/公开副本核对v1.1.json"
    evidence.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(records, ensure_ascii=False))


if __name__ == "__main__":
    main()
