from typing import List, Dict, Any
import pdfplumber
import camelot
from ..utils import normalize_date, parse_amount

class StrategyResult:
    def __init__(self, rows: List[Dict[str, Any]], confidence: float):
        self.rows = rows
        self.confidence = confidence

def _row(date, desc, debit, credit, balance, page_no, currency=None):
    amt = None
    if debit:
        amt = parse_amount(debit)
        if amt is not None:
            amt = -abs(amt)
    elif credit:
        amt = parse_amount(credit)
        if amt is not None:
            amt = abs(amt)
    return {
        "date": normalize_date(date),
        "description": " ".join(str(desc or "").split()),
        "amount": amt,
        "balance": parse_amount(balance) if balance else None,
        "page_no": page_no,
        "currency": currency,
    }

def try_pdfplumber(path: str) -> StrategyResult:
    rows: List[Dict[str, Any]] = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            try:
                table = page.extract_table({
                    "horizontal_strategy": "text",
                    "vertical_strategy": "text",
                    "snap_tolerance": 3,
                })
            except Exception:
                table = None
            if not table or len(table) < 2:
                continue
            header = [str(h or "").strip().lower() for h in table[0]]
            def find_idx(cands):
                for c in cands:
                    if c in header:
                        return header.index(c)
                return None
            i_date = find_idx(["date","transaction date"]) or 0
            i_desc = find_idx(["description","details","narrative"]) or 1
            i_deb = find_idx(["debit","withdrawal","out"])
            i_cre = find_idx(["credit","deposit","in"])
            i_bal = find_idx(["balance","running balance"])
            for r in table[1:]:
                if not r or len(r) < 2:
                    continue
                get = lambda i: (r[i] if i is not None and i < len(r) else None)
                date = get(i_date); desc = get(i_desc)
                debit = get(i_deb); credit = get(i_cre); balance = get(i_bal)
                if not date and not desc:
                    continue
                rows.append(_row(date, desc, debit, credit, balance, pno))
    conf = 0.75 if rows else 0.0
    return StrategyResult(rows, conf)

def try_camelot(path: str) -> StrategyResult:
    rows: List[Dict[str, Any]] = []
    try:
        tables = camelot.read_pdf(path, pages='all', flavor='stream')
    except Exception:
        tables = []
    for t in tables:
        df = t.df
        if df.shape[0] < 2:
            continue
        header = [str(h).strip().lower() for h in list(df.iloc[0])]
        def find_col(names, default=None):
            for name in names:
                if name in header:
                    return header.index(name)
            return default
        i_date = find_col(["date","transaction date"], 0)
        i_desc = find_col(["description","details","narrative"], 1)
        i_deb = find_col(["debit","withdrawal","out"], None)
        i_cre = find_col(["credit","deposit","in"], None)
        i_bal = find_col(["balance","running balance"], None)
        for _, r in df.iloc[1:].iterrows():
            row = list(r)
            get = lambda i: (row[i] if i is not None and i < len(row) else None)
            date = get(i_date); desc = get(i_desc)
            debit = get(i_deb); credit = get(i_cre); balance = get(i_bal)
            if not date and not desc:
                continue
            rows.append(_row(date, desc, debit, credit, balance, t.page))
    conf = 0.65 if rows else 0.0
    return StrategyResult(rows, conf)