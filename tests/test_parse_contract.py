from fastapi.testclient import TestClient
from app.main import app


def test_parse_endpoint_contract(tmp_path):
    client = TestClient(app)
    # create a small dummy PDF (empty) so upload works
    p = tmp_path / "dummy.pdf"
    p.write_bytes(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF")

    with p.open("rb") as fh:
        r = client.post("/parse", files={"file": ("dummy.pdf", fh, "application/pdf")})
    assert r.status_code == 200
    data = r.json()
    assert "summary" in data and "transactions" in data
    assert data["summary"]["rows_parsed"] == 0