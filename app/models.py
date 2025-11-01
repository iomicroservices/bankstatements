from pydantic import BaseModel
from typing import List, Optional


class Transaction(BaseModel):
    date: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    debit_credit: Optional[str] = None
    balance: Optional[float] = None
    currency: Optional[str] = None
    page_no: Optional[int] = None


class ParseResult(BaseModel):
    account: Optional[str] = None
    currency: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    quality: float = 0.0
    rows_parsed: int = 0
    issues: List[str] = []


class ParseResponse(BaseModel):
    summary: ParseResult
    transactions: List[Transaction]
    csv_path: Optional[str] = None
    xlsx_path: Optional[str] = None