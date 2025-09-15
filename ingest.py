import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


def _ensure_docling():
    try:
        from docling.document_converter import DocumentConverter
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Docling is required. Install with: uv add docling"
        ) from e


_CONVERTER = None


def _get_converter():
    """Lazily create a DocumentConverter per process to avoid re-initialization overhead."""
    global _CONVERTER
    if _CONVERTER is None:
        from docling.document_converter import DocumentConverter

        _CONVERTER = DocumentConverter()
    return _CONVERTER


def _label_name(label: Any) -> Optional[str]:
    if label is None:
        return None
    try:
        return getattr(label, "name", None) or str(label)
    except Exception:
        return str(label)


def _element_label_name(el: Any) -> Optional[str]:
    for attr in ("label", "type", "category", "kind"):
        if hasattr(el, attr):
            name = _label_name(getattr(el, attr))
            if name:
                return name
    return None


def _element_text(el: Any) -> str:
    for attr in ("text", "content", "value", "to_text"):
        val = getattr(el, attr, None)
        if callable(val):
            try:
                txt = val()
                if isinstance(txt, str) and txt.strip():
                    return txt
            except Exception:
                pass
        elif isinstance(val, str) and val.strip():
            return val
    return str(el)


def _table_to_rows(tbl: Any) -> Optional[List[List[str]]]:
    cells = getattr(tbl, "table_cells", None)
    if cells is not None and isinstance(cells, Sequence):
        rows, row = [], []
        row_number = cells[0].end_row_offset_idx
        for cell in cells:
            if row_number != cell.end_row_offset_idx:
                rows.append(row)
                row = []
                row_number = cell.end_row_offset_idx
            row.append(_element_text(cell.text))

        rows.append(row)
        return rows
    return None


def parse_pdf_with_docling(pdf_path: Path) -> Dict[str, Any]:
    _ensure_docling()
    converter = _get_converter()
    result = converter.convert(str(pdf_path))

    elements = result.assembled.elements

    allowed_labels = {"SECTION_HEADER", "LIST_ITEM", "TEXT", "TABLE"}
    content_parts: List[str] = []
    out: Dict[str, Any] = {"source": str(pdf_path), "content": ""}

    current_header: Optional[str] = None
    pending_list: List[str] = []

    def flush_list_to_section():
        nonlocal pending_list, current_header
        if current_header and pending_list:
            existing = out.get(current_header)
            if isinstance(existing, list):
                existing.extend(pending_list)
            elif existing is None:
                out[current_header] = list(pending_list)
            pending_list = []

    for el in elements:
        label_name = _element_label_name(el)
        if label_name not in allowed_labels:
            continue

        if label_name == "SECTION_HEADER":
            flush_list_to_section()
            header_text = _element_text(el).strip()
            if header_text:
                current_header = header_text
                content_parts.append(header_text)
            continue

        if label_name == "LIST_ITEM":
            txt = _element_text(el).strip()
            if txt:
                pending_list.append(txt)
                content_parts.append(txt)
            continue

        if label_name == "TEXT":
            txt = _element_text(el).strip()
            if txt:
                content_parts.append(txt)
            continue

        if label_name == "TABLE":
            rows = _table_to_rows(el) or []
            ncols = max((len(r) for r in rows), default=0)
            if ncols != 2:
                flush_list_to_section()
                continue

            mapping: Dict[str, str] = {}
            start_idx = 0
            if rows:
                first = [c.strip().lower() for c in rows[0]]
                if any(h in first for h in ("label", "key", "name")) and any(
                    v in first for v in ("value", "val")
                ):
                    start_idx = 1

            for r in rows[start_idx:]:
                if len(r) != 2:
                    continue
                k, v = r[0].strip(), r[1].strip()
                if k:
                    mapping[k] = v

            if mapping:
                flush_list_to_section()
                if current_header:
                    existing = out.get(current_header)
                    if existing is None:
                        out[current_header] = mapping
                content_parts.extend([f"{k}: {v}" for k, v in mapping.items()])
            continue

    flush_list_to_section()

    out["content"] = "\n".join(content_parts).strip()
    return out


def _process_one(pdf: Path, output_dir: Path) -> Tuple[str, Optional[str]]:
    """Worker to parse a single PDF and write JSON.

    Returns (output_path or input path on error, error message or None).
    """
    try:
        doc_json = parse_pdf_with_docling(pdf)
        out_path = output_dir / (pdf.stem + ".json")
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(doc_json, f, ensure_ascii=False, indent=2)
        return (str(out_path), None)
    except Exception as e:
        return (str(pdf), str(e))


def ingest(input_dir: Path, output_dir: Path, workers: int = 1) -> None:
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted([p for p in input_dir.glob("**/*.pdf") if p.is_file()])
    if not pdfs:
        print(f"No PDFs found in {input_dir}")
        return

    # Determine worker count
    if workers is None or workers <= 0:
        workers = 1

    if workers == 1:
        for pdf in pdfs:
            path, err = _process_one(pdf, output_dir)
            if err:
                print(f"Failed to process {pdf}: {err}")
            else:
                print(f"Wrote {path}")
        return

    print(f"Processing {len(pdfs)} PDFs with {workers} workers...")
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_process_one, pdf, output_dir): pdf for pdf in pdfs}
        for fut in as_completed(futures):
            pdf = futures[fut]
            try:
                path, err = fut.result()
            except Exception as e:
                print(f"Failed to process {pdf}: {e}")
                continue
            if err:
                print(f"Failed to process {pdf}: {err}")
            else:
                print(f"Wrote {path}")


def main():
    parser = argparse.ArgumentParser(description="Parse PDFs with Docling and emit JSON")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("documents"),
        help="Directory with input PDFs",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory to write JSON outputs",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(max((os.cpu_count() or 2) - 1, 1), 5),
        help="Number of parallel worker processes (default: CPU count - 1)",
    )
    args = parser.parse_args()

    ingest(args.input_dir, args.output_dir, workers=args.workers)


if __name__ == "__main__":
    main()
