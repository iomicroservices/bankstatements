from typing import Dict, Any
from .strategies import try_pdfplumber, try_camelot
from ..utils import reconcile_running_balance

MIN_CONF = 0.65

def parse_pdf(path: str) -> Dict[str, Any]:
    r1 = try_pdfplumber(path)
    best_rows = r1.rows
    best_conf = r1.confidence
    if best_conf < MIN_CONF:
        r2 = try_camelot(path)
        if len(r2.rows) > len(best_rows):
            best_rows = r2.rows
        best_conf = max(best_conf, r2.confidence)
    issues, bal_ratio = reconcile_running_balance(best_rows)
    quality = min(1.0, 0.5 * best_conf + 0.5 * bal_ratio)
    return {"rows": best_rows, "quality": round(quality, 3), "issues": issues}