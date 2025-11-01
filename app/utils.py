import re
from dateutil import parser as dparse

AMOUNT_RE = re.compile(r"[£$€]?\s*-?\(?\d{1,3}(?:,\d{3})*(?:\.\d{2})?\)?")

def normalize_date(s: str) -> str | None:
    if not s:
     return None
    s = str(s).strip()
    try:
     return dparse.parse(s, dayfirst=True, fuzzy=True).date().isoformat()
    except Exception:
        return None
    
def parse_amount(s: str | None) -> float | None:
    if s is None:
        return None
    raw = str(s).strip().replace("\u2212", "-") # U+2212 minus
    if not raw:
        return None
    neg = raw.startswith("(") and raw.endswith(")")
    raw = raw.strip("()")
    raw = raw.replace(",", "")
    raw = raw.replace("CR", "").replace("DR", "-")
    raw = raw.replace("£", "").replace("$", "").replace("€", "")
    try:
        val = float(raw)
    except Exception:
        return None
    return -val if neg else val

def reconcile_running_balance(rows):
    issues = []
    checks = passes = 0
    prev_bal = None
    for r in rows:
        bal = r.get("balance")
        amt = r.get("amount")
        if bal is None:
            continue
        if prev_bal is None:
            prev_bal = bal
            continue
        if amt is None:
            prev_bal = bal
            continue
        checks += 1
        expected = round(prev_bal + amt, 2)
        if abs(expected - bal) < 0.01:
            passes += 1
        else:
            issues.append(f"Balance mismatch p{r.get('page_no')}: expected {expected} got {bal}")
        prev_bal = bal
    ratio = (passes / checks) if checks else 0.0
    return issues, ratio