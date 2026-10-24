from datetime import UTC, datetime
from io import BytesIO
import locale
import os

import pytest

from sphinx_json_schema_spec import fetch_or_load


@pytest.mark.parametrize("time_locale", ["C", ""])
def test_conditional_request_uses_http_date(
    tmp_path,
    monkeypatch,
    time_locale,
):
    cache_path = tmp_path / "spec.html"
    cache_path.write_bytes(b"<html><body>cached</body></html>")
    modified = datetime(2025, 1, 2, 15, 4, 5, tzinfo=UTC).timestamp()
    os.utime(cache_path, (modified, modified))
    requests = []

    class Response(BytesIO):
        code = 200

    def urlopen(request, context):
        requests.append(request)
        return Response(b"<html><body>fresh</body></html>")

    monkeypatch.setattr("urllib.request.urlopen", urlopen)
    previous_locale = locale.setlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, time_locale)
        result = fetch_or_load(cache_path, "https://example.com/spec.html")
    finally:
        locale.setlocale(locale.LC_TIME, previous_locale)

    assert requests[0].get_header("If-modified-since") == (
        "Thu, 02 Jan 2025 15:04:05 GMT"
    )
    assert result.find("body").text == "fresh"
