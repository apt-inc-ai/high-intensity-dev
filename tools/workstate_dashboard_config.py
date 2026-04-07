"""Configuration loader for workstate dashboard integrations."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path


DEFAULT_RAILWAY_API = "https://backboard.railway.com/graphql/v2"

DEFAULT_SERVICE_GROUPS = [
    {
        "title": "Local Services",
        "services": [
            {
                "id": "frontend",
                "name": "GUS R1 Frontend",
                "display_url": "localhost:3000",
                "probe_url": "http://localhost:3000/",
                "link_url": "http://localhost:3000/",
                "kind": "http",
            },
            {
                "id": "backend",
                "name": "GUS R1 Backend",
                "display_url": "localhost:8001/health",
                "probe_url": "http://localhost:8001/health",
                "link_url": "http://localhost:8001/health",
                "kind": "http",
            },
            {
                "id": "ampi-frontend",
                "name": "AMPI Frontend",
                "display_url": "localhost:3001",
                "probe_url": "http://localhost:3001/",
                "link_url": "http://localhost:3001/",
                "kind": "http",
            },
            {
                "id": "ampi-backend",
                "name": "AMPI Backend",
                "display_url": "localhost:8002/health",
                "probe_url": "http://localhost:8002/health",
                "link_url": "http://localhost:8002/health",
                "kind": "http",
            },
        ],
    },
    {
        "title": "Cloud Services",
        "services": [
            {
                "id": "web-frontend",
                "name": "GUS R1 Frontend",
                "display_url": "app.apt-gus.ai",
                "probe_url": "https://app.apt-gus.ai/api/health",
                "link_url": "https://app.apt-gus.ai/",
                "kind": "http",
            },
            {
                "id": "web-backend",
                "name": "GUS R1 Backend",
                "display_url": "api.apt-gus.ai/health",
                "probe_url": "https://api.apt-gus.ai/health",
                "link_url": "https://api.apt-gus.ai/health",
                "kind": "http",
            },
            {
                "id": "ampi-web-frontend",
                "name": "AMPI Frontend",
                "display_url": "ampi.apt-gus.ai",
                "probe_url": "https://ampi.apt-gus.ai/api/health",
                "link_url": "https://ampi.apt-gus.ai/",
                "kind": "http",
            },
            {
                "id": "ampi-web-backend",
                "name": "AMPI Backend",
                "display_url": "ampi-api.apt-gus.ai/health",
                "probe_url": "https://ampi-api.apt-gus.ai/health",
                "link_url": "https://ampi-api.apt-gus.ai/health",
                "kind": "http",
            },
        ],
    },
    {
        "title": "Claude Status",
        "services": [
            {
                "id": "claude-api",
                "name": "Claude API",
                "display_url": "status.claude.com",
                "link_url": "https://status.claude.com/",
                "kind": "statuspage_component",
                "component_id": "k8w3r06qmzrp",
            },
            {
                "id": "claude-code",
                "name": "Claude Code",
                "display_url": "status.claude.com",
                "link_url": "https://status.claude.com/",
                "kind": "statuspage_component",
                "component_id": "yyzkbfz2thpt",
            },
            {
                "id": "claude-ai",
                "name": "claude.ai",
                "display_url": "status.claude.com",
                "link_url": "https://status.claude.com/",
                "kind": "statuspage_component",
                "component_id": "rwppv331jlwc",
            },
        ],
    },
]

DEFAULT_PAGE_GROUPS = [
    {
        "title": "GUS R1 Local Pages",
        "links": [
            {"label": "Chat", "url": "http://localhost:3000/", "route": "/"},
            {
                "label": "Digital Twin",
                "url": "http://localhost:3000/digital-twin",
                "route": "/digital-twin",
            },
            {
                "label": "Make Room",
                "url": "http://localhost:3000/make-room",
                "route": "/make-room",
            },
            {
                "label": "Dependency Graph",
                "url": "http://localhost:3000/dependency-graph",
                "route": "/dependency-graph",
            },
            {
                "label": "Code Graph",
                "url": "http://localhost:3000/code-graph",
                "route": "/code-graph",
            },
            {
                "label": "Knowledge Graph",
                "url": "http://localhost:3000/knowledge-graph",
                "route": "/knowledge-graph",
            },
            {
                "label": "Docs Graph",
                "url": "http://localhost:3000/docs-graph",
                "route": "/docs-graph",
            },
            {"label": "Trend Chart", "url": "http://localhost:3000/chart", "route": "/chart"},
            {"label": "Report Issue", "url": "http://localhost:3000/feedback", "route": "/feedback"},
            {"label": "PowerShell 7", "action": "launch_pwsh", "route": "pwsh"},
        ],
    },
    {
        "title": "AMPI Local Pages",
        "links": [
            {"label": "Chat", "url": "http://localhost:3001/", "route": "/"},
            {
                "label": "Make Room",
                "url": "http://localhost:3001/make-room",
                "route": "/make-room",
            },
        ],
    },
    {
        "title": "GUS R1 Web Pages",
        "links": [
            {"label": "Chat", "url": "https://app.apt-gus.ai/", "route": "app.apt-gus.ai"},
            {
                "label": "Digital Twin",
                "url": "https://app.apt-gus.ai/digital-twin",
                "route": "/digital-twin",
            },
            {
                "label": "Make Room",
                "url": "https://app.apt-gus.ai/make-room",
                "route": "/make-room",
            },
            {
                "label": "Dependency Graph",
                "url": "https://app.apt-gus.ai/dependency-graph",
                "route": "/dependency-graph",
            },
            {
                "label": "Code Graph",
                "url": "https://app.apt-gus.ai/code-graph",
                "route": "/code-graph",
            },
            {
                "label": "Knowledge Graph",
                "url": "https://app.apt-gus.ai/knowledge-graph",
                "route": "/knowledge-graph",
            },
            {
                "label": "Docs Graph",
                "url": "https://app.apt-gus.ai/docs-graph",
                "route": "/docs-graph",
            },
            {"label": "Trend Chart", "url": "https://app.apt-gus.ai/chart", "route": "/chart"},
            {"label": "Report Issue", "url": "https://app.apt-gus.ai/feedback", "route": "/feedback"},
            {"label": "Docs", "url": "https://gus-docs.pages.dev/", "route": "gus-docs.pages.dev"},
            {"label": "Landing Page", "url": "https://apt-gus.ai/", "route": "apt-gus.ai"},
        ],
    },
    {
        "title": "AMPI Web Pages",
        "links": [
            {"label": "Chat", "url": "https://ampi.apt-gus.ai/", "route": "ampi.apt-gus.ai"},
            {
                "label": "Make Room",
                "url": "https://ampi.apt-gus.ai/make-room",
                "route": "/make-room",
            },
        ],
    },
]


def _load_env_value(key: str, tools_dir: Path, default: str = "") -> str:
    """Load a key from process env, then tools/.env, then default."""
    value = os.environ.get(key, "")
    if value:
        return value

    env_file = tools_dir / ".env"
    try:
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            env_key, env_value = line.split("=", 1)
            if env_key.strip() == key:
                return env_value.strip()
    except Exception:
        pass
    return default


def _load_json_value(key: str, tools_dir: Path, default):
    """Load JSON from env if present, otherwise return a deep copy of default."""
    raw = _load_env_value(key, tools_dir, "")
    if not raw:
        return copy.deepcopy(default)
    try:
        parsed = json.loads(raw)
        return parsed
    except Exception:
        return copy.deepcopy(default)


def _load_services(tools_dir: Path) -> dict[str, str]:
    """Load Railway service mapping from env JSON if present."""
    raw = _load_env_value("RAILWAY_SERVICES_JSON", tools_dir, "")
    if not raw:
        return {"backend": "", "frontend": ""}
    try:
        parsed = json.loads(raw)
        if (
            isinstance(parsed, dict)
            and isinstance(parsed.get("backend"), str)
            and isinstance(parsed.get("frontend"), str)
        ):
            return {"backend": parsed["backend"], "frontend": parsed["frontend"]}
    except Exception:
        pass
    return {"backend": "", "frontend": ""}


def load_dashboard_config(tools_dir: Path) -> dict:
    """Return resolved dashboard integration config."""
    return {
        "railway_token": _load_env_value("RAILWAY_TOKEN", tools_dir, ""),
        "railway_project_id": _load_env_value("RAILWAY_PROJECT_ID", tools_dir, ""),
        "railway_env_id": _load_env_value("RAILWAY_ENV_ID", tools_dir, ""),
        "railway_services": _load_services(tools_dir),
        "railway_api": _load_env_value("RAILWAY_API", tools_dir, DEFAULT_RAILWAY_API),
        "elevenlabs_api_key": _load_env_value("ELEVENLABS_API_KEY", tools_dir, ""),
        "service_groups": _load_json_value(
            "DASHBOARD_SERVICE_GROUPS_JSON", tools_dir, DEFAULT_SERVICE_GROUPS
        ),
        "page_groups": _load_json_value(
            "DASHBOARD_PAGE_GROUPS_JSON", tools_dir, DEFAULT_PAGE_GROUPS
        ),
    }
