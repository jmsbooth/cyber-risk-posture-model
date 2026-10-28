"""Structural PDF QA for source-matched CRPI release candidates.

This is automated geometry/renderability testing, not subjective figure QA.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

import fitz

def main(path: Path):
    raw = path.read_bytes()
    doc = fitz.open(path)
    if doc.page_count < 30 or doc.page_count > 100:
        raise SystemExit(f"Unexpected page count: {doc.page_count}")
    empty = []
    bad = []
    text_bytes = 0
    for idx, page in enumerate(doc):
        txt = page.get_text()
        text_bytes += len(txt)
        if len(txt.strip()) < 30:
            empty.append(idx+1)
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if not span["text"].strip():
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                        bad.append([idx+1, span["text"][:50], list(span["bbox"])])
        # Rasterization of every page validates renderability as well as text extraction.
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        if pix.width < 500:
            raise SystemExit(f"Page {idx+1} has anomalous raster size")
    report = {"source": str(path), "pages":doc.page_count,
              "pdf_sha256":hashlib.sha256(raw).hexdigest(),
              "extracted_characters":text_bytes,
              "empty_pages":empty, "text_outside_page":bad[:30]}
    Path("publication_pdf_qa_v02.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if empty or bad:
        raise SystemExit("PDF QA failed; inspect publication_pdf_qa_v02.json")
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    main(Path(sys.argv[1]))
