"""Static guarantees for the cross-platform Google MCP integration."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIGS = (ROOT / ".mcp.json", ROOT / ".cursor" / "mcp.json", ROOT / ".vscode" / "mcp.json")


def test_editor_mcp_configs_are_valid_and_portable() -> None:
    for path in CONFIGS:
        data = json.loads(path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers", data.get("servers"))
        assert set(servers) == {"google_search_console", "google_analytics"}
        assert servers["google_search_console"]["command"] == "gsc-mcp"
        assert servers["google_analytics"]["command"] == "analytics-mcp"
        serialized = path.read_text(encoding="utf-8")
        assert "C:\\Users\\" not in serialized
        assert ".exe" not in serialized


def test_google_mcp_environment_contract_is_consistent() -> None:
    for path in CONFIGS:
        data = json.loads(path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers", data.get("servers"))
        gsc_env = servers["google_search_console"]["env"]
        ga4_env = servers["google_analytics"]["env"]
        assert "GOOGLE_SERVICE_ACCOUNT_FILE" in gsc_env
        assert "GOOGLE_APPLICATION_CREDENTIALS" in ga4_env
        assert "GOOGLE_PROJECT_ID" in ga4_env


def test_platform_installers_and_diagnostics_exist() -> None:
    expected = (
        "install-google-gsc.ps1",
        "install-google-ga4.ps1",
        "install-google-gsc.sh",
        "install-google-ga4.sh",
        "check-google-mcp.ps1",
        "check-google-mcp.sh",
        "check-google-auth.ps1",
        "check-google-auth.sh",
    )
    for name in expected:
        assert (ROOT / "scripts" / name).is_file(), name
