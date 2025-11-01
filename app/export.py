from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


def write_outputs(rows: List[Dict[str, Any]], outdir: Path, stem: str):
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    csv_path = outdir / f"{stem}.csv"
    xlsx_path = outdir / f"{stem}.xlsx"
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
    return str(csv_path), str(xlsx_path)