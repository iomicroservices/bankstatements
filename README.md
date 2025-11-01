This is **Step 1** of the `bankstatement` app: a minimal FastAPI service that runs in GitHub Codespaces. In later steps we'll add PDF parsing.

## How to use (Step 1)
1) Push this repo to GitHub.
2) Click **Code → Create codespace on main**.
3) Wait for the container to build. When ready, a browser tab should auto-open to the API docs.
4) If it doesn't open, run:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Then open the forwarded port 8000.

You should see `/health` returning `{ "ok": true }` and `/` showing the service name.

Step 2
In this step we add:
- Parsing dependencies (pandas, openpyxl, pdfplumber, camelot, pdf2image, pytesseract, etc.)
- A **/parse** endpoint that accepts a PDF upload, stores it under `.data/`, and returns a stub summary.

Next step we’ll implement real extraction.

We now implement **real extraction for text-based PDFs** using `pdfplumber` first and `camelot` as a fallback, then write CSV/XLSX.


OCR for scanned PDFs will come in Step 4.