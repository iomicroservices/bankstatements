from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid

from .models import ParseResponse, ParseResult, Transaction
from .parser.core import parse_pdf_stub
from .export import write_outputs

app = FastAPI(title="bankstatement")

TMP = Path(".data")
TMP.mkdir(exist_ok=True)

@app.get("/")
def root():
    return {"service": "bankstatement", "status": "ready"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/parse", response_model=ParseResponse)
async def parse(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF")

    rid = uuid.uuid4().hex[:8]
    pdf_path = TMP / f"upload_{rid}.pdf"
    with pdf_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    result = parse_pdf_stub(str(pdf_path))
    rows = result["rows"]

    # Even if empty, write files so the API contract is stable
    csv_path, xlsx_path = write_outputs(rows, TMP, f"parsed_{rid}")

    summary = ParseResult(
        quality=result["quality"],
        rows_parsed=len(rows),
        issues=result["issues"],
    )
    tx = [Transaction(**r) for r in rows]

    return JSONResponse(ParseResponse(
        summary=summary,
        transactions=tx,
        csv_path=csv_path,
        xlsx_path=xlsx_path
    ).model_dump())