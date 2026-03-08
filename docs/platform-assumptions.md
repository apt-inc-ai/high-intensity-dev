# Platform Assumptions

The Workstate Dashboard is intentionally optimized for a local Windows setup.

## Supported Baseline

- Windows 10/11
- Python 3.10+ on `PATH` (`python` and optionally `pythonw`)
- Windows Terminal installed (`wt` command available)
- Claude Code writing transcripts under `%USERPROFILE%\\.claude\\projects`

## Optional Integrations

- Railway metrics require:
  - `RAILWAY_TOKEN`
  - `RAILWAY_PROJECT_ID`
  - `RAILWAY_ENV_ID`
  - Optional `RAILWAY_SERVICES_JSON` (example: `{"backend":"...","frontend":"..."}`)
  - Optional `RAILWAY_API` override
- ElevenLabs usage requires:
  - `ELEVENLABS_API_KEY`

These values can be supplied either:

- As process environment variables
- In `tools/.env`

## Notes

- Session/tab auto-mapping relies on Windows-only process and UI Automation calls (`wmic`, `powershell`, UI Automation APIs).
- On non-Windows platforms, the dashboard server can still run, but Windows-specific session enrichment features may be unavailable.
